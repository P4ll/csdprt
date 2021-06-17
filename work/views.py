from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.views.generic import ListView, DeleteView, UpdateView, CreateView, DetailView
from .models import *
from django.contrib.auth.models import User
from .forms import *
from django.urls import reverse, reverse_lazy
from django.contrib import messages
import os
import json

"""Раздел резюме"""


def redirect_to_my_resume(request):
    """
    Переносит юзера на его DetailView резюме. Если его резюме нет, то перенесёт
    на создание резюме
    """
    my_resume = ResumesModel.objects.filter(client_id=request.user.id)
    if my_resume:
        return redirect(reverse("check_resume", kwargs={"pk": request.user.id}))
    else:
        return redirect(reverse("create_resume"))


def redirect_update_resumes(request):
    """
    Защищённый редирект на update своего резюме
    """
    return redirect(reverse("update_my_resume", kwargs={"pk": request.user.id}))


def redirect_delete_resumes(request):
    """
    Редирект на удаление резюме
    """
    return redirect(reverse("delete_my_resume", kwargs={"pk": request.user.id}))


def get_contacts_resume(request, user_id):
    """Асинхронка для резюме

    Отдаёт данные клиенту с номером телефона, именем и почтой + каунтит просмотры

    user_id - id пользователя, от которого нужно получить данные

    """
    resume = ResumesModel.objects.get(client_id=user_id)
    if resume.is_deleted or not resume.is_moderated:
        return redirect(reverse("resumes"))
    resume.counter += 1
    resume.save()
    return HttpResponse(json.dumps({"phone": resume.client_id.phone,
                                    "name": resume.client_id.first_name,
                                    "email": resume.client_id.email}),
                        content_type="application/json")


def get_contacts_vacancies(request, vac_id):
    """Асинхронка для вакансий

    Отдаёт номер телефона и почту компании пользователю + каунтит просмотры

    vac_id - id вакансии
    """
    vacancies = VacanciesModel.objects.get(id=vac_id)
    vacancies.counter += 1
    vacancies.save()
    return HttpResponse(json.dumps({"phone": vacancies.phone, "email": vacancies.email}), content_type="application/json")


class ResumesView(ListView):
    model = ResumesModel
    paginate_by = 10
    template_name = 'work/resumes/resumes.html'
    context_object_name = "resumes"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parameter = None  # искомое слово в строке поиска
        self.object_list = None  # если не объявить, то будет undefined и будет ловить эксепшены

    def get(self, request, *args, **kwargs):
        """Переопределённый get

        В parameter попадает искомое слово или None
        """
        try:
            self.parameter = request.GET["find"]
        except:
            self.parameter = None
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        """Переопределённый контекст

        Искомое слово попадёт обратно в строку поиска.
        Если резюме удалено, то
        """
        context = super().get_context_data(**kwargs)
        try:
            have_resume = ResumesModel.objects.get(client_id=self.request.user.id)
            context["have_resume"] = True
            context["is_deleted"] = have_resume.is_deleted
        except:
            context["have_resume"] = False
            context["is_deleted"] = True
        context["parameter"] = self.parameter
        return context

    def get_queryset(self):
        if self.parameter:
            return ResumesModel.objects.filter(is_moderated=True, is_deleted=False).filter(title__contains=self.parameter)
        else:
            return ResumesModel.objects.filter(is_moderated=True, is_deleted=False)


class ResumesDetail(DetailView):
    model = ResumesModel
    template_name = "work/resumes/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        this_id = int(os.path.split(self.request.path)[1])
        context["this_user"] = AdvUser.objects.get(id=this_id)
        return context

    def get_queryset(self):
        """
        Проверка на то, что текущий пользователь запрашивает своё резюме. В таком случае
        возвращается толькое его резюме, иначе возвращается только с префиксом is_moderated и !is_deleted,
        чтобы нельзя было получить доступ через адресную строку к не модерированным резюме
        """
        if os.path.split(self.request.path)[1] == str(self.request.user.id):
            return ResumesModel.objects.filter(client_id=self.request.user.id)
        else:
            return ResumesModel.objects.filter(is_moderated=True, is_deleted=False)


class ResumesCreate(LoginRequiredMixin, CreateView):
    model = ResumesModel
    form_class = ResumesForm
    template_name = "work/create.html"

    def __init__(self):
        super().__init__()
        self.object = None

    def get(self, request, *args, **kwargs):
        try:
            ResumesModel.objects.get(client_id=request.user.id)
            return redirect(reverse("update_resume"))
        except Exception as e:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = AdvUser.objects.get(id=self.request.user.id)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "POST" and hasattr(self, 'object'):
            data = kwargs["data"].dict()
            data["title"] = data["title"].strip().lower()
            data.update({"client_id": self.request.user.id})
            kwargs["data"] = data
        return kwargs

    def get_success_url(self):
        return reverse("resumes")


class ResumesUpdate(LoginRequiredMixin, UpdateView):
    model = ResumesModel
    form_class = ResumesForm
    template_name = "work/create.html"

    def get(self, request, *args, **kwargs):
        if os.path.split(self.request.path)[1] == str(self.request.user.id):
            try:
                ResumesModel.objects.filter(client_id=request.user.id)
                return super().get(request, *args, **kwargs)
            except Exception as e:
                return redirect(reverse("resumes"))
        else:
            return redirect(reverse("update_resume"))

    def get_success_url(self):
        this_resume = ResumesModel.objects.get(client_id=self.request.user.id)
        this_resume.is_deleted = False
        this_resume.is_moderated = False
        this_resume.counter = 0
        this_resume.save()
        return reverse("resumes")


class ResumesDelete(LoginRequiredMixin, DeleteView):
    model = ResumesModel
    template_name = "work/delete.html"
    success_url = reverse_lazy("resumes")

    def get(self, request, *args, **kwargs):
        if os.path.split(self.request.path)[1] == str(self.request.user.id):
            try:
                this_resume = ResumesModel.objects.get(client_id=request.user.id)
                return super().get(request, *args, **kwargs)
            except Exception as e:
                return redirect(reverse("resumes"))
        else:
            return redirect(reverse("delete_resume"))

    def delete(self, request, *args, **kwargs):
        """
        Переопределение delete, чтобы вместо обычного удаления происходило
        изменение флага is_deleted на True, со сбросом флага модерации и каунтера
        """
        success_url = self.get_success_url()
        this_resume = ResumesModel.objects.get(client_id=request.user.id)
        this_resume.is_deleted = True
        this_resume.is_moderated = False
        this_resume.counter = 0
        this_resume.save()
        return redirect(success_url)

    def get_success_url(self):
        return reverse("resumes")


""""""


"""Раздел вакансий"""


class VacanciesView(ListView):
    model = VacanciesModel
    paginate_by = 10
    template_name = "work/vacancies/vacancies.html"
    context_object_name = "vacancies"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object_list = None
        self.parameter = None

    def get(self, request, *args, **kwargs):
        try:
            self.parameter = request.GET["find"]
        except:
            self.parameter = None
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parameter"] = self.parameter
        return context

    def get_queryset(self):
        if self.parameter:
            return VacanciesModel.objects.filter(title__contains=self.parameter)
        else:
            return VacanciesModel.objects.all()


class VacanciesDetail(DetailView):
    model = VacanciesModel
    template_name = "work/vacancies/detail.html"
    context_object_name = "vacancies"


""""""
