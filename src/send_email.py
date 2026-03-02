"""
Module to send surf report emails
"""

import logging
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.settings import EmailSettings

logger = logging.getLogger(__name__)


def send_user_email():
    """
    Fetches the current surf report via curl and sends it as an email.
    """
    env = EmailSettings()

    message = MIMEMultipart()
    message["From"] = env.EMAIL
    message["To"] = env.EMAIL_RECEIVER
    message["Subject"] = env.SUBJECT

    try:
        result = subprocess.run(
            ["curl", env.COMMAND],
            capture_output=True,
            text=True,
            check=True,
        )
        body = result.stdout
    except subprocess.CalledProcessError as e:
        logger.error("Failed to fetch surf report via curl: %s", e.stderr)
        body = "Failed to fetch surf report."

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(env.SMTP_SERVER, env.SMTP_PORT) as server:
        server.starttls()
        server.login(env.EMAIL, env.EMAIL_PW)
        server.sendmail(env.EMAIL, env.EMAIL_RECEIVER, message.as_string())
        logger.info("Email sent successfully.")


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    send_user_email()
