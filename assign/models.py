from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# PDF-файл будет сохранен в директории homework_pdfs, созданной на основе поля slug объекта Homework
def upload_to(instance, filename):
    return f'homework_pdfs/{instance.slug}/{filename}'

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                      .filter(status=Homework.Status.PUBLISHED)
class Homework(models.Model):

    #статус публикации - опубликованный / не опубликованный
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='assign_homeworks')
    body = models.TextField()
    pdf = models.FileField(upload_to=upload_to, null=True, blank=True)

    publish = models.DateTimeField(default=timezone.now)  # поле дата публикации
    created = models.DateTimeField(auto_now_add=True)  # поле дата создания
    updated = models.DateTimeField(auto_now=True)  # поле дата изменения
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    tags = TaggableManager()

    #Для взаимодействия с ORM, с class PublishedManager
    objects = models.Manager() # менеджер, применяемый по умолчанию
    published = PublishedManager() # конкретно-прикладной менеджер

    #сортировка и индексация через дату публикации
    class Meta: #класс определяет метаданные модели.
        ordering = ['-publish'] #сортировка
        indexes = [
            models.Index(fields=['-publish']), #индексация
        ]

    def get_absolute_url(self):
        return reverse('assign:homework_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    homework = models.ForeignKey(Homework,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.homework}'

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class HomeworkSolution(models.Model):
    # Ссылка на домашнее задание
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='solutions')

    # Студент, отправивший решение
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homework_solutions')

    # Текстовый ответ обязателен
    answer_text = models.TextField()

    # PDF-файл необязателен
    answer_pdf = models.FileField(upload_to='homework_solutions/', null=True, blank=True)

    # Дата создания и обновления решения
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.homework.title} - {self.student.username}"


