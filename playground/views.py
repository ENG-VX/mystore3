from django.core.mail import send_mail, mail_admins, EmailMessage
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
import requests
import logging

logger = logging.getLogger(__name__)

class HelloView(APIView):
    def get(self, request):
        try:
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('received the response')
            data = response.json()
        except requests.ConnectionError:
            logger.critical('httpbin is offline')
        return render(request, 'playground/hello.html', {'name': 'Abdullah'})


# @cache_page(10*60)
# def say_hello(request):
#     response = requests.get('https://httpbin.org/delay/2')
#     data = response.json()
#     return render(request, 'playground/hello.html', {'name': data})

# def senEmail(request):
#     try:
#         # send_mail('test', "I'm Just testing", 'sender@store.com', ['resevers@store.com'])

#         # mail_admins('test', "I'm Just testing", html_message="<p>Welcome back</p>")

#         # message = EmailMessage('test', "I'm Just testing", 'sender@store.com', ['resevers@store.com'])
#         # message.attach_file('static/playground/images/my_image.png')
#         # message.send()

#         message = BaseEmailMessage(
#             template_name="playground/emails/helloMail.html",
#             context={'name':"Abdullah"}
#         )
#         message.send(['resevers@store.com'])
#     except ValueError:
#         pass
#     return render(request, 'playground/hello.html', {'name': 'Mosh'})
