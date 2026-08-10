import jdatetime
from datetime import date as date_cls, timedelta
from django.shortcuts import render
from .models import Venue, city, RoomUnit, Availability
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from content.models import Announcement

FA_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
JALALI_MONTHS = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
                  "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]


def to_jalali_display(g_date):
    j = jdatetime.date.fromgregorian(date=g_date)
    day = str(j.day).translate(FA_DIGITS)
    month = JALALI_MONTHS[j.month - 1]
    year = str(j.year).translate(FA_DIGITS)
    return f"{day} {month} {year}"


def to_jalali_short(g_date):
    j = jdatetime.date.fromgregorian(date=g_date)
    y = str(j.year).translate(FA_DIGITS)
    m = str(j.month).zfill(2).translate(FA_DIGITS)
    d = str(j.day).zfill(2).translate(FA_DIGITS)
    return f"{y}/{m}/{d}"


def jalali_str_to_gregorian(date_str):
    jy, jm, jd = [int(p) for p in date_str.split('-')]
    return jdatetime.date(jy, jm, jd).togregorian()


def gregorian_to_jalali_param(g_date):
    j = jdatetime.date.fromgregorian(date=g_date)
    return f"{j.year:04d}-{j.month:02d}-{j.day:02d}"


def get_visible_announcements(request):
    audiences = ['portal', 'members'] if request.user.is_authenticated else ['portal']
    announcements = Announcement.objects.filter(
        is_active=True, audience__in=audiences
    ).order_by('-created_at')
    for a in announcements:
        a.date_short = to_jalali_short(a.created_at)
        a.date_full = f"{to_jalali_display(a.created_at)} ساعت {a.created_at.strftime('%H:%M').translate(FA_DIGITS)}"
    return announcements


def home(request):
    cities = city.objects.all().order_by('name')
    featured_venues = Venue.objects.filter(is_active=True).select_related('city')
    return render(request, 'index.html', {
        'cities': cities,
        'featured_venues': featured_venues,
        'announcements': get_visible_announcements(request),
        'user': request.user,
    })

def dashboard(request):
    cities = city.objects.all().order_by('name')
    return render(request, 'dashboard.html', {'cities': cities})

def dashboard_view(request):
    cities = city.objects.all().order_by('name')
    return render(request, 'dashboard.html', {
        'cities': cities,
        'announcements': get_visible_announcements(request),
        'user': request.user,
    })

def vacancy_list(request):
    date_str = request.GET.get('date', '')

    base_qs = Availability.objects.filter(
        status='available',
        room_unit__venue__is_active=True,
    ).select_related('room_unit', 'room_unit__venue', 'room_unit__venue__city')

    if date_str:
        # A specific date was picked in the calendar: show only that day.
        try:
            selected_date = jalali_str_to_gregorian(date_str)
        except (ValueError, TypeError):
            selected_date = date_cls.today()
        availabilities = base_qs.filter(date=selected_date).order_by(
            'room_unit__venue__city__name', 'room_unit__venue__name'
        )
        response_date = gregorian_to_jalali_param(selected_date)
    else:
        # No date picked: show every open date we have, grouped by city.
        availabilities = base_qs.order_by(
            'date', 'room_unit__venue__city__name', 'room_unit__venue__name'
        )
        response_date = ''

    grouped = {}
    for a in availabilities:
        u = a.room_unit
        city_name = u.venue.city.name
        grouped.setdefault(city_name, []).append({
            "venue": u.venue.name,
            "unitType": u.unit_type,
            "roomType": u.room_type,
            "date": gregorian_to_jalali_param(a.date),
            "dateDisplay": to_jalali_display(a.date),
        })

    results = [
        {"city": city_name, "count": len(items), "units": items}
        for city_name, items in grouped.items()
    ]

    return JsonResponse({
        "date": response_date,
        "results": results,
    })

def build_week_strip(selected_date):
    FA_WEEKDAYS = ['شنبه','یکشنبه','دوشنبه','سه‌شنبه','چهارشنبه','پنج‌شنبه','جمعه']
    strip = []
    for delta in range(-3, 4):
        g_date = selected_date + timedelta(days=delta)
        j = jdatetime.date.fromgregorian(date=g_date)
        weekday_index = (g_date.weekday() + 2) % 7
        strip.append({
            'weekday': FA_WEEKDAYS[weekday_index],
            'day_fa': str(j.day).translate(FA_DIGITS),
            'month_fa': str(j.month).translate(FA_DIGITS),
            'date_param': f"{j.year}-{j.month:02d}-{j.day:02d}",
            'is_selected': delta == 0,
        })
    prev_week = selected_date - timedelta(days=7)
    next_week = selected_date + timedelta(days=7)
    j_prev = jdatetime.date.fromgregorian(date=prev_week)
    j_next = jdatetime.date.fromgregorian(date=next_week)
    return (
        strip,
        f"{j_prev.year}-{j_prev.month:02d}-{j_prev.day:02d}",
        f"{j_next.year}-{j_next.month:02d}-{j_next.day:02d}"
    )

def city_results(request):

    city_name = request.GET.get('city', '')
    date_str = request.GET.get('date', '')

    try:
        selected_date = jalali_str_to_gregorian(date_str) if date_str else date_cls.today()
        week_strip, week_prev_param, week_next_param = build_week_strip(selected_date)
    except (ValueError, TypeError):
        selected_date = date_cls.today()

    venues = Venue.objects.filter(city__name=city_name, is_active=True).prefetch_related('units')

    city_obj = city.objects.filter(name=city_name).first()
    city_rules = city_obj.rules if city_obj else ''
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
        'city_rules': city_rules,
        'city_obj': city_obj,
        'announcements': get_visible_announcements(request),
        'week_strip': week_strip,
        'week_prev_param': week_prev_param,
        'week_next_param': week_next_param,
        'user': request.user,
        'selected_date_fa': to_jalali_display(selected_date),
        'selected_date_param': gregorian_to_jalali_param(selected_date),
        'prev_date_param': gregorian_to_jalali_param(selected_date - timedelta(days=1)),
        'next_date_param': gregorian_to_jalali_param(selected_date + timedelta(days=1)),
    }
    return render(request, 'city.html', context)