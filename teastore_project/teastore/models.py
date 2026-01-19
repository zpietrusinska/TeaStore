from django.conf import settings
from django.db import models


class TeaCategory(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Origin(models.Model):
    country_code = models.CharField(max_length=2)
    region = models.CharField(max_length=60)
    farm_name = models.CharField(max_length=80, blank=True)
    is_organic = models.BooleanField(default=False)

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
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    category = models.ForeignKey(TeaCategory, on_delete=models.PROTECT)
    origin = models.ForeignKey(Origin, on_delete=models.SET_NULL, null=True, blank=True)
    tea_type = models.CharField(max_length=10, choices=TeaType.choices)
    caffeine_level = models.CharField(max_length=10, choices=CaffeineLevel.choices)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock_qty = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class OrderStatus(models.TextChoices):
    NEW = "new", "Nowe"
    PAID = "paid", "Oplacone"
    SHIPPED = "shipped", "Wyslane"
    CANCELED = "canceled", "Anulowane"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(null=True, blank=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    tea = models.ForeignKey(Tea, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["order", "tea"], name="unique_order_item")
        ]

    def __str__(self):
        return f"{self.order_id} - {self.tea}"
