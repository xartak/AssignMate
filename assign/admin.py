from django.contrib import admin
from .models import Homework, Comment
from .models import HomeworkSolution

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author'] #фильтрация в боковой панели
    search_fields = ['title', 'body'] #поля, по которым можно осуществить поиск
    prepopulated_fields = {'slug': ('title',)} #slug = title
    raw_id_fields = ['author'] #поле author отображается поисковым виджетом
    autocomplete_fields = ['author'] #критерий сортировки по статусу
    date_hierarchy = 'publish' #навигация по иерархии дат
    ordering = ['status', 'publish']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'homework', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']

@admin.register(HomeworkSolution)
class HomeworkSolutionAdmin(admin.ModelAdmin):
    list_display = ['homework', 'student', 'created', 'updated']
    list_filter = ['created', 'updated', 'student']
    search_fields = ['answer_text', 'homework__title']