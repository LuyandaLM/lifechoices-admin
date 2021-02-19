from decouple import config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def activate_email(user):
    host = 'smtp.gmail.com'
    port = 587
    username = config("LCS_ADMIN_PORTAL_GMAIL_USERNAME")
    password = config("LCS_ADMIN_PORTAL_GMAIL_PASSWORD")
    from_email = username
    to_list = user.email
    email_conn = smtplib.SMTP(host, port)
    email_conn.ehlo()
    start = email_conn.starttls()
    email_conn.login(username, password)
    msg = MIMEMultipart("alternative")
    msg['Subject'] = "ACCOUNT ACTIVATION"
    html = """\
    <html>
      <head></head>
      <body>
        <p>Hi!<br>
           How are you?<br>
           Here is the <a href="https://lifechoices-admin.herokuapp.com/user/login/">LOGIN</a> link.
        </p>
      </body>
    </html>
    """
    html_message = MIMEText(html, 'html')
    msg.attach(html_message)
    test = email_conn.sendmail(from_email, to_list, msg.as_string())
    stop = email_conn.quit()
