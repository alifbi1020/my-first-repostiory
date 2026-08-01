from django.db import models

class city(models.Model):
    name = models.CharField(max_length= 50, unique=True, verbose_name="نام شهر")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهر ها"
class Venue(models.Model):
    name = models.CharField(max_length=150, verbose_name="نام مهمان‌سراها")
    city = models.ForeignKey(city, on_delete=models.PROTECT, related_name='venues', verbose_name="شهرها")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    cover_image = models.ImageField(upload_to='venues/', blank=True, null=True, verbose_name="تصویر")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    def __str__(self):
        return f"{self.name} ({self.city})"
    class Meta:
        verbose_name = "مهمان سرا"
        verbose_name_plural = "مهمان سراها"
class RoomUnit(models.Model):
    STATUS_CHOICES = [
        ('undefined', 'تعریف نشده'),
        ('available', 'ظرفیت خالی'),
        ('full', 'ظرفیت پر'),
    ]
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='units', verbose_name="مهمان سرا")
    unit_type = models.CharField(max_length=100, verbose_name="نوع واحد")
    room_type = models.CharField(max_length=100, blank=True, verbose_name="نوع استراحتگاه")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='undefined',
        verbose_name="وضعیت"
    )
    price_per_night = models.PositiveBigIntegerField(verbose_name="قیمت هر شب (ریال)")

    def __str__(self):
        return f"{self.venue.name} - {self.unit_type}"

    class Meta:
        verbose_name = "واحد اقامتی"
        verbose_name_plural = "واحد های اقامتی"
class Availability(models.Model): 
    room_unit = models.ForeignKey(RoomUnit, on_delete=models.CASCADE, related_name='availabilities', verbose_name="واحد اقامتی")
    date = models.DateField(verbose_name="تاریخ")
    status = models.CharField(
        max_length=20,
        choices=RoomUnit.STATUS_CHOICES,
        default='undefined',
        verbose_name='وضعیت'
    )
    def __str__(self):
        return f"{self.room_unit} - {self.date} - {self.get_status_display()}"
    class Meta:
        unique_together = ('room_unit', 'date')
        verbose_name = "ظرفیت روزانه"
        verbose_name_plural = "ظرفیت‌های روزانه"