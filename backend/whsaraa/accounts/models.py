from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class user(AbstractUser):
    national_code = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'کد ملی باید 10 رقم باشد.')],
        verbose_name= "کد ملی"
    )
    membership_code = models.CharField(
        max_length= 14,
        unique=True,
        validators=[RegexValidator(r'^\d{14}$', 'کد عضویت باید 14 رقم باشد.')],
        verbose_name= "کد عضویت"
    )
    phone_number = models.CharField(
        max_length= 11,
        unique= True,
        validators=[RegexValidator(r'^\d{11}$', 'شماره همراه باید 11 رقم باشد.')],
        verbose_name= "شماره همراه"
    )
    membership_expiry = models.DateField(null=True, blank=True, verbose_name="اعتبار عضویت")
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name="تصویر پروفایل")
    USERNAME_FIELD = 'membership_code'
    REQUIRED_FIELDS = ['username', 'national_code', 'phone_number']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.membership_code})"
