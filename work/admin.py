from django.contrib import admin
from .models import ResumesModel, VacanciesModel


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'date_publication', 'is_moderated')
    ordering = ["is_moderated"]


class VacanciesAdmin(admin.ModelAdmin):
    list_display = ('id', 'firm_name', 'title', 'trash')
    ordering = ["-trash"]


admin.site.register(ResumesModel, ResumeAdmin)
admin.site.register(VacanciesModel, VacanciesAdmin)
