from django.db import models
from django.contrib.auth.models import User
from accounts.models import AdvUser
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator


class ResumesModel(models.Model):
    """Резюме

    Описываются резюме пользователей. Используется во views.py и в forms.py

    """
    client_id = models.OneToOneField(AdvUser, on_delete=models.CASCADE, primary_key=True, verbose_name="ID работника")
    title = models.CharField(verbose_name="Название", max_length=64, default="В поисках работы")
    work_experience = models.CharField(verbose_name="Опыт работы", max_length=16)
    specialization = models.TextField(verbose_name="Специальность")
    desired_salary = models.IntegerField(verbose_name="Желаемая зарплата", blank=True)
    hard_skills = models.TextField(verbose_name="Ключевые навыки")
    about_you = models.TextField(verbose_name="О себе")
    native_language = models.TextField(verbose_name="Родной язык")
    foreign_language = models.TextField(verbose_name="Иностранный язык")
    date_publication = models.DateField(verbose_name="Дата публикации", auto_now_add=True)
    date_update = models.DateField(verbose_name="Дата последнего обновления", auto_now=True)
    counter = models.IntegerField(verbose_name="Просмотрело", default=0)
    is_moderated = models.BooleanField(verbose_name="Прошла модерацию", blank=True, default=False)
    is_deleted = models.BooleanField(verbose_name="Удалено", blank=True, default=False)

    class Meta:
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"
        ordering = ["-work_experience", "desired_salary"]

    def __str__(self):
        return str(self.client_id.id)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.title = self.title.lower()
        super().save(force_insert, force_update, using, update_fields)


class VacanciesModel(models.Model):
    """Вакансии

    Описываются вакансии фирм и различных ИП. Используется во views.py. Предполагается,
    что работа с данной моделью будет происходить через панель администратора

    """
    firm_name = models.CharField(max_length=32, verbose_name="Название фирмы", blank=True)
    title = models.CharField(max_length=64, verbose_name="Название", default="В поисках сотрудника")
    position = models.CharField(max_length=20, verbose_name="Должность")
    salary = models.CharField(max_length=100, verbose_name="Предлагаемая зарплата")
    requirements = models.TextField(verbose_name="Требования к работнику")
    working_conditions = models.TextField(verbose_name="Условия работы")
    work_experience = models.CharField(max_length=15, verbose_name="Опыт работы")
    address = models.CharField(max_length=100, verbose_name="Адрес фирмы")
    date_publication = models.DateField(verbose_name="Дата публикации", auto_now=True)
    email = models.EmailField(verbose_name="Электронная почта", validators=[EmailValidator])
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    trash = models.IntegerField(verbose_name="Оценка вакансии (1 - плохо, 10 - очень хорошо)",
                                validators=[MaxValueValidator(10), MinValueValidator(1)], default=1)
    counter = models.IntegerField(verbose_name="Просмотрело", blank=True, default=0)
    # img = models.ImageField(width_field=None, height_field=None, upload_to=None)

    class Meta:
        verbose_name = "Вакансию"
        verbose_name_plural = "Вакансии"
        ordering = ["-trash", ]

    def __str__(self):
        return str(self.id)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.title = self.title.lower()
        super().save(force_insert, force_update, using, update_fields)
