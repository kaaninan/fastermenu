# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC0de3aa6706093cb5e419c19c5996300b'
auth_token = 'f30686f7b9c4b737199432f2a407a8e6'
client = Client(account_sid, auth_token)

message = client.messages.create(
                              from_='+12014313833',
                              body='body',
                              to='+905309263819'
                          )

print(message.sid)
