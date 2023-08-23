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

    class Meta:
        verbose_name = "F Локация"
        verbose_name_plural = "F Локации"


class MarkTransportModel(BaseSlugModel):
    """ForeignKey. Марка трансопрта"""

    mark_tr = models.CharField(max_length=64, verbose_name='Марка')

    def __str__(self):
        return f'{self.mark_tr}'

    class Meta:
        verbose_name = "F Транспорта марка"
        verbose_name_plural = "F Транспорта марки"


class ModelTransportModel(BaseSlugModel):
    """ForeignKey. Модель транспорта"""

    model_tr = models.CharField(max_length=64, verbose_name='Модель')

    def __str__(self):
        return f'{self.model_tr}'

    class Meta:
        verbose_name = "F Транспорта модель"
        verbose_name_plural = "F Транспорта модели"


class ThemeEventModel(BaseSlugModel):
    """ForeignKey. Тематика мероприятия"""

    theme = models.CharField(max_length=64, verbose_name='Тематика')

    def __str__(self):
        return f'{self.theme}'

    class Meta:
        verbose_name = "F Тематика"
        verbose_name_plural = "F Тематики"


class VarietyVisaModel(BaseSlugModel):
    """ForeignKey. Вид визы"""

    variety = models.CharField(max_length=64, verbose_name='Вид визы')  # туристическая, бизнес или др.

    def __str__(self):
        return f'{self.variety}'

    class Meta:
        verbose_name = "F Виза вид"
        verbose_name_plural = "F Визы вид"


class ValidityVisaModel(BaseSlugModel):
    """ForeignKey. Продолжительность визы"""

    validity = models.CharField(max_length=64, verbose_name='Продолжительность визы')  # 30 дней\1 год или др

    def __str__(self):
        return f'{self.validity}'

    class Meta:
        verbose_name = "F Виза продолжительность"
        verbose_name_plural = "F Визы продолжительность"


class NameServiceModel(BaseSlugModel):
    """ForeignKey. Наименование услуги"""

    validity = models.CharField(max_length=64, verbose_name='Наименование услуги')  # маникюр, обучение игры на гитаре

    def __str__(self):
        return f'{self.validity}'

    class Meta:
        verbose_name = "F Наименование услуги"
        verbose_name_plural = "F Наименование услуг"


class NameCurrencyModel(BaseSlugModel):
    """ForeignKey. Наименование валюты"""

    currency = models.CharField(max_length=64, verbose_name='Наименование валюты')

    def __str__(self):
        return f'{self.currency}'

    class Meta:
        verbose_name = "F Наименование валюты"
        verbose_name_plural = "F Наименование валют"


# старт маин моделей


class EventPosterModel(BaseModel):
    """Модель мероприятий, афиш"""

    date = models.DateTimeField(verbose_name='Дата и время')
    themes = models.ForeignKey(ThemeEventModel, on_delete=models.PROTECT, verbose_name='Тематика')
    photo = models.ImageField(upload_to='photos/event', verbose_name='Фото', null=True, blank=True)

    # add_photo = 'later'

    def __str__(self):
        return f'{self.themes} - {self.date}'

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"


