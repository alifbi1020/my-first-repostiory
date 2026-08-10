from django.conf import settings
from django.db import models
from venues.models import RoomUnit


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('confirmed', 'تایید شده'),
        ('cancelled', 'لغو شده'),
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
    price_at_booking = models.PositiveBigIntegerField(verbose_name="قیمت ثبت‌شده (ریال)")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")

    def __str__(self):
        return f"{self.user} - {self.room_unit} - {self.date}"

    class Meta:
        unique_together = ('room_unit', 'date')
        verbose_name = "رزرو"
        verbose_name_plural = "رزروها"
