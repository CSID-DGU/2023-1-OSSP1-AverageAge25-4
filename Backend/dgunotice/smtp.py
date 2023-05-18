import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

# 수신자
recipients = ["수신자1","수신자2"]

message = MIMEMultipart();
message['Subject'] = '동국대 메일 알림 테스트'
message['From'] = "발신자"
message['To'] = ",".join(recipients)

title = "부제목"
body = "내용"

content = """
    <html>
    <body>
        <h2>{}</h2>
        <p> {} </p>
    </body>
    </html>
""".format(title, body)

mimetext = MIMEText(content,'html')
message.attach(mimetext)

email_id = '아이디'
email_pw = '비밀번호'

server = smtplib.SMTP('smtp.naver.com',587)
server.ehlo()
server.starttls()
server.login(email_id,email_pw)
server.sendmail(message['From'],recipients,message.as_string())
server.quit()