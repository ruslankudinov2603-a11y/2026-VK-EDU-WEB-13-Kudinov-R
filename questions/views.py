from django.shortcuts import render

# Create your views here.

def ask(request):
    return render(request, 'questions/ask.html')

def question(request , question_id):
    question = {
        'title': 'Как изучать Python?',
        'id': question_id,
        'text': 'С чего лучше начать изучение Python и Django?',
        'author': 'Ruslan',
        'answers': [
            {
                'text': 'Начни с основ Python, затем переходи к Django.',
                'author': 'Иван',
            },
            {
                'text': 'Лучше сразу писать небольшие проекты.',
                'author': 'Алексей',
            },
            {
                'text': 'Практикуйся каждый день и разбирай чужой код.',
                'author': 'Мария',
            },
        ],
    }

    return render(request, 'questions/question.html', {
        'question': question
    })

