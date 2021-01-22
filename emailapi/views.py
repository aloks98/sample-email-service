import os
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sendgrid import SendGridAPIClient
from mailjet_rest import Client

from .models import Email
from .serializers import EmailSerializer


def mailjet_email(sobject: EmailSerializer):
    api_key = os.environ.get('MAILJET_API_KEY')
    api_secret = os.environ.get('MAILJET_API_SECRET')
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    to_email = []
    cc_email = []
    for e in sobject.validated_data['to']:
        to_email.append({"email": e})
    for c in sobject.validated_data['cc']:
        cc_email.append({"email": c})
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "noreply@aloks.dev",
                    "Name": "aloks.dev NOREPLY"
                },
                "To": to_email,
                "Cc": cc_email,
                "Subject": sobject.validated_data['subject'],
                "HTMLPart": sobject.validated_data['email_text']
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.json())
    return result.status_code


def sendgrid_email(sobject: EmailSerializer):
    to_email = []
    cc_email = []
    for e in sobject.validated_data['to']:
        to_email.append({"email": e})
    for c in sobject.validated_data['cc']:
        cc_email.append({"email": c})
    data = {
        "from": {
            "email": "noreply@aloks.dev",
            "name": "aloks.dev NOREPLY"
        },
        "personalizations": [
            {
                "to": to_email,
                "subject": sobject.validated_data['subject'],
            }
        ],
        "content": [
            {
                "type": "text/html",
                "value": sobject.validated_data['email_text']
            }
        ]
    }
    print(len(cc_email))
    if len(cc_email) != 0:
        data["personalizations"] = [
            {
                "to": to_email,
                "cc": cc_email,
                "subject": sobject.validated_data['subject'],
            }
        ]

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg_response = sg.client.mail.send.post(request_body=data)
        return sg_response.status_code
    except Exception as e:
        print(e.message)


@api_view(['GET', 'POST'])
def email_functions(request, format=None):
    if request.method == 'GET':
        emails = Email.objects.all()
        email_serializer = EmailSerializer(emails, many=True)
        return Response(email_serializer.data)

    elif request.method == 'POST':
        email_serializer = EmailSerializer(data=request.data)
        if email_serializer.is_valid():
            print(email_serializer)
            sg_response = sendgrid_email(email_serializer)
            if sg_response == 202:
                email_serializer.save()
                return Response({
                    "message": "Email succesfully sent through Sendgrid.",
                    "status_code": "200"
                }, status.HTTP_200_OK)
            else:
                mj_response = mailjet_email(email_serializer)
                if mj_response != 200:
                    return Response({
                        "message": "Email couldn't be sent due to some error. ",
                        "status_code": mj_response
                    }, mj_response)
                else:
                    email_serializer.save()
                    return Response({
                        "message": "Email succesfully sent through Mailjet.",
                        "status_code": "200"
                    }, status.HTTP_200_OK)
        else:
            return Response(email_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def email_details(request, pk, format=None):
    try:
        email = Email.objects.get(pk=pk)
    except Email.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        email_serializer = EmailSerializer(email)
        return Response(email_serializer.data)
