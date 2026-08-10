import json
import jdatetime
from django.db import transaction, IntegrityError
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from venues.models import RoomUnit, Availability
from .models import Reservation


def _jalali_str_to_gregorian(date_str):
    jy, jm, jd = [int(p) for p in date_str.split('-')]
    return jdatetime.date(jy, jm, jd).togregorian()


@require_POST
def create_reservation(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'login_required'}, status=401)

    try:
        payload = json.loads(request.body)
        room_unit_id = int(payload.get('room_unit_id'))
        date_str = payload.get('date')
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

            reservation = Reservation.objects.create(
                user=request.user,
                room_unit=room_unit,
                date=selected_date,
                price_at_booking=room_unit.price_per_night,
                status='pending',
            )
            availability.status = 'full'
            availability.save(update_fields=['status'])
    except RoomUnit.DoesNotExist:
        return JsonResponse({'error': 'unit_not_found'}, status=404)
    except Availability.DoesNotExist:
        return JsonResponse({'error': 'not_available'}, status=409)
    except IntegrityError:
        return JsonResponse({'error': 'already_reserved'}, status=409)

    return JsonResponse({'success': True, 'reservation_id': reservation.id})