class VisaModel(BaseModel):
    """Визы, и прочие документы"""

    variety = models.ForeignKey(VarietyVisaModel, on_delete=models.PROTECT, verbose_name='Вид визы')
    validity = models.ForeignKey(ValidityVisaModel, on_delete=models.PROTECT, verbose_name='Продолжительность визы')
    photo = models.ImageField(upload_to='photos/visa', verbose_name='Фото', null=True, blank=True)

    # add_photo = 'later'

    def __str__(self):
        return f'{self.variety} - {self.validity}'

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
    wi_fi = models.BooleanField(default=False, verbose_name='Нал wi-fi')
    air_conditioner = models.BooleanField(default=False, verbose_name='Нал кондера')
    washing_machine = models.BooleanField(default=False, verbose_name='Нал стир машинки')
    sleeper = models.PositiveSmallIntegerField(choices=CHOICES_SIX, verbose_name='Кол-во спальных мест')
    commission = models.PositiveSmallIntegerField(null=True, blank=True, default=0, verbose_name='Комиссия')
    photo = models.ImageField(upload_to='photos/estate', verbose_name='Фото', null=True, blank=True)

    def __str__(self):
        return f'{self.price} - {self.floor}/{self.max_floor}'

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

    def __str__(self):
        return f'{self.mark} - {self.model}'

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
    period = models.CharField(choices=CHOICES_PERIOD, max_length=1,
                              verbose_name='Период')  # для отображения периода оплаты. Price/period
    photo = models.ImageField(upload_to='photos/work', verbose_name='Фото', null=True, blank=True)

    def __str__(self):
        return f'{self.name_vacancy} - {self.period}'

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
    photo = models.ImageField(upload_to='photos/services', verbose_name='Фото', null=True, blank=True)

    def __str__(self):
        return f'{self.name_service} - {self.price}'

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class CurrencyModel(models.Model):
    """Валютные пары (до 5 шт)"""

    name_currency_1_1 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_1_1',
                                          verbose_name='Валюта 1_1')
    name_currency_1_2 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_1_2',
                                          verbose_name='Валюта 1_2')
    price_1 = models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='Цена_1')

    name_currency_2_1 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_2_1',
                                          null=True, blank=True, verbose_name='Валюта 2_1')
    name_currency_2_2 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_2_2',
                                          null=True, blank=True, verbose_name='Валюта 2_2')
    price_2 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                  verbose_name='Цена_2')

    name_currency_3_1 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_3_1',
                                          null=True, blank=True, verbose_name='Валюта 3_1')
    name_currency_3_2 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_3_2',
                                          null=True, blank=True, verbose_name='Валюта 3_2')
    price_3 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                  verbose_name='Цена_3')

    name_currency_4_1 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_4_1',
                                          null=True, blank=True, verbose_name='Валюта 4_1')
    name_currency_4_2 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_4_2',
                                          null=True, blank=True, verbose_name='Валюта 4_2')
    price_4 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                  verbose_name='Цена_4')

    name_currency_5_1 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_5_1',
                                          null=True, blank=True, verbose_name='Валюта 5_1')
    name_currency_5_2 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_5_2',
                                          null=True, blank=True, verbose_name='Валюта 5_2')
    price_5 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                  verbose_name='Цена_5')

    delivery = models.BooleanField(default=False, verbose_name='Доставка')
    contact = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Создатель модели')
    description = models.CharField(max_length=2048, verbose_name='Описание')
    is_public = models.BooleanField(default=True, verbose_name='Публикация')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    location = models.ManyToManyField('LocationModel', verbose_name='Локация', blank=True)  # временное решение
    # проработать нужно добавление карты, отображение города
    slug = models.SlugField(blank=True, null=True, db_index=True, unique=True, verbose_name='Ссылка')

    def __str__(self):
        return f'{self.name_currency_1_1}/{self.name_currency_1_2} - {self.price_1}'

    class Meta:
        verbose_name = "Валютная пара"
        verbose_name_plural = "Валютные пары"


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
    photo = models.ImageField(upload_to='photos/buy_sell', verbose_name='Фото', null=True, blank=True)

    def __str__(self):
        return f'{self.name_product} - {self.price}'

    class Meta:
        verbose_name = "Покупка/продажа"
        verbose_name_plural = "Покупка/продажа"


class FoodModel(BuySellModel):
    """Домашняя еда"""

    new_photo = models.ImageField(upload_to='photos/food', verbose_name='Фото_new', null=True, blank=True)

    class Meta:
        verbose_name = "Домашняя еда"
        verbose_name_plural = "Домашняя еда"


class TaxiModel(BuySellModel):
    """Такси"""

    new_photo = models.ImageField(upload_to='photos/taxi', verbose_name='Фото_new', null=True, blank=True)

    class Meta:
        verbose_name = "Такси"
        verbose_name_plural = "Такси"


class TripModel(BuySellModel):
    """Экскурсии"""

    new_photo = models.ImageField(upload_to='photos/trip', verbose_name='Фото_new', null=True, blank=True)

    class Meta:
        verbose_name = "Экскурсия"
        verbose_name_plural = "Экскурсии"
