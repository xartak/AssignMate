from django.shortcuts import render, get_object_or_404, redirect
from .models import Homework, Comment, HomeworkSolution
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailHomeworkForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth.decorators import login_required

"""
#Альтернативное представление списка постов

class HomeworkListView(ListView):

    queryset = Homework.published.all()
    context_object_name = 'homeworks'
    paginate_by = 3
    template_name = 'assign/homework/list.html'
"""
def is_student(user):
    return hasattr(user, 'profile') and user.profile.role == 'student'

def is_teacher(user):
    return hasattr(user, 'profile') and user.profile.role == 'teacher'

def homework_list(request, tag_slug=None):
    homework_list = Homework.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        homework_list = homework_list.filter(tags__in=[tag])

    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(homework_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        homeworks = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        homeworks = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу результатов
        homeworks = paginator.page(paginator.num_pages)
    return render(request,
                  'assign/homework/list.html',
                  {'homeworks': homeworks,
                   'tag': tag})


def homework_detail(request, year, month, day, homework):
    homework = get_object_or_404(Homework,
                             status=Homework.Status.PUBLISHED,
                             slug=homework,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # Список активных комментариев к этому посту
    comments = homework.comments.filter(active=True)
    # Форма для комментирования пользователями
    form = CommentForm()


    homework_tags_ids = homework.tags.values_list('id', flat=True)
    similar_homeworks = Homework.published.filter(tags__in=homework_tags_ids) \
        .exclude(id=homework.id)
    similar_homeworks = similar_homeworks.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]

    solutions = None
    can_submit_solution = False  # Значение по умолчанию для переменной

    if is_teacher(request.user):
        solutions = homework.solutions.all()
    elif is_student(request.user):
        solutions = homework.solutions.filter(student=request.user)
        can_submit_solution = not solutions.exists()

    return render(request,
                  'assign/homework/detail.html',
                  {'homework': homework,
                   'comments': comments,
                   'form': form,
                   'similar_homeworks': similar_homeworks,
                   'solutions': solutions,
                   'can_submit_solution': can_submit_solution
                   })

def homework_share(request, homework_id):
    # Извлечь пост по его идентификатору id
    homework = get_object_or_404(Homework,
                             id=homework_id,
                             status=Homework.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailHomeworkForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            homework_url = request.build_absolute_url(
                homework.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{homework.title}"
            message = f"Read {homework.title} at {homework_url}\n\n" \
                      f"{cd['name']}\'s ({cd['email']}) comments: {cd['comments']}"
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      [cd['to']])
            sent = True
    else:
        form = EmailHomeworkForm()
    return render(request, 'assign/homework/share.html', {'homework': homework,
                                                    'form': form,
                                                    'sent': sent})

@require_POST
def homework_comment(request, homework_id):
    homework = get_object_or_404(Homework,
                             id=homework_id,
                             status=Homework.Status.PUBLISHED)
    comment = None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.homework = homework
        # Сохранить комментарий в базе данных
        comment.save()
    return render(request, 'assign/homework/comment.html',
                  {'homework': homework,
                   'form': form,
                   'comment': comment})

@login_required
def submit_solution(request, homework_id):
    homework = get_object_or_404(Homework, id=homework_id)
    if not is_student(request.user):
        return redirect('')  # или страница ошибки

    if request.method == 'POST':
        answer_text = request.POST.get('answer_text')
        answer_pdf = request.FILES.get('answer_pdf', None)

        solution = HomeworkSolution(homework=homework, student=request.user, answer_text=answer_text,
                                    answer_pdf=answer_pdf)
        solution.save()

        return redirect(homework.get_absolute_url())  # Редирект на страницу домашнего задания

    return render(request, 'assign/homework/submit_solution.html', {'homework': homework})

@login_required
def delete_solution(request, solution_id):
    solution = get_object_or_404(HomeworkSolution, id=solution_id, student=request.user)
    if request.method == 'POST':
        solution.delete()
        return redirect('assign:homework_list')  # Или другой URL, куда нужно перейти после удаления
    else:
        return render(request, 'assign/homework/confirm_delete.html', {
            'solution': solution,
            'homework': solution.homework  # Добавляем объект homework в контекст
        })