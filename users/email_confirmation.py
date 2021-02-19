from decouple import config
import smtplib


def activate_email(activate_account, email_address):
    host = 'smtp.gmail.com'
    port = 587
    username = config("LCS_ADMIN_PORTAL_GMAIL_USERNAME")
    password = config("LCS_ADMIN_PORTAL_GMAIL_PASSWORD")
    from_email = username
    to_list = email_address
    email_conn = smtplib.SMTP(host, port)
    email_conn.ehlo()
    start = email_conn.starttls()
    email_conn.login(username, password)

    if activate_account:
        email_message: str = "Your account has successfully been activated."
    elif not activate_account:
        email_message: str = "Your account was not successfully activated."
    test = email_conn.sendmail(from_email, to_list, email_message)
    stop = email_conn.quit()
