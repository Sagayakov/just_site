from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    """Базовая модель добавляющая поля используемые во всех моделях"""

    class Meta:
        abstract = True

    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    contact = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Создатель модели')
    description = models.CharField(max_length=2048, verbose_name='Описание')
    is_public = models.BooleanField(default=True, verbose_name='Публикация')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    location = models.ManyToManyField('LocationModel', verbose_name='Локация', blank=True)  # временное решение
    # проработать нужно добавление карты, отображение города
    slug = models.SlugField(blank=True, null=True, db_index=True, unique=True, verbose_name='Ссылка')


class BaseSlugModel(models.Model):
    """Базовая модель расширяющая Foreign модели"""

    slug = models.SlugField(blank=True, null=True, db_index=True, unique=True, verbose_name='Ссылка')

    class Meta:
        abstract = True


class LocationModel(models.Model):
    """ForeignKey. Место расположения объявления"""

    location = models.CharField(max_length=64, verbose_name='Город/район')

    def __str__(self):
        return f'{self.location}'


class MarkTransportModel(BaseSlugModel):
    """ForeignKey. Марка трансопрта"""

    mark_tr = models.CharField(max_length=64, verbose_name='Марка')

    def __str__(self):
        return f'{self.mark_tr}'

    class Meta:
        verbose_name = "Марка"
        verbose_name_plural = "Марки"


class ModelTransportModel(BaseSlugModel):
    """ForeignKey. Модель транспорта"""

    model_tr = models.CharField(max_length=64, verbose_name='Модель')

    def __str__(self):
        return f'{self.model_tr}'

    class Meta:
        verbose_name = "Модель"
        verbose_name_plural = "Модели"


class ThemeEventModel(BaseSlugModel):
    """ForeignKey. Тематика мероприятия"""

    theme = models.CharField(max_length=64, verbose_name='Тематика')

    def __str__(self):
        return f'{self.theme}'

    class Meta:
        verbose_name = "Тематика"
        verbose_name_plural = "Тематики"


class VarietyVisaModel(BaseSlugModel):
    """ForeignKey. Вид визы"""

    variety = models.CharField(max_length=64, verbose_name='Вид визы') # туристическая, бизнес или др.

    def __str__(self):
        return f'{self.variety}'

    class Meta:
        verbose_name = "Вид визы"
        verbose_name_plural = "Виды виз"


class ValidityVisaModel(BaseSlugModel):
    """ForeignKey. Продолжительность визы"""

    validity = models.CharField(max_length=64, verbose_name='Продолжительность визы') # 30 дней\1 год или др

    def __str__(self):
        return f'{self.validity}'

    class Meta:
        verbose_name = "Продолжительность визы"
        verbose_name_plural = "Продолжительность виз"


class NameServiceModel(BaseSlugModel):
    """ForeignKey. Наименование услуги"""

    validity = models.CharField(max_length=64, verbose_name='Наименование услуги')  # маникюр, обучение игры на гитаре

    def __str__(self):
        return f'{self.validity}'

    class Meta:
        verbose_name = "Наименование услуги"
        verbose_name_plural = "Наименование услуг"


class NameCurrencyModel(BaseSlugModel):
    """ForeignKey. Наименование валюты"""

    currency = models.CharField(max_length=64, verbose_name='Наименование валюты')

    def __str__(self):
        return f'{self.currency}'

    class Meta:
        verbose_name = "Наименование валюты"
        verbose_name_plural = "Наименование валют"

# старт маин моделей


class EventPosterModel(BaseModel):
    """Модель мероприятий, афиш"""

    date = models.DateTimeField(verbose_name='Дата и время')
    themes = models.ForeignKey(ThemeEventModel, on_delete=models.PROTECT, verbose_name='Тематика')
    photo = models.ImageField(upload_to='photos/event', verbose_name='Фото', null=True, blank=True)
    # add_photo = 'later'

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"


class VisaModel(BaseModel):
    """Визы, и прочие документы"""

    variety = models.ForeignKey(VarietyVisaModel, on_delete=models.PROTECT, verbose_name='Вид визы')
    validity = models.ForeignKey(ValidityVisaModel, on_delete=models.PROTECT, verbose_name='Продолжительность визы')
    photo = models.ImageField(upload_to='photos/visa', verbose_name='Фото', null=True, blank=True)
    # add_photo = 'later'

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"


