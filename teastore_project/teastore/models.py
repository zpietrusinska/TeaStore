from django.conf import settings
from django.db import models


class TeaCategory(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name="Nazwa")
    description = models.TextField(blank=True, verbose_name="Opis")

    def __str__(self):
        return self.name


class Origin(models.Model):
    country_code = models.CharField(max_length=2, verbose_name="Kod kraju")
    region = models.CharField(max_length=60, verbose_name="Region")
    farm_name = models.CharField(max_length=80, blank=True, verbose_name="Plantacja")
    is_organic = models.BooleanField(default=False, verbose_name="Bio")

    def __str__(self):
        base = f"{self.country_code}-{self.region}"
        return f"{base} ({self.farm_name})" if self.farm_name else base


class TeaType(models.TextChoices):
    BLACK = "black", "Czarna"
    GREEN = "green", "Zielona"
    WHITE = "white", "Biala"
    OOLONG = "oolong", "Oolong"
    HERBAL = "herbal", "Ziolowa"
    PUERH = "puerh", "Puerh"


class CaffeineLevel(models.TextChoices):
    NONE = "none", "Bez kofeiny"
    LOW = "low", "Niska"
    MEDIUM = "medium", "Srednia"
    HIGH = "high", "Wysoka"


class Tea(models.Model):
    name = models.CharField(max_length=120, verbose_name="Nazwa")
    description = models.TextField(blank=True, verbose_name="Opis")
    category = models.ForeignKey(TeaCategory, on_delete=models.PROTECT, verbose_name="Kategoria")
    origin = models.ForeignKey(
        Origin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Pochodzenie",
    )
    tea_type = models.CharField(max_length=10, choices=TeaType.choices, verbose_name="Typ herbaty")
    caffeine_level = models.CharField(
        max_length=10, choices=CaffeineLevel.choices, verbose_name="Poziom kofeiny"
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Cena")
    stock_qty = models.PositiveIntegerField(default=0, verbose_name="Stan magazynowy")
    is_active = models.BooleanField(default=True, verbose_name="Aktywna")
    added_at = models.DateField(auto_now_add=True, verbose_name="Data dodania")

    def __str__(self):
        return self.name


class OrderStatus(models.TextChoices):
    NEW = "new", "Nowe"
    PAID = "paid", "Oplacone"
    SHIPPED = "shipped", "Wyslane"
    CANCELED = "canceled", "Anulowane"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Uzytkownik",
    )
    status = models.CharField(
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.NEW,
        verbose_name="Status",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    delivery_date = models.DateField(null=True, blank=True, verbose_name="Data dostawy")
    note = models.TextField(blank=True, verbose_name="Notatka")

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name="Zamowienie"
    )
    tea = models.ForeignKey(Tea, on_delete=models.PROTECT, verbose_name="Herbata")
    quantity = models.PositiveIntegerField(verbose_name="Ilosc")
    unit_price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Cena jednostkowa"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["order", "tea"], name="unique_order_item")
        ]

    def __str__(self):
        return f"{self.order_id} - {self.tea}"
