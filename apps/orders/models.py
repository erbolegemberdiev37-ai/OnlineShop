from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Новый"),
        ("processing", "В обработке"),
        ("shipped", "Отправлен"),
        ("delivered", "Доставлен"),
        ("canceled", "Отменён"),
    ]
    DELIVERY_CHOICES = [
        ("pickup", "Самовывоз"),
        ("courier", "Курьер"),
    ]
    PAYMENT_CHOICES = [
        ("cash", "Наличные"),
        ("card", "Картой при получении"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="Пользователь",
    )
    full_name = models.CharField("ФИО", max_length=255)
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email")
    address = models.CharField("Адрес доставки", max_length=500)
    comment = models.TextField("Комментарий", blank=True)
    delivery_method = models.CharField(
        "Доставка", max_length=20, choices=DELIVERY_CHOICES, default="courier"
    )
    payment_method = models.CharField(
        "Оплата", max_length=20, choices=PAYMENT_CHOICES, default="cash"
    )
    status = models.CharField(
        "Статус", max_length=20, choices=STATUS_CHOICES, default="new"
    )
    total = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.pk} — {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Заказ",
    )
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Товар",
    )
    product_name = models.CharField("Название товара", max_length=255)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity
