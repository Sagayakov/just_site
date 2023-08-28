from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class BaseModel(models.Model):
    """Базовая модель добавляющая поля используемые во всех моделях"""

    class Meta:
        abstract = True

    name_offer = models.CharField(max_length=64, verbose_name='Название объявления')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    contact = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Создатель модели')
    description = models.CharField(max_length=2048, verbose_name='Описание')
    is_public = models.BooleanField(default=True, verbose_name='Публикация')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    location = models.ManyToManyField('LocationModel', verbose_name='Локация', blank=True)  # временное решение
    # проработать нужно добавление карты, отображение города
    slug = models.SlugField(blank=True, null=True, db_index=True, unique=True, verbose_name='Ссылка')
    priority = models.BooleanField(default=False, verbose_name='Приоритетное размещение')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = datetime.now().strftime("%Y%m%d%H%M%S%f")
        super().save(*args, **kwargs)


class BaseSlugModel(models.Model):
    """Базовая модель расширяющая Foreign модели"""

    slug = models.SlugField(blank=True, null=True, db_index=True, unique=True, verbose_name='Ссылка')

    class Meta:
        abstract = True


class LocationModel(BaseSlugModel):
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
    """ForeignKey. Вид услуги"""

    kind = models.CharField(max_length=64, verbose_name='Вид услуги')  # маникюр, обучение игры на гитаре

    def __str__(self):
        return f'{self.kind}'

    class Meta:
        verbose_name = "F Вид услуги"
        verbose_name_plural = "F Вид услуг"


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

    variety_1 = models.ForeignKey(VarietyVisaModel, on_delete=models.PROTECT, related_name='variety_1',
                                  verbose_name='Вид визы_1')
    validity_1 = models.ForeignKey(ValidityVisaModel, on_delete=models.PROTECT, related_name='validity_1',
                                   verbose_name='Продолжительность визы_1')
    # price_1 из наследуемого класса BaseModel. Называется там price
    small_description_1 = models.CharField(max_length=64, null=True, blank=True, verbose_name='Краткое описание_1')

    variety_2 = models.ForeignKey(VarietyVisaModel, on_delete=models.PROTECT, related_name='variety_2',
                                  blank=True, null=True, verbose_name='Вид визы_2')
    validity_2 = models.ForeignKey(ValidityVisaModel, on_delete=models.PROTECT, related_name='validity_2',
                                   blank=True, null=True, verbose_name='Продолжительность визы_2')
    price_2 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                  verbose_name='Цена_2')
    small_description_2 = models.CharField(max_length=64, null=True, blank=True, verbose_name='Краткое описание_2')

    variety_3 = models.ForeignKey(VarietyVisaModel, on_delete=models.PROTECT, related_name='variety_3',
                                  blank=True, null=True, verbose_name='Вид визы_3')
    validity_3 = models.ForeignKey(ValidityVisaModel, on_delete=models.PROTECT, related_name='validity_3',
                                   blank=True, null=True, verbose_name='Продолжительность визы_3')
    price_3 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                  verbose_name='Цена_3')
    small_description_3 = models.CharField(max_length=64, null=True, blank=True, verbose_name='Краткое описание_3')

    variety_4 = models.ForeignKey(VarietyVisaModel, on_delete=models.PROTECT, related_name='variety_4',
                                  blank=True, null=True, verbose_name='Вид визы_4')
    validity_4 = models.ForeignKey(ValidityVisaModel, on_delete=models.PROTECT, related_name='validity_4',
                                   blank=True, null=True, verbose_name='Продолжительность визы_4')
    price_4 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                  verbose_name='Цена_4')
    small_description_4 = models.CharField(max_length=64, null=True, blank=True, verbose_name='Краткое описание_4')

    variety_5 = models.ForeignKey(VarietyVisaModel, on_delete=models.PROTECT, related_name='variety_5',
                                  blank=True, null=True, verbose_name='Вид визы_5')
    validity_5 = models.ForeignKey(ValidityVisaModel, on_delete=models.PROTECT, related_name='validity_5',
                                   blank=True, null=True, verbose_name='Продолжительность визы_5')
    price_5 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                  verbose_name='Цена_5')
    small_description_5 = models.CharField(max_length=64, null=True, blank=True, verbose_name='Краткое описание_5')

    variety_6 = models.ForeignKey(VarietyVisaModel, on_delete=models.PROTECT, related_name='variety_6',
                                  blank=True, null=True, verbose_name='Вид визы_6')
    validity_6 = models.ForeignKey(ValidityVisaModel, on_delete=models.PROTECT, related_name='validity_6',
                                   blank=True, null=True, verbose_name='Продолжительность визы_6')
    price_6 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                  verbose_name='Цена_6')
    small_description_6 = models.CharField(max_length=64, null=True, blank=True, verbose_name='Краткое описание_6')

    variety_7 = models.ForeignKey(VarietyVisaModel, on_delete=models.PROTECT, related_name='variety_7',
                                  blank=True, null=True, verbose_name='Вид визы_7')
    validity_7 = models.ForeignKey(ValidityVisaModel, on_delete=models.PROTECT, related_name='validity_7',
                                   blank=True, null=True, verbose_name='Продолжительность визы_7')
    price_7 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                  verbose_name='Цена_7')
    small_description_7 = models.CharField(max_length=64, null=True, blank=True, verbose_name='Краткое описание_7')

    variety_8 = models.ForeignKey(VarietyVisaModel, on_delete=models.PROTECT, related_name='variety_8',
                                  blank=True, null=True, verbose_name='Вид визы_8')
    validity_8 = models.ForeignKey(ValidityVisaModel, on_delete=models.PROTECT, related_name='validity_8',
                                   blank=True, null=True, verbose_name='Продолжительность визы_8')
    price_8 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                  verbose_name='Цена_8')
    small_description_8 = models.CharField(max_length=64, null=True, blank=True, verbose_name='Краткое описание_8')

    photo = models.ImageField(upload_to='photos/visa', verbose_name='Фото', null=True, blank=True)

    # add_photo = 'later'

    def __str__(self):
        return f'{self.variety_1} - {self.validity_1}'

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
    floor = models.PositiveSmallIntegerField(choices=CHOICES_TEN, blank=True, null=True, verbose_name='Этаж')
    max_floor = models.PositiveSmallIntegerField(choices=CHOICES_TEN, blank=True, null=True,
                                                 verbose_name='Этажность здания')
    kitchen = models.BooleanField(default=False, verbose_name='Нал кухни')
    wi_fi = models.BooleanField(default=False, verbose_name='Нал wi-fi')
    air_conditioner = models.BooleanField(default=False, verbose_name='Нал кондера')
    washing_machine = models.BooleanField(default=False, verbose_name='Нал стир машинки')
    sleeper = models.PositiveSmallIntegerField(choices=CHOICES_SIX, blank=True, null=True,
                                               verbose_name='Кол-во спальных мест')
    commission = models.PositiveSmallIntegerField(null=True, blank=True, default=0, verbose_name='Комиссия')
    photo = models.ImageField(upload_to='photos/estate', blank=True, null=True, verbose_name='Фото')

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
    model = models.ForeignKey(ModelTransportModel, blank=True, null=True, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to='photos/transport', verbose_name='Фото', null=True, blank=True)
    variety = models.PositiveSmallIntegerField(choices=CHOICES_TRANSPORT, verbose_name='Разновидность')
    year = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Год')
    engine_power = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Объем двигателя')
    delivery = models.BooleanField(default=False, verbose_name='Доставка')
    commission = models.PositiveSmallIntegerField(null=True, blank=True, default=0, verbose_name='Комиссия')
    air_conditioner = models.BooleanField(default=False, blank=True, null=True, verbose_name='Нал кондера')

    def __str__(self):
        return f'{self.mark} - {self.model}'

    class Meta:
        verbose_name = "Аренда транспорта"
        verbose_name_plural = "Аренда транспорта"


class WorkModel(BaseModel):
    """Работа, шутинг"""

    CHOICES_PERIOD = (
        (1, 'Разовое задание'),
        (2, 'Временная работа'),
        (3, 'Постоянная работа'),
        (4, "Неполный день"),
        (5, "Другое")
    )

    period = models.CharField(choices=CHOICES_PERIOD, max_length=1, verbose_name='Период')
    # для отображения периода оплаты. Price/period
    experience = models.BooleanField(default=False, verbose_name='Наличие опыта')
    full_time = models.BooleanField(default=False, verbose_name='Полный рабочий день')
    photo = models.ImageField(upload_to='photos/work', null=True, blank=True, verbose_name='Фото')

    def __str__(self):
        return f'{self.name_offer} - {self.period}'

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

    theme_service = models.ForeignKey(NameServiceModel, blank=True, null=True, on_delete=models.PROTECT,
                                      verbose_name='Направление услуги')
    unit = models.PositiveSmallIntegerField(choices=CHOICES_UNIT, verbose_name="Единица измерения")
    photo = models.ImageField(upload_to='photos/services', verbose_name='Фото', null=True, blank=True)
    home_visit = models.BooleanField(default=False, verbose_name='Выезд на дом')

    def __str__(self):
        return f'{self.theme_service} - {self.price}'

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class CurrencyModel(models.Model):
    """Валютные пары"""

    name_currency_1_1 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_1_1',
                                          help_text='USD', verbose_name='Валюта 1_1')  # USD
    name_currency_1_2 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_1_2',
                                          help_text='RUB', verbose_name='Валюта 1_2')  # RUB
    price_1_1 = models.DecimalField(decimal_places=2, max_digits=10, default=0, help_text='USD/RUB',
                                    verbose_name='Цена_1_1')  # USD/RUB
    price_1_2 = models.DecimalField(decimal_places=2, max_digits=10, default=0, help_text='RUB/USD',
                                    null=True, blank=True, verbose_name='Цена_1_2')  # RUB/USD
    small_description_1 = models.CharField(max_length=32, null=True, blank=True, help_text='курс от 10 до 100 USD',
                                           verbose_name='Краткое описание_1')
    # курс от 10 до 100 USD

    name_currency_2_1 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_2_1',
                                          null=True, blank=True, verbose_name='Валюта 2_1')
    name_currency_2_2 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_2_2',
                                          null=True, blank=True, verbose_name='Валюта 2_2')
    price_2_1 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                    verbose_name='Цена_2_1')
    price_2_2 = models.DecimalField(decimal_places=2, max_digits=10, default=0,
                                    null=True, blank=True, verbose_name='Цена_2_2')
    small_description_2 = models.CharField(max_length=32, null=True, blank=True, help_text='курс от 101 до 999 USDT',
                                           verbose_name='Краткое описание_2')

    name_currency_3_1 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_3_1',
                                          null=True, blank=True, verbose_name='Валюта 3_1')
    name_currency_3_2 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_3_2',
                                          null=True, blank=True, verbose_name='Валюта 3_2')
    price_3_1 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                    verbose_name='Цена_3_1')
    price_3_2 = models.DecimalField(decimal_places=2, max_digits=10, default=0,
                                    null=True, blank=True, verbose_name='Цена_3_2')
    small_description_3 = models.CharField(max_length=32, null=True, blank=True, verbose_name='Краткое описание_3')

    name_currency_4_1 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_4_1',
                                          null=True, blank=True, verbose_name='Валюта 4_1')
    name_currency_4_2 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_4_2',
                                          null=True, blank=True, verbose_name='Валюта 4_2')
    price_4_1 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                    verbose_name='Цена_4_1')
    price_4_2 = models.DecimalField(decimal_places=2, max_digits=10, default=0,
                                    null=True, blank=True, verbose_name='Цена_4_2')
    small_description_4 = models.CharField(max_length=32, null=True, blank=True, verbose_name='Краткое описание_4')

    name_currency_5_1 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_5_1',
                                          null=True, blank=True, verbose_name='Валюта 5_1')
    name_currency_5_2 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_5_2',
                                          null=True, blank=True, verbose_name='Валюта 5_2')
    price_5_1 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                    verbose_name='Цена_5_1')
    price_5_2 = models.DecimalField(decimal_places=2, max_digits=10, default=0,
                                    null=True, blank=True, verbose_name='Цена_5_2')
    small_description_5 = models.CharField(max_length=32, null=True, blank=True, verbose_name='Краткое описание_5')

    name_currency_6_1 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_6_1',
                                          null=True, blank=True, verbose_name='Валюта 6_1')
    name_currency_6_2 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_6_2',
                                          null=True, blank=True, verbose_name='Валюта 6_2')
    price_6_1 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                    verbose_name='Цена_6_1')
    price_6_2 = models.DecimalField(decimal_places=2, max_digits=10, default=0,
                                    null=True, blank=True, verbose_name='Цена_6_2')
    small_description_6 = models.CharField(max_length=32, null=True, blank=True, verbose_name='Краткое описание_6')

    name_currency_7_1 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_7_1',
                                          null=True, blank=True, verbose_name='Валюта 7_1')
    name_currency_7_2 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_7_2',
                                          null=True, blank=True, verbose_name='Валюта 7_2')
    price_7_1 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                    verbose_name='Цена_7_1')
    price_7_2 = models.DecimalField(decimal_places=2, max_digits=10, default=0,
                                    null=True, blank=True, verbose_name='Цена_7_2')
    small_description_7 = models.CharField(max_length=32, null=True, blank=True, verbose_name='Краткое описание_7')

    name_currency_8_1 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_8_1',
                                          null=True, blank=True, verbose_name='Валюта 8_1')
    name_currency_8_2 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_8_2',
                                          null=True, blank=True, verbose_name='Валюта 8_2')
    price_8_1 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                    verbose_name='Цена_8_1')
    price_8_2 = models.DecimalField(decimal_places=2, max_digits=10, default=0,
                                    null=True, blank=True, verbose_name='Цена_8_2')
    small_description_8 = models.CharField(max_length=32, null=True, blank=True, verbose_name='Краткое описание_8')

    name_currency_9_1 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_9_1',
                                          null=True, blank=True, verbose_name='Валюта 9_1')
    name_currency_9_2 = models.ForeignKey(NameCurrencyModel, on_delete=models.PROTECT, related_name='currency_9_2',
                                          null=True, blank=True, verbose_name='Валюта 9_2')
    price_9_1 = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True,
                                    verbose_name='Цена_9_1')
    price_9_2 = models.DecimalField(decimal_places=2, max_digits=10, default=0,
                                    null=True, blank=True, verbose_name='Цена_9_2')
    small_description_9 = models.CharField(max_length=32, null=True, blank=True, verbose_name='Краткое описание_9')

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
        return f'{self.name_currency_1_1}/{self.name_currency_1_2} - {self.price_1_1}'

    class Meta:
        verbose_name = "Валютная пара"
        verbose_name_plural = "Валютные пары"


