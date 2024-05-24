"""
Module to send surf report emails
"""

import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Email server configuration
SMTP_SERVER = os.getenv("SMTP_SERVER")
PORT = 587  # Port for TLS connection

# Sender's email credentials
SENDER_EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PW")

# Receiver's email
RECEIVER_EMAIL = os.getenv("EMAIL_RECEIVER")

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = SENDER_EMAIL
message["To"] = RECEIVER_EMAIL
message["Subject"] = os.getenv("SUBJECT")


def send_user_email():
    """
    Sends user an email
    """
    SURF = subprocess.run(
        ["curl", os.getenv("COMMAND")], capture_output=True, text=True, check=True
    )
    if SURF.returncode == 0:  # Check if command executed successfully
        BODY = SURF.stdout
    else:
        BODY = "Failed to execute curl command."
    message.attach(MIMEText(BODY, "plain"))

    # Connect to the SMTP server
    with smtplib.SMTP(SMTP_SERVER, PORT) as server:
        server.starttls()  # Secure the connection
        server.login(SENDER_EMAIL, PASSWORD)
        text = message.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        print("Email sent successfully.")


send_user_email()
