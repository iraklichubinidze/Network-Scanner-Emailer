import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(smtp_server, smtp_port, smtp_login, smtp_password, sender_email, receiver_emails, html_file):
    with open(html_file, 'r') as f:
        html_content = f.read()

    message = MIMEMultipart("alternative")
    message["Subject"] = "Daily NetScan"
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_emails)

    part = MIMEText(html_content, "html")
    message.attach(part)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_login, smtp_password)
            server.sendmail(sender_email, receiver_emails, message.as_string())
        print("Email alert sent successfully.")
    except Exception as e:
        print(f"Failed to send email alert: {e}")
