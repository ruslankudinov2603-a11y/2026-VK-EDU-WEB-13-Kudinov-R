from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from questions.models import Question, Answer, Tag, QuestionLike, AnswerLike
from .pagination import paginate
from .forms import RegistrationForm, ProfileForm, QuestionForm, AnswerForm
from core.models import Profile

def index(request):
    questions = Question.objects.newest().select_related('author').prefetch_related('tags')
    page_obj = paginate(questions, request)
    return render(request, 'core/index.html', {'questions': page_obj, 'page_obj': page_obj})


def login(request):
    next_url = request.POST.get('next') or request.GET.get('next') or '/'

    if not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = '/'

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect(next_url)

        messages.error(request, 'Неверный логин или пароль.')
    return render(request, 'core/login.html', {'next': next_url})


def logout(request):
    auth_logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'core/signup.html', {'form': form})


@login_required
def profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        user_data = {
            'email': request.POST.get('email', ''),
            'first_name': request.POST.get('first_name', ''),
            'last_name': request.POST.get('last_name', ''),
        }

        if profile_form.is_valid():
            request.user.first_name = user_data['first_name'].strip()
            request.user.last_name = user_data['last_name'].strip()
            request.user.email = user_data['email'].strip()
            request.user.save()

            profile_form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('profile')

    else:
        profile_form = ProfileForm(instance=profile)
        user_data = {
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

    return render(request, 'core/profile.html', {
        'profile_form': profile_form,
        'profile': profile,
        'user_data': user_data,
    })


def hot(request):
    questions = Question.objects.popular().select_related('author').prefetch_related('tags')
    page_obj = paginate(questions, request)
    return render(request, 'core/hot.html', {'questions': page_obj, 'page_obj': page_obj})


def tag(request, tag_name):
    tag = get_object_or_404(Tag, slug=tag_name)
    questions = tag.questions.with_counts().select_related('author').prefetch_related('tags')
    questions = questions.order_by('-created_at')
    page_obj = paginate(questions, request)
    return render(request, 'core/tag.html', {
        'questions': page_obj,
        'page_obj': page_obj,
        'tag_name': tag.name,
    })


@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            form.save_m2m()
            return redirect('question', question_id=question.id)
    else:
        form = QuestionForm()

    return render(request, 'questions/ask.html', {'form': form})


def question(request, question_id):
    question = get_object_or_404(
        Question.objects.select_related('author').prefetch_related('tags', 'answers__author'),
        id=question_id
    )

    if request.method == 'POST' and request.user.is_authenticated:
        form = AnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect(
                f"{redirect('question', question_id=question.id).url}#answer-{answer.id}"
            )
    else:
        form = AnswerForm()

    question.likes_count = question.likes.filter(value=1).count()
    question.dislikes_count = question.likes.filter(value=-1).count()

    for answer in question.answers.all():
        answer.likes_count = answer.likes.filter(value=1).count()
        answer.dislikes_count = answer.likes.filter(value=-1).count()

    return render(request, 'questions/question.html', {
        'question': question,
        'answers': question.answers.all(),
        'form': form,
    })



@require_POST
@login_required
def question_like(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    value = int(request.POST.get('value', 1))

    if value not in (1, -1):
        return JsonResponse({'error': 'Некорректный голос'}, status=400)

    vote, created = QuestionLike.objects.get_or_create(
        user=request.user,
        question=question,
        defaults={'value': value}
    )

    if not created:
        if vote.value == value:
            vote.delete()
        else:
            vote.value = value
            vote.save(update_fields=['value'])

    return JsonResponse({
        'likes_count': question.likes.filter(value=1).count(),
        'dislikes_count': question.likes.filter(value=-1).count(),
    })

@require_POST
@login_required
def answer_like(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)

    value = int(request.POST.get('value', 1))

    if value not in (1, -1):
        return JsonResponse({'error': 'Некорректный голос'}, status=400)

    vote, created = AnswerLike.objects.get_or_create(
        user=request.user,
        answer=answer,
        defaults={'value': value}
    )

    if not created:
        if vote.value == value:
            vote.delete()
        else:
            vote.value = value
            vote.save(update_fields=['value'])

    return JsonResponse({
        'likes_count': answer.likes.filter(value=1).count(),
        'dislikes_count': answer.likes.filter(value=-1).count(),
    })


@require_POST
@login_required
def mark_correct(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)

    if answer.question.author != request.user:
        return JsonResponse({
            'success': False,
            'error': 'Нет прав на изменение этого ответа.'
        }, status=403)

    answer.is_correct = not answer.is_correct
    answer.save(update_fields=['is_correct'])

    return JsonResponse({
        'success': True,
        'is_correct': answer.is_correct,
    })