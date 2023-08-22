from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    """Базовая модель добавляющая поля используемые во всех моделях"""

    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Создатель модели')
    description = models.CharField(max_length=2048, verbose_name='Описание')
    is_public = models.BooleanField(default=True, verbose_name='Публикация')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    location = models.CharField(max_length=128, verbose_name='Локация', null=True, blank=True)  # временное решение
    # проработать нужно добавление карты, отображение города
    slug = models.SlugField(blank=True, null=True, db_index=True, unique=True, verbose_name='Ссылка')

    class Meta:
        abstract = True


# class BassForeignModel(models.Model):
#     slug = models.SlugField(blank=True, null=True, db_index=True, unique=True, verbose_name='Ссылка')
#
#     class Meta:
#         abstract = True


class MarkTransport(models.Model):
    """ForeignKey. Марка трансопрта"""

    mark_tr = models.CharField(max_length=64, verbose_name='Марка')
    slug = models.SlugField(blank=True, null=True, db_index=True, unique=True, verbose_name='Ссылка')

    def __str__(self):
        return f'{self.mark_tr}'

    class Meta:
        verbose_name = "Марка"
        verbose_name_plural = "Марки"


class ModelTransport(models.Model):
    """ForeignKey. Модель транспорта"""

    model_tr = models.CharField(max_length=64, verbose_name='Модель')
    slug = models.SlugField(blank=True, null=True, db_index=True, unique=True, verbose_name='Ссылка')

    def __str__(self):
        return f'{self.model_tr}'

    class Meta:
        verbose_name = "Модель"
        verbose_name_plural = "Модели"


class ThemeEvent(models.Model):
    """ForeignKey. Тематика мероприятия"""

    theme = models.CharField(max_length=64, verbose_name='Тематика')
    slug = models.SlugField(blank=True, null=True, db_index=True, unique=True, verbose_name='Ссылка')

    def __str__(self):
        return f'{self.theme}'

    class Meta:
        verbose_name = "Тематика"
        verbose_name_plural = "Тематики"


class VarietyVisa(models.Model):
    """ForeignKey. Вид визы"""

    variety = models.CharField(max_length=64, verbose_name='Вид визы')
    slug = models.SlugField(blank=True, null=True, db_index=True, unique=True, verbose_name='Ссылка')

    def __str__(self):
        return f'{self.variety}'

    class Meta:
        verbose_name = "Вид визы"
        verbose_name_plural = "Виды виз"


class EventPoster(models.Model):
    """Модель мероприятий, афиш"""

    date = models.DateTimeField(verbose_name='Дата и время')
    themes = models.ForeignKey(ThemeEvent, on_delete=models.PROTECT, verbose_name='Тематика')
    photo = models.ImageField(upload_to='photos/event', verbose_name='Фото', null=True, blank=True)
    # add_photo = 'later'


class Visa(models.Model):
    """Визы, и прочие документы"""

    variety = models.CharField(max_length=128, verbose_name='Вид визы')  # choice
    validity = models.CharField(max_length=128, verbose_name='Срок визы')  # choice
    photo = models.ImageField(upload_to='photos/visa', verbose_name='Фото', null=True, blank=True)
    # add_photo = 'later'


class RealEstate(models.Model):
    """Недвижка"""

    CHOICES_SIX = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, '6 и больше'),
    )

    CHOICES_TEN = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, '10 и больше'),
    )
    number_of_rooms = models.PositiveSmallIntegerField(choices=CHOICES_SIX, verbose_name='Кол-во комнат')
    floor = models.PositiveSmallIntegerField(choices=CHOICES_TEN, verbose_name='Этаж')
    max_floor = models.PositiveSmallIntegerField(choices=CHOICES_TEN, verbose_name='Этажность здания')
    kitchen = models.BooleanField(default=False, verbose_name='Нал кухни')
    wi_fi = models.BooleanField(default=False, verbose_name='Нал wifi')
    air_conditioner = models.BooleanField(default=False, verbose_name='Нал кондера')
    sleeper = models.PositiveSmallIntegerField(choices=CHOICES_SIX, verbose_name='Кол-во спальных мест')
    commission = models.PositiveSmallIntegerField(null=True, blank=True, default=0, verbose_name='Комиссия')


class Transport(models.Model):
    """Аренда транспорта"""

    CHOICES_TRANSPORT = (
        (1, 'Байк'),
        (2, 'Мотоцикл'),
        (3, 'Автомобиль'),
        (4, 'Другое')
    )
    # mark = models.CharField()
    # model = models.CharField()
    variety = models.PositiveSmallIntegerField(choices=CHOICES_TRANSPORT, verbose_name='Разновидность')
    year = models.PositiveSmallIntegerField(verbose_name='Год')
    engine_power = models.PositiveSmallIntegerField(verbose_name='Объем двигателя')
    delivery = models.BooleanField(default=False, verbose_name='Доставка')
    commission = models.PositiveSmallIntegerField(null=True, blank=True, default=0, verbose_name='Комиссия')
    air_conditioner = models.BooleanField(default=False, verbose_name='Нал кондера', null=True, blank=True)


# class Work(models.Model):
#     """Работа, шутинг"""
