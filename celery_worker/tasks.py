from celery import Celery
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize Celery
app = Celery('tasks', broker='redis://redis:6379/0')

# Define the task for sending alerts
@app.task
def send_alert(error_rate, total_requests):
    sender_email = "your-email@example.com"
    receiver_email = "alert-receiver@example.com"
    password = "your-email-password"

    subject = "High Error Rate Detected"
    body = f"High error rate detected!\n\nError Rate: {error_rate}\nTotal Requests: {total_requests}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.example.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.close()
    except Exception as e:
        print(f"Error sending alert email: {e}")
