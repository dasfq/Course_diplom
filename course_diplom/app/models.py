from django.db import models
from django.contrib.auth.models import User
from .managers import CustomUserManager

STATE_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)

USER_TYPE_CHOICES = (
    ('shop', 'Магазин'),
    ('buyer', 'Покупатель'),
)


class CustomUser(User):
    middle_name = models.CharField(max_length=30, blank=True)
    company = models.CharField(verbose_name='Компания', max_length=30, blank=True)
    position = models.CharField(verbose_name='Должность', max_length=30, blank=True)
    type = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPE_CHOICES, max_length=5, default='buyer')
    USERNAME_FIELD = 'email'
    object = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"
        ordering = ('email',)


class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Статус приёма заказов', default=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Список категорий"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ManyToManyField(Category, verbose_name='Категория товаров', related_name='products', blank=True)
    # category = models.ForeignKey(Category, verbose_name='Категория', , on_delete=models.CASCADE)
    name = models.CharField(max_length=80, verbose_name='Название')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = "Список товаров"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ItemInfo(models.Model):
    item = models.ForeignKey(Item, verbose_name='Товар', related_name='item_infos', blank=True, on_delete=models.CASCADE)
    model = models.CharField(max_length=80, verbose_name='Модель', blank=True)
    external_id = models.PositiveIntegerField(verbose_name='Внешний ИД')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='item_infos', blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Информация о товаре'
        verbose_name_plural = "Информации о товаре"
        ordering = ('-item',)

    def __str__(self):
        return self.name

class Parameter(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')

    class Meta:
        verbose_name = 'Имя параметра'
        verbose_name_plural = "Список имен параметров"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ItemParameter(models.Model):
    item = models.ForeignKey(ItemInfo, verbose_name='Информация о продукте', related_name='product_parameters', blank=True, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, verbose_name='Параметр', related_name='product_parameters', blank=True, on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=100)

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = "Список параметров"


class Order(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', related_name='orders', blank=True, on_delete=models.CASCADE)
    date  = models.DateTimeField(auto_now_add=True)
    status = models.CharField(verbose_name='Статус', choices=STATE_CHOICES, max_length=15)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Список заказ"
        ordering = ('-date',)

    def __str__(self):
        return str(self.date)

class OrderInfo(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='ordered_items', blank=True, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemInfo, verbose_name='Информация о продукте', related_name='ordered_items', blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Заказанная позиция'
        verbose_name_plural = "Список заказанных позиций"
