import smtplib
from email.message import EmailMessage

def send_email(to: str, subject: str, body: str):
    sender_email = "your_email@outlook.com"
    sender_password = "your_app_password"  # Outlook App Password, NOT your login password

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to
    msg.set_content(body)

    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
