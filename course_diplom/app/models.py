from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
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

# CONTACT_CHOICES = (
#     ('cell_phone', 'Номер телефона'),
#     ('adress', "Почтовый адрес"),
# )

default_description = 'Узнать характеристики товара можно у вашего менеджера'


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="E-mail", unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=30, blank=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=30, blank=True)
    middle_name = models.CharField(verbose_name="Отчество", max_length=30, blank=True)
    company = models.CharField(verbose_name='Компания', max_length=30, blank=True)
    position = models.CharField(verbose_name='Должность', max_length=30, blank=True)
    type = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPE_CHOICES, max_length=5, default='buyer')

    is_staff = models.BooleanField(('staff status'), default=False,
                                   help_text=('Designates whether the user can log into this admin site.'), )
    is_active = models.BooleanField(('active'), default=True, help_text=(
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.'
    ),
                                    )
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"
        ordering = ('email',)

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Список категорий"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка на файл с товарами', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Статус приёма заказов', default=True)
    category = models.ManyToManyField(Category, verbose_name="Категория")

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"
        ordering = ('-name',)

    def __str__(self):
        return self.name



class Item(models.Model):
    category = models.ManyToManyField(Category, verbose_name='Категория товаров', related_name='products', blank=True)
    name = models.CharField(max_length=80, verbose_name='Название')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = "Список товаров"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ItemInfo(models.Model):
    item = models.ForeignKey(Item, verbose_name='Товар', blank=True, on_delete=models.CASCADE)
    model = models.CharField(max_length=80, verbose_name='Модель', blank=True)
    description = models.CharField(max_length=100, verbose_name='Описание товара', default=default_description)
    external_id = models.PositiveIntegerField(verbose_name='Внешний ИД')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='item_infos', blank=True,
                             on_delete=models.CASCADE)
    in_stock_qty = models.PositiveIntegerField(verbose_name='Количество товара',default=0)

    class Meta:
        verbose_name = 'Информация о товаре'
        verbose_name_plural = "Информации о товаре"
        ordering = ('-item',)

        # задаёт ограничение уникальности для данных полей.
        constraints = [
            models.UniqueConstraint(fields=['item', 'shop', 'external_id'], name='unique_item_info')
        ]

    def __str__(self):
        return self.item.name


class Parameter(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')

    class Meta:
        verbose_name = 'Имя параметра'
        verbose_name_plural = "Список всех параметров"
        ordering = ('name',)

    def __str__(self):
        return self.name


class ItemParameter(models.Model):
    item = models.ForeignKey(ItemInfo, verbose_name='Информация о продукте', related_name='item_parameters',
                             blank=True, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, verbose_name='Параметр', related_name='product_parameters', blank=True,
                                  on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=100)

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = "Список параметров товаров"


class Order(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', related_name='orders', blank=True,
                             on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(verbose_name='Статус', choices=STATE_CHOICES, max_length=15)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Список заказ"
        ordering = ('-date',)

    def __str__(self):
        return str(self.date)


class OrderInfo(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='ordered_items', blank=True,
                              on_delete=models.CASCADE)
    item = models.ForeignKey(ItemInfo, verbose_name='Информация о продукте', related_name='ordered_items', blank=True,
                             on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Заказанная позиция'
        verbose_name_plural = "Список заказанных позиций"


class Contact(models.Model):
    user = models.ManyToManyField(CustomUser, verbose_name='Пользователь')
    adress = models.CharField(verbose_name='Адрес', default='', max_length=10)
    phone = models.CharField(verbose_name='Телефон', default='+7(900)123-45-67', max_length=30, unique=True)

    class Meta:
        verbose_name = "Контактные данные"
        verbose_name_plural = "Контактные данные"

    def __str__(self):
        return str(self.pk)
