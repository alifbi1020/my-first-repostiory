from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta
from venues.models import RoomUnit


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('confirmed', 'تایید شده'),
        ('cancelled', 'لغو شده'),
        ('expired', 'منقضی شده'),  # کامنت: وضعیت جدید برای رزروهای ۱۰ دقیقه‌ای که پرداخت نشدند
    ]
    PAYMENT_TYPE_CHOICES = [
        ('wallet', 'کیف پول'),
        ('gateway', 'درگاه پرداخت'),
        ('temporary', 'رزرو موقت'),  # کامنت: نوع پرداخت برای رزرو موقت
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="کاربر",
    )
    room_unit = models.ForeignKey(
        RoomUnit,
        on_delete=models.PROTECT,
        related_name='reservations',
        verbose_name="واحد اقامتی",
    )
    date = models.DateField(verbose_name="تاریخ اقامت")
    checkout_date = models.DateField(verbose_name="تاریخ خروج", blank=True, null=True)
    price_at_booking = models.PositiveBigIntegerField(verbose_name="قیمت ثبت‌شده (ریال)")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت"
    )
    payment_type = models.CharField(  # کامنت: ذخیره نوع روش پرداخت انتخابی کاربر
        max_length=20, choices=PAYMENT_TYPE_CHOICES, blank=True, null=True, verbose_name="نوع پرداخت"
    )
    payment_deadline = models.DateTimeField(  # کامنت: زمان انقضای ۱۰ دقیقه‌ای برای رزرو موقت
        blank=True, null=True, verbose_name="مهلت پرداخت"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")

    def __str__(self):
        return f"{self.user} - {self.room_unit} - {self.date}"

    def is_expired(self):
        """کامنت: بررسی می‌کند آیا زمان رزرو موقت منقضی شده است"""
        if self.status == 'pending' and self.payment_deadline:
            return timezone.now() > self.payment_deadline
        return False

    class Meta:
        unique_together = ('room_unit', 'date')
        verbose_name = "رزرو"
        verbose_name_plural = "رزروها"
        ordering = ['-created_at']  # کامنت: نمایش جدیدترین رزروها اول
