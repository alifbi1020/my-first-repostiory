from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room_unit', 'date', 'status', 'price_at_booking', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('user__first_name', 'user__last_name', 'room_unit__venue__name')
