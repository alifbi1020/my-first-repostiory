import json
import jdatetime
from datetime import timedelta
from django.db import transaction, IntegrityError
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from venues.models import RoomUnit, Availability
from .models import Reservation


def _jalali_str_to_gregorian(date_str):
    jy, jm, jd = [int(p) for p in date_str.split('-')]
    return jdatetime.date(jy, jm, jd).togregorian()


@login_required(login_url='/accounts/login/')
def my_reservations_view(request):
    """
    کامنت: این ویو صفحه لیست رزروهای کاربر را نمایش می‌دهد.
    - فقط رزروهای فعال (غیر از لغو شده و منقضی شده) نمایش داده می‌شوند.
    - کاربر می‌تواند از اینجا رزروهای خود را لغو کند.
    """
    reservations = Reservation.objects.filter(
        user=request.user
    ).exclude(status__in=['cancelled', 'expired']).select_related(
        'room_unit__venue__city',
        'room_unit__unit_type'
    ).order_by('-date')
    
    context = {
        'reservations': reservations
    }
    return render(request, 'my_reservations.html', context)


@require_POST
def create_reservation(request):
    """
    کامنت: این ویو رزرو جدید می‌سازد.
    - اگر payment_type == 'temporary' باشد، ۱۰ دقیقه مهلت پرداخت داده می‌شود و وضعیت 'pending' می‌ماند.
    - در غیر این صورت، به‌صورت پیش‌فرض 'confirmed' می‌شود (چون درگاه واقعی نداریم).
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'login_required'}, status=401)

    try:
        payload = json.loads(request.body)
        room_unit_id = int(payload.get('room_unit_id'))
        date_str = payload.get('date')
        payment_type = payload.get('payment_type', 'gateway')  # کامنت: نوع پرداخت از فرانت ارسال می‌شود
        selected_date = _jalali_str_to_gregorian(date_str)
    except (TypeError, ValueError, AttributeError, json.JSONDecodeError):
        return JsonResponse({'error': 'invalid_data'}, status=400)

    try:
        with transaction.atomic():
            room_unit = RoomUnit.objects.select_related('venue').get(
                id=room_unit_id, venue__is_active=True
            )
            availability = Availability.objects.select_for_update().get(
                room_unit=room_unit, date=selected_date
            )
            if availability.status != 'available':
                return JsonResponse({'error': 'not_available'}, status=409)

            # کامنت: تعیین وضعیت اولیه و مهلت پرداخت بر اساس نوع پرداخت
            if payment_type == 'temporary':
                # کامنت: برای رزرو موقت، ۱۰ دقیقه مهلت پرداخت و وضعیت pending
                status = 'pending'
                deadline = timezone.now() + timedelta(minutes=10)
            else:
                # کامنت: برای کیف پول یا درگاه، فرض می‌کنیم پرداخت انجام شده و confirmed است
                status = 'confirmed'
                deadline = None

            reservation = Reservation.objects.create(
                user=request.user,
                room_unit=room_unit,
                date=selected_date,
                price_at_booking=room_unit.price_per_night,
                status=status,
                payment_type=payment_type,
                payment_deadline=deadline,
            )
            
            # کامنت: فقط اگر رزرو موقت باشد، وضعیت اتاق را 'full' می‌کنیم تا در ۱۰ دقیقه رزرو بماند
            # اگر confirmed باشد هم که قطعی است و full می‌ماند
            availability.status = 'full'
            availability.save(update_fields=['status'])
    except RoomUnit.DoesNotExist:
        return JsonResponse({'error': 'unit_not_found'}, status=404)
    except Availability.DoesNotExist:
        return JsonResponse({'error': 'not_available'}, status=409)
    except IntegrityError:
        return JsonResponse({'error': 'already_reserved'}, status=409)

    return JsonResponse({
        'success': True,
        'reservation_id': reservation.id,
        'status': reservation.status,
        'payment_deadline': reservation.payment_deadline.isoformat() if reservation.payment_deadline else None,
    })


def get_reservation_detail(request, reservation_id):
    """
    کامنت: این ویو جزئیات یک رزرو را برمی‌گرداند.
    - برای پر کردن مودال شناسنامه رزرو در فرانت استفاده می‌شود.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'login_required'}, status=401)

    try:
        reservation = Reservation.objects.select_related(
            'room_unit__venue__city',
            'room_unit__unit_type'
        ).get(id=reservation_id, user=request.user)
    except Reservation.DoesNotExist:
        return JsonResponse({'error': 'not_found'}, status=404)

    # کامنت: ساختن دیتای رزرو برای ارسال به فرانت
    data = {
        'city_name': reservation.room_unit.venue.city.name if reservation.room_unit.venue.city else '',
        'venue_name': reservation.room_unit.venue.name,
        'unit_type': reservation.room_unit.unit_type.name if reservation.room_unit.unit_type else '',
        'checkin_date': jdatetime.date.fromgregorian(date=reservation.date).strftime('%Y-%m-%d'),
        'checkout_date': jdatetime.date.fromgregorian(date=reservation.date + timedelta(days=3)).strftime('%Y-%m-%d'),
        'total_price': reservation.price_at_booking * 3,  # کامنت: فرض بر ۳ شب اقامت
        'image_url': reservation.room_unit.image.url if reservation.room_unit.image else None,
        'status': reservation.status,
        'payment_type': reservation.payment_type,
    }

    return JsonResponse({
        'success': True,
        'reservation': data
    })


@login_required(login_url='/accounts/login/')
@require_POST
def cancel_reservation(request, reservation_id):
    """
    کامنت: این ویو رزرو را لغو کرده و ظرفیت را آزاد می‌کند.
    - وضعیت رزرو به 'cancelled' تغییر می‌کند.
    - ظرفیت اتاق در تاریخ مربوطه آزاد می‌شود (status = 'available').
    """
    try:
        with transaction.atomic():
            reservation = Reservation.objects.select_related('room_unit').get(
                id=reservation_id, user=request.user
            )
            
            # کامنت: اگر رزرو قبلاً لغو یا منقضی شده، خطا می‌دهیم
            if reservation.status in ['cancelled', 'expired']:
                return JsonResponse({'error': 'already_cancelled'}, status=400)
            
            # کامنت: تغییر وضعیت رزرو به لغو شده
            reservation.status = 'cancelled'
            reservation.save(update_fields=['status'])
            
            # کامنت: آزادسازی ظرفیت اتاق در تاریخ رزرو
            availability = Availability.objects.filter(
                room_unit=reservation.room_unit,
                date=reservation.date
            ).first()
            
            if availability and availability.status == 'full':
                availability.status = 'available'
                availability.save(update_fields=['status'])
    
    except Reservation.DoesNotExist:
        return JsonResponse({'error': 'not_found'}, status=404)
    
    return JsonResponse({'success': True})
