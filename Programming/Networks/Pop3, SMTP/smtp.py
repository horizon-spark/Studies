from smtplib import SMTP_SSL

host = 'smtp.mail.ru'
port = 465

user = 'kadarmetov.dn@mail.ru'
password = open('password.txt').readline()
to = "kozinets.egor@gmail.com"

with SMTP_SSL(host, port) as smtp:
    print(smtp.ehlo())
    print(smtp.login(user, password))
    print(smtp.sendmail(user, to, "KadarmetovDN"))