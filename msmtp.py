import smtplib, ssl
from email.message import EmailMessage
from config import mailidpass

def sendmail(umail):
    try:
        port = 465  # For SSL
        smtp_server = "smtpout.secureserver.net"
        sender_email = "rudra.shah@rudrashah.in"
        receiver_email = umail 
        password = mailidpass

        msg = EmailMessage()
        msg.set_content("Hello Test")

        msg['Subject'] = "Thank You for registering in HackNUThon 4.0 !!"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)
        return "Sent"
    except:
        return "Error"

sendmail("panktichawda06@gmail.com")