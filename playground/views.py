from django.core.mail import send_mail, mail_admins, EmailMessage
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers

def say_hello(request):
    notify_customers.delay('Hi man')
    return render(request,'hello.html',{'name':'Abdullah'})

def senEmail(request):
    try:
        # send_mail('test', "I'm Just testing", 'sender@store.com', ['resevers@store.com'])

        # mail_admins('test', "I'm Just testing", html_message="<p>Welcome back</p>")

        # message = EmailMessage('test', "I'm Just testing", 'sender@store.com', ['resevers@store.com'])
        # message.attach_file('playground/static/images/my_image.png')
        # message.send()

        message = BaseEmailMessage(
            template_name="emails/helloMail.html",
            context={'name':"Abdullah"}
        )
        message.send(['resevers@store.com'])
    except ValueError:
        pass
    return render(request, 'hello.html', {'name': 'Mosh'})
