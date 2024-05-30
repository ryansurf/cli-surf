"""
Module to send surf report emails
"""

import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.settings import EmailSettings

# Load environment variables from .env file
env = EmailSettings()

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = env.EMAIL
message["To"] = env.EMAIL_RECEIVER
message["Subject"] = env.SUBJECT


def send_user_email():
    """
    Sends user an email
    """
    SURF = subprocess.run(
        ["curl", env.COMMAND],
        capture_output=True,
        text=True,
        check=True,
    )
    if SURF.returncode == 0:  # Check if command executed successfully
        BODY = SURF.stdout
    else:
        BODY = "Failed to execute curl command."
    message.attach(MIMEText(BODY, "plain"))

    # Connect to the SMTP server
    with smtplib.SMTP(env.SMTP_SERVER, env.SMTP_PORT) as server:
        server.starttls()  # Secure the connection
        server.login(env.EMAIL, env.EMAIL_PW)
        text = message.as_string()
        server.sendmail(env.EMAIL, env.EMAIL_RECEIVER, text)
        print("Email sent successfully.")


if __name__ == "__main__":
    send_user_email()
