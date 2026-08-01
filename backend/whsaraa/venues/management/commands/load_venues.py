from django.core.management.base import BaseCommand
from venues.models import *

DATA = [
    {"venue": "زائرسرای مشهد", "city": "مشهد", "unit_type": "سوئیت دونفره", "room_type": "بدون اتاق خواب", "price": 3856000},
    {"venue": "زائرسرای مشهد", "city": "مشهد", "unit_type": "سوئیت سه نفره", "room_type": "بدون اتاق خواب", "price": 5392000},
    {"venue": "زائرسرای مشهد", "city": "مشهد", "unit_type": "سوئیت چهار نفره", "room_type": "بدون اتاق خواب", "price": 5840000},
    {"venue": "زائرسرای مشهد", "city": "مشهد", "unit_type": "آپارتمان", "room_type": "تک خواب", "price": 6960000},
    {"venue": "زائرسرای مشهد", "city": "مشهد", "unit_type": "آپارتمان", "room_type": "تک خواب نرخ کانون جهان گردی", "price": 12500000},
    {"venue": "زائرسرای مشهد", "city": "مشهد", "unit_type": "آپارتمان", "room_type": "دو خواب", "price": 8128000},
    {"venue": "پردیس مشهد", "city": "مشهد", "unit_type": "سوئیت سه نفره", "room_type": "بدون اتاق خواب", "price": 2560000},
    {"venue": "پردیس مشهد", "city": "مشهد", "unit_type": "آپارتمان", "room_type": "تک خواب", "price": 3920000},
    {"venue": "پردیس مشهد", "city": "مشهد", "unit_type": "آپارتمان", "room_type": "دو خواب", "price": 5570000},
    {"venue": "استراحتگاه اردبیل", "city": "اردبیل", "unit_type": "سوئیت چهار نفره", "room_type": "تک خواب", "price": 7296000},
    {"venue": "استراحتگاه یزد", "city": "یزد", "unit_type": "سوئیت سه نفره", "room_type": "بدون اتاق خواب", "price": 4640000},
    {"venue": "استراحتگاه یزد", "city": "یزد", "unit_type": "سوئیت چهار نفره", "room_type": "بدون اتاق خواب", "price": 5280000},
    {"venue": "استراحتگاه یزد", "city": "یزد", "unit_type": "سوئیت پنج نفره", "room_type": "", "price": 6096000},
    {"venue": "استراحتگاه اصفهان", "city": "اصفهان", "unit_type": "سوئیت سه نفره", "room_type": "", "price": 3600000},
    {"venue": "استراحتگاه اصفهان", "city": "اصفهان", "unit_type": "سوئیت چهار نفره", "room_type": "بدون اتاق خواب", "price": 4640000},
    {"venue": "استراحتگاه اصفهان", "city": "اصفهان", "unit_type": "سوئیت پنج نفره", "room_type": "", "price": 5280000},
    {"venue": "استراحتگاه پرند", "city": "پرند", "unit_type": "پنج نفره", "room_type": "دو خواب", "price": 12500000},
    {"venue": "خانه کارگر تبریز", "city": "تبریز", "unit_type": "چهار نفره", "room_type": "بدون خواب", "price": 5060000},
    {"venue": "خانه کارگر تبریز", "city": "تبریز", "unit_type": "چهار نفره", "room_type": "تک خواب", "price": 6560000},
    {"venue": "شهید فاضل سرعین", "city": "سرعین", "unit_type": "چهار نفره", "room_type": "تک خواب", "price": 5456000},
    {"venue": "شهید فاضل سرعین", "city": "سرعین", "unit_type": "چهار نفره دوبلکس", "room_type": "تک خواب", "price": 5392000},
    {"venue": "شهید فاضل سرعین", "city": "سرعین", "unit_type": "پنج نفره دوبلکس", "room_type": "دو خواب", "price": 5696000},
    {"venue": "کاراسرعین", "city": "سرعین", "unit_type": "چهار نفره", "room_type": "تک خواب", "price": 7312000},
    {"venue": "کاراسرعین", "city": "سرعین", "unit_type": "پنج نفره", "room_type": "دو خواب", "price": 8176000},
    {"venue": "استراحتگاه قشم", "city": "قشم", "unit_type": "کوچک چهار نفره", "room_type": "تک خواب", "price": 6272000},
    {"venue": "استراحتگاه قشم", "city": "قشم", "unit_type": "بزرگ چهار نفره", "room_type": "تک خواب", "price": 6800000},
    {"venue": "استراحتگاه قشم", "city": "قشم", "unit_type": "کوچک پنج نفره", "room_type": "دو خواب", "price": 7440000},
    {"venue": "استراحتگاه قشم", "city": "قشم", "unit_type": "بزرگ شش نفره", "room_type": "دو خواب", "price": 8176000},
    {"venue": "استراحتگاه گرگان", "city": "گرگان", "unit_type": "سوئیت سه نفره", "room_type": "بدون اتاق خواب", "price": 3850000},
    {"venue": "استراحتگاه گرگان", "city": "گرگان", "unit_type": "آپارتمان چهارنفره", "room_type": "تک خواب", "price": 5650000},
    {"venue": "استراحتگاه گرگان", "city": "گرگان", "unit_type": "آپارتمان پنج نفره", "room_type": "دو خواب", "price": 6350000},
    {"venue": "مجتمع شهید امامی چمخاله (ردیف خزر)", "city": "چمخاله", "unit_type": "30 متری یک نفره", "room_type": "--", "price": 4800000},
    {"venue": "مجتمع شهید امامی چمخاله(ردیف یاس و زنبق)", "city": "چمخاله", "unit_type": "28 متری یک نفره (یاس و زنبق)", "room_type": "", "price": 4512000},
    {"venue": "مجتمع شهید امامی چمخاله(ردیف یاس و زنبق)", "city": "چمخاله", "unit_type": "20 متری ردیف شقایق یک نفره(طبقه 3)", "room_type": "", "price": 3105000},
    {"venue": "مجتمع شهید امامی چمخاله(ردیف یاس و زنبق)", "city": "چمخاله", "unit_type": "20 متری ردیف شقایق یک نفره(طبقه 1 یا 2)", "room_type": "", "price": 3105000},
    {"venue": "مجتمع شهید امامی چمخاله(ردیف یاس و زنبق)", "city": "چمخاله", "unit_type": "30 متری ردیف شقایق یک نفره(طبقه 3)", "room_type": "", "price": 4720000},
    {"venue": "مجتمع شهید امامی چمخاله(ردیف یاس و زنبق)", "city": "چمخاله", "unit_type": "30 متری ردیف شقایق یک نفره(طبقه 1 یا 2)", "room_type": "", "price": 4720000},
    {"venue": "مجتمع شهید امامی چمخاله(ردیف یاس و زنبق)", "city": "چمخاله", "unit_type": "38 متری ردیف شقایق یک نفره(طبقه 3)", "room_type": "", "price": 5312000},
    {"venue": "مجتمع شهید امامی چمخاله(ردیف یاس و زنبق)", "city": "چمخاله", "unit_type": "38 متری ردیف شقایق یک نفره(طبقه 1 یا 2)", "room_type": "", "price": 5312000},
    {"venue": "مجتمع شهید امامی چمخاله(ردیف یاس و زنبق)", "city": "چمخاله", "unit_type": "55 متری ردیف شقایق یک نفره(طبقه 3)", "room_type": "", "price": 6928000},
    {"venue": "مجتمع شهید امامی چمخاله(ردیف یاس و زنبق)", "city": "چمخاله", "unit_type": "55 متری ردیف شقایق یک نفره(طبقه 1 یا 2)", "room_type": "", "price": 6928000},
]

class Command(BaseCommand):
    help = "وارد کردن مهمان سراها و واحد های اقامتی از دیتای اولیه"

    def handle(self, *args, **options):
        new_venues = 0
        new_units = 0

        for row in DATA:
            city_obj, _ = city.objects.get_or_create(name = row["city"])
            venue_obj, venue_created = Venue.objects.get_or_create(
                name = row["venue"], city=city_obj
            )
            if venue_created :
                new_venues += 1
            _, unit_created = RoomUnit.objects.get_or_create(
                venue = venue_obj,
                unit_type = row["unit_type"],
                room_type = row["room_type"],
                defaults={"price_per_night": row["price"]},
            )
            if unit_created:
                new_units += 1
        self.stdout.write(self.style.SUCCESS(
            f"{new_venues} مهمان‌سرای جدید و {new_units} واحد اقامتی جدید اضافه شد."
        ))