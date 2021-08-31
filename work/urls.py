from django.urls import path, re_path
from work import views

urlpatterns = [
    path('resumes/', views.ResumesView.as_view(), name="resumes"),
    path('resumes/create', views.ResumesCreate.as_view(), name="create_resume"),
    path('resumes/<slug:pk>', views.ResumesDetail.as_view(), name="check_resume"),
    path('resumes/update/', views.redirect_update_resumes, name="update_resume"),
    path('resumes/update/<slug:pk>', views.ResumesUpdate.as_view(), name="update_my_resume"),
    path('resumes/delete/', views.redirect_delete_resumes, name="delete_resume"),
    path('resumes/delete/<slug:pk>', views.ResumesDelete.as_view(), name="delete_my_resume"),

    path('resumes/check/', views.redirect_to_my_resume, name="redirect_to_my_resume"),

    path('resumes/<int:user_id>/get_contact_resume', views.get_contacts_resume),
    path('vacancies/<int:vac_id>/get_contact_vac', views.get_contacts_vacancies),

    path('vacancies/', views.VacanciesView.as_view(), name="vacancies"),
    path('vacancies/<slug:pk>', views.VacanciesDetail.as_view(), name="check_vacancies"),
]
