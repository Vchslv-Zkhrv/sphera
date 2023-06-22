import smtplib as _smtplib
import ssl as _ssl
from email.mime.text import MIMEText as _MIMEText
from email.mime.multipart import MIMEMultipart as _MIMEMultipart

from config import SMTP_LOGIN, SMTP_APPLICATION_PASSWORD


email = "vchslv.zkhrv@gmail.com"


html = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
 <head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 600px; width: 600px">
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; background-color: yellowgreen; color: white; font-weight: 800; gap: 24px; border-radius: 12px; max-height: 300px, max-width: 400px">
        <p>Проверьте правильность логина и пароля</p>
        <a style="display: block; background-color: white; border-radius: 5px; color: rgb(30,30,30); padding: 12px; text-decoration: none; heidht: fit-content" href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">Ссылка</a>
    </div>
</body>
</html>
"""


def test():

    msg = _MIMEMultipart()
    msg["From"] = SMTP_LOGIN
    msg["To"] = SMTP_LOGIN
    msg["Subject"] = "Подтвердите создание аккаунта на платфоре Сфера"
    msg["Bcc"] = SMTP_LOGIN

    payload = _MIMEText(html, "HTML", "UTF-8")

    msg.attach(payload)

    context = _ssl.create_default_context()

    with _smtplib.SMTP_SSL("smtp.yandex.ru", 465, timeout=5, context=context) as server:
        server.ehlo()
        server.login(SMTP_LOGIN, SMTP_APPLICATION_PASSWORD)
        server.sendmail(SMTP_LOGIN, email, msg.as_string())

    print("sended")


test()
