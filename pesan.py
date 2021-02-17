# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC1e56f4800694e2c370589989aead1b71'
auth_token = '486802a7ea66b8d6d55123d22ee36b4c'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
		     messagingServiceSid='VA3943c7296c2357360c0530f42d4c932a',
                     from_='+15017122661',
                     to='+6288297537306'
                 )

print(message.sid)
