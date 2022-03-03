from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from users.models import CustomUser

# @receiver(post_save, sender=CustomUser)
# def send_welcome_email(sender, instance, created, **kwargs):
#     if created:
#         send_mail(
#     #         "Welcome to goodreads clone",
#     #         f"Hi, {instance.username}. Wlcome to Goodreads clone enjoy and relax with readeing",
#     #         'faridtinchlikov@gmail.com',
#     #         [instance.email]
#             print('email send')
#         )

