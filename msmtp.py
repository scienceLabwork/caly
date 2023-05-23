import smtplib, ssl
from email.message import EmailMessage
from config import mailidpass

def sendmail(umail,uname,resetlink):
    try:
        port = 465  # For SSL
        smtp_server = "smtpout.secureserver.net"
        sender_email = "rudra.shah@rudrashah.in"
        receiver_email = umail 
        password = mailidpass

        msg = EmailMessage()
        msg.set_content(
f"""
Dear {uname},

We have received a request to reset your password for your caly account. We understand that forgetting passwords happens to the best of us, so we're here to help you regain access to your account.

To reset your password, please follow the instructions below:

Visit the caly password reset page by clicking on the following link: {resetlink}
You will be directed to a page where you can enter your new password. Choose a strong and unique password that you haven't used before.
After entering your new password, click on the "Reset Password" button to save your changes.
Please note that for security purposes, this password reset link will expire after 2 hour. If you do not reset your password within this time frame, you will need to request a new password reset.

If you did not request this password reset or believe it to be a mistake, please disregard this email. Your account security is important to us, and we recommend taking necessary precautions such as changing your password regularly and not sharing it with anyone.

If you require any further assistance or have any questions, please feel free to reach out to our support team at [support email address]. We're always here to help!

Thank you for using caly. We appreciate your trust in us.

Best regards,
Team Caly
""")

        msg['Subject'] = "Reset Your Password - Caly"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)
        return "Sent"
    except:
        return "Error"

tlink = "samplelinkwouldbehere"
sendmail("panktichawda06@gmail.com","Pankti",tlink)