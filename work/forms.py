from django import forms
from .models import *

main_lang_choices = (
    ('Русский', u'Русский'),
    ('Украинский', u'Украинский'),
    ('Белорусский', u'Белорусский'),
)

foreign_lang_choices = (
    ('Нет', u'Нет'),
    ('Русский', u'Русский'),
    ('Английский', u'Английский'),
    ('Немецкий', u'Немецкий'),
    ('Французский', u'Французский'),
    ('Украинский', u'Украинский'),
    ('Белорусский', u'Белорусский'),
)


class ResumesForm(forms.ModelForm):
    class Meta:
        model = ResumesModel
        fields = ["work_experience", "title", "specialization", "desired_salary", "hard_skills", "about_you", "native_language",
                  "foreign_language", "client_id"]
        widgets = {
            "work_experience": forms.TextInput(attrs={
                "class": "experience res_experience form-control bg-light",
                "placeholder": "Опыт работы",
                "title": "90% работодателей не рассматривают вакансии без опыта",
                "data-toggle": "tooltip",
            }),
            "title": forms.TextInput(attrs={
                "class": "form-control res_title bg-light",
                "placeholder": "Заголовок",
                "title": "Постарайтесь выбрать 'кричащий' заголовок, так как по нему будет выполняться поиск",
                "data-toggle": "tooltip",
            }),
            "specialization": forms.TextInput(attrs={
                "class": "specialization res_specialization form-control bg-light",
                "placeholder": "Специализация",
                "title": "Укажите вашу специальность (Факультет, направление...)",
                "data-toggle": "tooltip",
                "data-placement": "bottom"
            }),
            "desired_salary": forms.TextInput(attrs={
                "class": "res_zp form-control bg-light",
                "placeholder": "Желаемая зарплата",
                "title":"Сверяйте зарплату с рынком, лучше написать на 15-20% больше, чем вы получаете сейчас",
                "data-toggle": "tooltip",
                "data-placement": "bottom"
            }),
            "hard_skills": forms.TextInput(attrs={
                "class": "res_skills form-control bg-light",
                "placeholder": "Hard skills",
                "title": "Избегайте очевидных вещей. Ключевые навыки - специфичные знания и умения, относящиеся непосредственно к рабочим процессам",
                "data-toggle": "tooltip",
                "data-placement": "bottom"
            }),
            "about_you": forms.Textarea(attrs={
                "class": "res_about form-control bg-light",
                "placeholder": "Обо мне",
                "title": 'Не путать с навыками, здесь вы указываете личностные качества. Вместо "Ответственность", например, напишите "Добросовестно отношусь к выполнению заданий" ',
                "data-toggle": "tooltip",
                "data-placement": "bottom"
            }),
            "native_language": forms.Select(choices=main_lang_choices, 
                                            attrs={"class": "bg-light res_native languages form-control"}),
            "foreign_language": forms.Select(choices=foreign_lang_choices,
                                             attrs={"class": "res_foreign form-control bg-light"}),
            "client_id": forms.HiddenInput()
        }
