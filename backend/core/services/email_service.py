import os
import random

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from configs.celery import app

from core.dataclasses.user_dataclass import User
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken

UserModel = get_user_model()



class EmailService:
    @staticmethod
    @app.task
    def __send_email(to: str, template_name: str, context: dict, subject: str):
        template = get_template(template_name)
        html_context = template.render(context)
        msg = EmailMultiAlternatives(subject=subject, from_email=os.environ.get('EMAIL_HOST_USER'), to=[to])
        msg.attach_alternative(html_context, 'text/html')
        msg.send()

    @classmethod
    def send_test(cls):
        cls.__send_email('anastasiia.mirovska@gmail.com', 'test.html', {}, 'Test Email')

    @classmethod
    def register_email(cls, user: User):
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost:3000/activate/{token}'
        cls.__send_email.delay(
            user.email,
            template_name='register.html',
            context={'name': user.profile.name, 'url': url},
            subject='Register'
        )

    @classmethod
    def recovery_email(cls, user: User):
        token = JWTService.create_token(user, RecoveryToken)
        url = f'http://localhost:3000/recovery/{token}'
        cls.__send_email(user.email, 'recovery.html', {'url': url}, 'Recovery password')

    @classmethod
    def check_bad_words_email(cls, user_id: int, car_id: int):
        managers = UserModel.objects.filter(is_active=True, is_staff=True, is_superuser=False)
        manager = random.choice(managers)

        cls.__send_email(manager.email, 'bad_words.html', {'user_id': f'{user_id}', 'car_id': f'{car_id}'}, 'Bad words detected')

