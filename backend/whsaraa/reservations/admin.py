from django.contrib import admin
from django.utils import timezone
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room_unit', 'date', 'status', 'payment_type', 'price_at_booking', 'created_at', 'payment_deadline', 'is_expired_display')
    list_filter = ('status', 'payment_type', 'date')
    search_fields = ('user__first_name', 'user__last_name', 'room_unit__venue__name')
    
    def is_expired_display(self, obj):
        """کامنت: نمایش وضعیت انقضا در پنل ادمین با آیکون بله/خیر"""
        return obj.is_expired()
    is_expired_display.short_description = "آیا منقضی شده؟"
    is_expired_display.boolean = True
    
    actions = ['confirm_reservation', 'cancel_reservation', 'expire_reservations']
    
    def confirm_reservation(self, request, queryset):
        """کامنت: اکشن دستی برای تایید رزروها از پنل ادمین"""
        updated = queryset.filter(status='pending').update(status='confirmed', payment_deadline=None)
        self.message_user(request, f"{updated} رزرو تایید شد.")
    confirm_reservation.short_description = "تایید رزروهای انتخاب‌شده"
    
    def cancel_reservation(self, request, queryset):
        """کامنت: اکشن دستی برای لغو رزروها از پنل ادمین"""
        updated = queryset.filter(status__in=['pending', 'confirmed']).update(status='cancelled')
        self.message_user(request, f"{updated} رزرو لغو شد.")
    cancel_reservation.short_description = "لغو رزروهای انتخاب‌شده"
    
    def expire_reservations(self, request, queryset):
        """کامنت: بررسی و انقضای رزروهای موقت که زمانشان گذشته است"""
        count = 0
        for res in queryset.filter(status='pending', payment_deadline__isnull=False):
            if res.is_expired():
                res.status = 'expired'
                res.save(update_fields=['status'])
                count += 1
        self.message_user(request, f"{count} رزرو منقضی شد.")
    expire_reservations.short_description = "انقضای رزروهای منقضی‌شده"
