from django.urls import path
from . import views

app_name = 'muiv_graduation_system'

urlpatterns = [
    # === Основные страницы ===
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),

    # === Авторизация ===
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/<str:role>/', views.RegisterAsView.as_view(), name='register_as'),

    # === Профиль ===
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # === Выпускник ===
    path('graduate/edit/', views.EditGraduateView.as_view(), name='edit_graduate'),
    path('graduate/export/docx/', views.ExportMyDataView.as_view(), name='export_my_data_docx'),

    # === Менеджер: выпускники ===
    path('manager/graduates/', views.ManagerGraduatesView.as_view(), name='manager_graduates'),
    path('manager/graduates/<int:grad_id>/edit/', views.EditGraduateByManagerView.as_view(), name='edit_graduate_by_manager'),

    # === Поиск и экспорт ===
    path('manager/search/', views.SearchGraduatesView.as_view(), name='search_graduates'),
    path('manager/export/<str:format>/', views.ExportSearchResultsView.as_view(), name='export_search_results'),

    # === Отчёты ===
    path('reports/', views.ReportsView.as_view(), name='reports'),
]