import jdatetime
from datetime import date as date_cls, timedelta
from django.shortcuts import render
from .models import Venue, city, RoomUnit
from django.http import JsonResponse

FA_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
JALALI_MONTHS = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
                  "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]


def to_jalali_display(g_date):
    j = jdatetime.date.fromgregorian(date=g_date)
    day = str(j.day).translate(FA_DIGITS)
    month = JALALI_MONTHS[j.month - 1]
    year = str(j.year).translate(FA_DIGITS)
    return f"{day} {month} {year}"


def jalali_str_to_gregorian(date_str):
    jy, jm, jd = [int(p) for p in date_str.split('-')]
    return jdatetime.date(jy, jm, jd).togregorian()


def gregorian_to_jalali_param(g_date):
    j = jdatetime.date.fromgregorian(date=g_date)
    return f"{j.year:04d}-{j.month:02d}-{j.day:02d}"


def home(request):
    cities = city.objects.all().order_by('name')
    return render(request, 'index.html', {'cities': cities})

def dashboard(request):
    cities = city.objects.all().order_by('name')
    return render(request, 'dashboard.html', {'cities': cities})

def vacancy_list(request):
    date_str = request.GET.get('date', '')
    try:
        selected_date = jalali_str_to_gregorian(date_str) if date_str else date_cls.today()
    except (ValueError, TypeError):
        selected_date = date_cls.today()
    units = RoomUnit.objects.filter(
        availabilities__date=selected_date,
        availabilities__status='available',
        venue__is_active=True
    ).select_related('venue', 'venue__city')

    data = [
        {
            "city": u.venue.city.name,
            "venue": u.venue.name,
            "unitType": u.unit_type,
        }
        for u in units
    ]
    return JsonResponse({"results": data})

def city_results(request):
    city_name = request.GET.get('city', '')
    date_str = request.GET.get('date', '')

    try:
        selected_date = jalali_str_to_gregorian(date_str) if date_str else date_cls.today()
    except (ValueError, TypeError):
        selected_date = date_cls.today()

    venues = Venue.objects.filter(city__name=city_name, is_active=True).prefetch_related('units')

    city_obj = city.objects.filter(name=city_name).first()
    slides = city_obj.slides.all() if city_obj else []

    for venue in venues:
        for unit in venue.units.all():
            avail = unit.availabilities.filter(date=selected_date).first()
            if avail:
                unit.date_status = avail.status
                unit.date_status_label = avail.get_status_display()
            else:
                unit.date_status = 'undefined'
                unit.date_status_label = 'تعریف‌نشده'

    context = {
        'city_name': city_name,
        'venues': venues,
        'slides': slides,
        'selected_date_fa': to_jalali_display(selected_date),
        'prev_date_param': gregorian_to_jalali_param(selected_date - timedelta(days=1)),
        'next_date_param': gregorian_to_jalali_param(selected_date + timedelta(days=1)),
    }
    return render(request, 'city.html', context)