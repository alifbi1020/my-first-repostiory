from django.contrib import admin
from .models import city, Venue, RoomUnit, Availability, CitySlide

admin.site.site_header = "پنل مدیریت سامانه سرا"
admin.site.site_title = "سامانه سرا"
admin.site.index_title = "مدیریت سامانه"

class AvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 1
class CitySlideInline(admin.TabularInline):
    model = CitySlide
    extra = 1


@admin.register(city)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [CitySlideInline]
class RoomUnitInline(admin.TabularInline):
    model = RoomUnit
    extra = 1
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name","city","is_active")
    list_filter = ("city", "is_active")
    inlines = [RoomUnitInline]
@admin.register(RoomUnit)
class RoomUnitAdmin(admin.ModelAdmin):
    list_display = ('venue', 'unit_type', 'room_type', 'status', 'price_per_night')
    list_filter = ('status', 'venue__city')
    inlines = [AvailabilityInline]