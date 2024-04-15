from django.urls import path
from . import views

app_name = 'assign'

urlpatterns = [
    path('', views.homework_list, name='homework_list'),
   # path('', views.HomeworkListView.as_view(), name='homework_list'),

    path('tag/<slug:tag_slug>/',
         views.homework_list, name='homework_list_by_tag'),

    path('<int:year>/<int:month>/<int:day>/<slug:homework>/',
         views.homework_detail,
         name='homework_detail'),

    path('<int:homework_id>/share/',
         views.homework_share, name='homework_share'),

    path('<int:homework_id>/comment/',
         views.homework_comment, name='homework_comment'),

    path('<int:homework_id>/submit/',
         views.submit_solution, name='submit_solution'),

    path('solution/delete/<int:solution_id>/',
         views.delete_solution, name='delete_solution'),

]