class BuySellModel(BaseModel):
    """Покупка/продажа"""

    CHOICES_UNIT = (
        (1, 'Шт'),
        (2, "Кг"),
        (3, "Гр"),
        (4, "Другое")
    )
    unit = models.PositiveSmallIntegerField(choices=CHOICES_UNIT, verbose_name="Единица измерения")  # price/unit
    delivery = models.BooleanField(default=False, verbose_name='Доставка')
    photo = models.ImageField(upload_to='photos/buy_sell', verbose_name='Фото', null=True, blank=True)

    def __str__(self):
        return f'{self.name_offer} - {self.price}'

    class Meta:
        verbose_name = "Покупка/продажа"
        verbose_name_plural = "Покупка/продажа"


class FoodModel(BaseModel):
    """Домашняя еда"""

    CHOICES_UNIT = (
        (1, 'Шт'),
        (2, "Кг"),
        (3, "Гр"),
        (4, "Другое")
    )
    unit = models.PositiveSmallIntegerField(choices=CHOICES_UNIT, verbose_name="Единица измерения")
    delivery = models.BooleanField(default=False, verbose_name='Доставка')
    photo = models.ImageField(upload_to='photos/food', verbose_name='Фото', null=True, blank=True)

    def __str__(self):
        return f'{self.name_offer} - {self.price}'

    class Meta:
        verbose_name = "Домашняя еда"
        verbose_name_plural = "Домашняя еда"


class TaxiModel(BaseModel):
    """Такси"""

    CHOICES_UNIT = (
        (1, 'Км'),
        (2, "Час"),
        (3, "Маршрут"),
        (4, 'Другое')
    )
    unit = models.PositiveSmallIntegerField(choices=CHOICES_UNIT, null=True, blank=True,
                                            verbose_name="Единица измерения")
    photo = models.ImageField(upload_to='photos/taxi', verbose_name='Фото', null=True, blank=True)

    def __str__(self):
        return f'{self.name_offer} - {self.price}'

    class Meta:
        verbose_name = "Такси"
        verbose_name_plural = "Такси"


class TripModel(BaseModel):
    """Экскурсии"""

    CHOICES_UNIT = (
        (1, 'Единица'),
        (2, "Час"),
        (3, "День"),
        (4, 'Другое')
    )
    unit = models.PositiveSmallIntegerField(choices=CHOICES_UNIT, verbose_name="Единица измерения")
    photo = models.ImageField(upload_to='photos/trip', verbose_name='Фото', null=True, blank=True)

    def __str__(self):
        return f'{self.name_offer} - {self.price}'

    class Meta:
        verbose_name = "Экскурсия"
        verbose_name_plural = "Экскурсии"
