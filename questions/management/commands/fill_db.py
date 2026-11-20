import random

from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import transaction

from core.models import Profile
from questions.models import (
    Question,
    Answer,
    Tag,
    QuestionLike,
    AnswerLike,
)


fake = Faker('ru_RU')
BATCH_SIZE = 5000


def bulk_insert(model, objects):
    """Сохраняет объекты пакетами."""
    objects = list(objects)

    for start in range(0, len(objects), BATCH_SIZE):
        model.objects.bulk_create(
            objects[start:start + BATCH_SIZE],
            batch_size=BATCH_SIZE
        )


class Command(BaseCommand):
    help = 'Заполнение базы тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        ratio = options['ratio']

        if ratio < 1:
            raise CommandError('Ratio должен быть положительным числом')

        user_count = ratio
        question_count = ratio * 10
        answer_count = ratio * 100
        tag_count = ratio
        likes_per_type = ratio * 100

        self.stdout.write('Создание пользователей...')

        users = [
            User(
                username=f'user_{i}',
                email=f'user_{i}@example.com',
                password='!'
            )
            for i in range(user_count)
        ]
        bulk_insert(User, users)
        users = list(User.objects.filter(
            username__startswith='user_'
        ).order_by('id'))

        bulk_insert(
            Profile,
            [Profile(user=user) for user in users]
        )

        self.stdout.write('Создание тегов...')

        tags = [
            Tag(
                name=fake.unique.word(),
                slug=f'tag-{i}'
            )
            for i in range(tag_count)
        ]
        bulk_insert(Tag, tags)
        tags = list(Tag.objects.filter(
            slug__startswith='tag-'
        ).order_by('id'))

        self.stdout.write('Создание вопросов...')

        questions = [
            Question(
                title=fake.sentence(nb_words=8),
                text=fake.paragraph(nb_sentences=5),
                author=users[i % user_count]
            )
            for i in range(question_count)
        ]
        bulk_insert(Question, questions)

        questions = list(
            Question.objects.order_by('id')[
                :question_count
            ]
        )

        self.stdout.write('Создание ответов...')

        answers = [
            Answer(
                question=questions[i % question_count],
                author=users[i % user_count],
                text=fake.paragraph(nb_sentences=3)
            )
            for i in range(answer_count)
        ]
        bulk_insert(Answer, answers)

        answer_objects = list(
            Answer.objects.order_by('id')[:answer_count]
        )

        self.stdout.write('Связывание вопросов с тегами...')

        through = Question.tags.through
        relations = []

        for question in questions:
            selected_tags = random.sample(
                tags,
                min(len(tags), random.randint(1, 3))
            )
            relations.extend([
                through(question_id=question.id, tag_id=tag.id)
                for tag in selected_tags
            ])

            if len(relations) >= BATCH_SIZE:
                bulk_insert(through, relations)
                relations.clear()

        if relations:
            bulk_insert(through, relations)

        self.stdout.write('Создание лайков вопросов...')

        question_likes = [
            QuestionLike(
                user=users[i % user_count],
                question=questions[
                    (i // user_count + (i % user_count) * 101)
                    % question_count
                ]
            )
            for i in range(likes_per_type)
        ]
        bulk_insert(QuestionLike, question_likes)

        self.stdout.write('Создание лайков ответов...')

        answer_likes = [
            AnswerLike(
                user=users[i % user_count],
                answer=answer_objects[
                    (i // user_count + (i % user_count) * 101)
                    % answer_count
                ]
            )
            for i in range(likes_per_type)
        ]
        bulk_insert(AnswerLike, answer_likes)

        self.stdout.write(self.style.SUCCESS(
            f'База заполнена! Пользователей: {user_count}, '
            f'вопросов: {question_count}, '
            f'ответов: {answer_count}, '
            f'тегов: {tag_count}, '
            f'лайков: {likes_per_type * 2}.'
        ))
