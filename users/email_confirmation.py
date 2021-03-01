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
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="http://fonts.cdnfonts.com/css/epilogue-2" rel="stylesheet">
    <style>
        @import url('http://fonts.cdnfonts.com/css/epilogue-2');
        
        .page{
            font-family: 'Epilogue', sans-serif;
            padding-top: 30px;
        } 
        #footer{
            background: black;
            position: absolute;
            bottom: 0px;       
            margin-top:20px    
        }
        
        #foottext{
            color: white;
        }
        .center {
            margin: auto;
            width: 100%;  
            padding: 10px;
            }
            #imgid {   
             width: 30%;
             }
         .login {
             background: #abcc37;
            height: 40px;
            width: 150px;
            border: none;
            border-radius: 10px;
         }
    </style>
    <title>confirm</title>
    </head>
    <body>
        <div class="page">
             <center>
                 <div><img src="https://media-private.canva.com/QIHEU/MADG2sQIHEU/2/s.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH4JWSMIDQ%2F20210219%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20210219T081028Z&X-Amz-Expires=28794&X-Amz-Signature=1b7aac6b2b9d011c937c3aa0f2fe3368469bb2a910baae178537af3d84372b23&X-Amz-SignedHeaders=host&response-expires=Fri%2C%2019%20Feb%202021%2016%3A10%3A22%20GMT" id="imgid"/></div>
                 <h4>
                Your account has been successfully activated!
            </h4>
                <p>
                Your registration with our admin app has been completed.
            </p><a href="https://lifechoices-admin.herokuapp.com/user/login/">
            <button class="login" >Log in</button></a>
               </center>
                
               <div class='center' id='footer'>
                <center><img src="https://www.lifechoices.co.za/themes/lifechoices/images/assets/logo/logo_429x99.png" id="imgid"/>
                <p id="foottext">INVESTING IN YOUTH TO TACKLE INEQUALITY</p></center>
               </div>
        </div>  
    </body>
    </html>
    """
    html_message = MIMEText(html, 'html')
    msg.attach(html_message)
    test = email_conn.sendmail(from_email, to_list, msg.as_string())
    stop = email_conn.quit()
