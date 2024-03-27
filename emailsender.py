import os
from datetime import datetime
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

class EmailSender:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.year = datetime.now().year

    def send_email(self, receiver_email, subject, body):
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())

def send_bulk_emails():
    load_dotenv()

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    csv_file = os.getenv("CSV_FILE")
    subject = os.getenv("SUBJECT")
    template_file = os.getenv("TEMPLATE_FILE")
    email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_password)
    env = Environment(loader=FileSystemLoader("./"))
    template = env.get_template(template_file)

    with open(csv_file, "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            receiver_email = row["email"]
            body = template.render(row, year=email_sender.year)
            try:
                email_sender.send_email(receiver_email, subject, body)
                print(f'[ Ok ] -> {receiver_email}')
            except Exception as e:
                print(e)

if __name__ == "__main__":
    send_bulk_emails()
