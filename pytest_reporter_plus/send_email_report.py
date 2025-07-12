import os
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid

import shutil

def zip_report_folder(folder_path: str, output_zip: str):
    shutil.make_archive(output_zip.replace(".zip", ""), 'zip', folder_path)
    return output_zip

def load_email_env(filepath="emailenv"):
    if not os.path.exists(filepath):
        raise FileNotFoundError("emailenv file not found!")

    config = {}
    with open(filepath, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                config[key.strip()] = value.strip()
    return config

def send_email_from_env(config: dict):
    sender = config["sender_email"]
    recipient = config["recipient_email"]
    report_path = config["report_path"]
    subject = config["subject"]
    smtp_server = config["smtp_server"]
    smtp_port = int(config["smtp_port"])
    password = config["email_password"]
    use_tls = True

    zip_path = zip_report_folder(report_path, f"{report_path}_zipped" + ".zip")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    msg.set_content("Your test report is attached as an HTML file.")

    filename = os.path.basename(zip_path)
    with open(zip_path, "rb") as f:
        report_data = f.read()
    msg.add_attachment(report_data, maintype="application", subtype="zip", filename=filename)

    try:
        if "sendgrid" in smtp_server.lower():
            if not password.startswith("SG."):
                print("****************************************************************")
                print("SendGrid API key looks invalid. It should start with 'SG.'")
                print("****************************************************************")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            if use_tls:
                server.starttls()
            login_user = "apikey" if "sendgrid" in smtp_server.lower() else sender
            server.login(login_user, password)
            server.send_message(msg)
            print("****************************************************************")
            print(f"{subject} is sent to {recipient} from {sender} successfully with attachment: {filename}")
            print("****************************************************************")
    except Exception as e:
        raise RuntimeError(f"Failed to send email: {e}") from e
