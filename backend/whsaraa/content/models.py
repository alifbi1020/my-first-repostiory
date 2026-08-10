from django.db import models


class Announcement(models.Model):
    AUDIENCE_CHOICES = [
        ('portal', 'پرتال (عمومی)'),
        ('members', 'اعضا (فقط کاربران لاگین‌کرده)'),
        ('managers', 'مدیران (فقط ادمین)'),
    ]
    title = models.CharField(max_length=200, verbose_name="عنوان")
    body = models.TextField(verbose_name="متن")
    audience = models.CharField(
        max_length=20,
        choices=AUDIENCE_CHOICES,
        default='portal',
        verbose_name="مخاطب",
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "اطلاعیه"
        verbose_name_plural = "اطلاعیه‌ها"