class RealEstateModel(BaseModel):
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
    amount_of_rooms = models.PositiveSmallIntegerField(choices=CHOICES_SIX, verbose_name='Кол-во комнат')
    floor = models.PositiveSmallIntegerField(choices=CHOICES_TEN, verbose_name='Этаж')
    max_floor = models.PositiveSmallIntegerField(choices=CHOICES_TEN, verbose_name='Этажность здания')
    kitchen = models.BooleanField(default=False, verbose_name='Нал кухни')
    wi_fi = models.BooleanField(default=False, verbose_name='Нал wifi')
    air_conditioner = models.BooleanField(default=False, verbose_name='Нал кондера')
    washing_machine = models.BooleanField(default=False, verbose_name='Нал стир машинки')
    sleeper = models.PositiveSmallIntegerField(choices=CHOICES_SIX, verbose_name='Кол-во спальных мест')
    commission = models.PositiveSmallIntegerField(null=True, blank=True, default=0, verbose_name='Комиссия')
    photo = models.ImageField(upload_to='photos/estate', verbose_name='Фото', null=True, blank=True)

    class Meta:
        verbose_name = "Аренда недвижимости"
        verbose_name_plural = "Аренда недвижимости"


class TransportModel(BaseModel):
    """Аренда транспорта"""

    CHOICES_TRANSPORT = (
        (1, 'Байк'),
        (2, 'Мотоцикл'),
        (3, 'Автомобиль'),
        (4, 'Другое')
    )
    mark = models.ForeignKey(MarkTransportModel, on_delete=models.PROTECT)
    model = models.ForeignKey(ModelTransportModel, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to='photos/transport', verbose_name='Фото', null=True, blank=True)
    variety = models.CharField(choices=CHOICES_TRANSPORT, max_length=1, verbose_name='Разновидность')
    year = models.PositiveSmallIntegerField(verbose_name='Год')
    engine_power = models.PositiveSmallIntegerField(verbose_name='Объем двигателя')
    delivery = models.BooleanField(default=False, verbose_name='Доставка')
    commission = models.PositiveSmallIntegerField(null=True, blank=True, default=0, verbose_name='Комиссия')
    air_conditioner = models.BooleanField(default=False, verbose_name='Нал кондера', null=True, blank=True)

    class Meta:
        verbose_name = "Аренда транспорта"
        verbose_name_plural = "Аренда транспорта"


class WorkModel(BaseModel):
    """Работа, шутинг"""

    CHOICES_PERIOD = (
        (1, 'День'),
        (2, 'Месяц'),
        (3, "Другое")
    )

    name_vacancy = models.CharField(max_length=64, verbose_name='Название вакансии')
    period = models.CharField(choices=CHOICES_PERIOD, max_length=1, verbose_name='Период') # для отображения периода оплаты. Price/period
    photo = models.ImageField(upload_to='photos/work', verbose_name='Фото', null=True, blank=True)

    class Meta:
        verbose_name = "Работа"
        verbose_name_plural = "Работа"


class ServicesModel(BaseModel):
    """Оказываемые услуги"""

    CHOICES_UNIT = (
        (1, 'Услуга'),
        (2, "Час"),
        (3, "Другое")
    )

    name_service = models.ForeignKey(NameServiceModel, on_delete=models.PROTECT)
    unit = models.CharField(choices=CHOICES_UNIT, max_length=1, verbose_name="Единица измерения")
    photo = models.ImageField(upload_to='photos/event', verbose_name='Фото', null=True, blank=True)

    def __str__(self):
        return f'{self.name_service} - {self.price}'

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class BuySellModel(BaseModel):
    """Покупка/продажа"""

    CHOICES_UNIT = (
        (1, 'Шт'),
        (2, "Кг"),
        (3, "Гр")
    )
    name_product = models.CharField(max_length=64, verbose_name='Название продукта')
    unit = models.CharField(choices=CHOICES_UNIT, max_length=1, verbose_name="Единица измерения")
    delivery = models.BooleanField(default=False, verbose_name='Доставка')


# class CurrencyModel(BaseModel):
#     """Валютные пары
#     Доделать логику"""
#
#     name_currency_1 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT)
#     name_currency_2 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT)
#     price_2 = models.PositiveIntegerField(default=0, verbose_name='Цена')
#     price_3 = models.PositiveIntegerField(default=0, verbose_name='Цена')
#     border_1 = models.PositiveIntegerField(default=0, verbose_name='Граница изменения курса')
#     border_2 = models.PositiveIntegerField(default=0, verbose_name='Граница изменения курса')
#     delivery = models.BooleanField(default=False, verbose_name='Доставка')


class FoodModel(BuySellModel):
    """Домашняя еда"""
    pass


class TaxiModel(BuySellModel):
    """Taxi"""
    pass


class TripModel(BuySellModel):
    """Экскурсии"""
    pass
