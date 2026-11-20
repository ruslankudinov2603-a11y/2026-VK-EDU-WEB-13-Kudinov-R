from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.pagination import paginate
from .models import Question, Answer


def ask(request):
    return render(request, 'questions/ask.html')


def question(request, question_id):
    question = get_object_or_404(
        Question.objects.select_related('author').prefetch_related(
            'tags', 'likes'
        ),
        id=question_id,
    )

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Чтобы оставить ответ, необходимо войти.')
            return redirect('login')

        text = request.POST.get('answer', '').strip()

        if text:
            Answer.objects.create(
                question=question,
                author=request.user,
                text=text,
            )
            return redirect('question', question_id=question.id)

    answers = (
        Answer.objects
        .filter(question=question)
        .select_related('author')
        .prefetch_related('likes')
        .order_by('-created_at')
    )
    page_obj = paginate(answers, request)

    return render(request, 'questions/question.html', {
        'question': question,
        'answers': page_obj,
        'page_obj': page_obj,
    })
