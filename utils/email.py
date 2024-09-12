import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from .protect import get_env_variable


def send_email(subject, body, to_email):
    

    EXEMPLE_EMAIL_DEV = get_env_variable('EXEMPLE_EMAIL_DEV')
    EXEMPLE_EMAIL_PASSWORD = get_env_variable('EXEMPLE_EMAIL_PASSWORD')


    server = smtplib.SMTP(host="smtp.gmail.com", port=587)
    server.starttls()
    server.login(EXEMPLE_EMAIL_DEV, EXEMPLE_EMAIL_PASSWORD)

    # Create the email
    msg = MIMEMultipart()
    msg["From"] = EXEMPLE_EMAIL_DEV
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Send the email and close the connection
    try:
        server.send_message(msg)
        logging.info("Email sent successfully")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        raise Exception(f"Failed to send email: {e}")  
    finally:
        server.quit()