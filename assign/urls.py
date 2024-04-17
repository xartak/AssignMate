from django.urls import path
from . import views
from .views import add_homework

app_name = 'assign'

urlpatterns = [
    path('', views.courses_list,
         name='courses_list'),  # Список всех домашних заданий, доступных пользователю

    path('courses/<int:pk>/',
         views.course_detail, name='course_detail'),

    path('tag/<slug:tag_slug>/',
         views.homework_list, name='homework_list_by_tag'),  # Фильтрация домашних заданий по тегу

    path('<int:year>/<int:month>/<int:day>/<slug:homework_slug>/',
         views.homework_detail,
         name='homework_detail'),

    path('<int:homework_id>/share/',
         views.homework_share, name='homework_share'),  # Поделиться домашним заданием

    path('<int:homework_id>/comment/',
         views.homework_comment, name='homework_comment'),  # Комментирование домашнего задания

    path('<int:homework_id>/submit/',
         views.submit_solution, name='submit_solution'),  # Отправка решения по домашнему заданию

    path('solution/delete/<int:solution_id>/',
         views.delete_solution, name='delete_solution'),  # Удаление решения домашнего задания

    path('add_homework/',
         add_homework, name='add_homework'),

    path('homeworks/', views.homework_list, name='homework_list'),

    path('homework/<int:homework_id>/delete/',
         views.delete_homework, name='delete_homework'),
]
