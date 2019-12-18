from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import smtplib
import json


@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        dicts = json.loads(data)
        sender = dicts['sender']
        recipient = dicts['recipient']
        password = dicts['password']
        subject = dicts['subject']
        text = dicts['text']
        try:
            smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            smtp_server.login(sender, password)
            message = "Subject: {}\n\n{}".format(subject, text)
            smtp_server.sendmail(sender, recipient, message)
            smtp_server.close()
            return JsonResponse({'status': 'ok'})
        except smtplib.SMTPAuthenticationError:
            return JsonResponse({'status': 'Проверьте натройки SMTP доступа почты или введенные данные'})
        except smtplib.SMTPSenderRefused:
            return JsonResponse({'status': 'Проверьте введенные данные'})
        finally:
            smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            smtp_server.close()
