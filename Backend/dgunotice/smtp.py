from pathlib import Path
import MySQLdb
import environ
import os
from similar import getSimKey
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication


env = environ.Env(
    DATABASE_NAME=(str, ''),
    DATABASE_USER=(str, ''),
    DATABASE_PASSWORD=(str, ''),
    DATABASE_HOST=(str, ''),
    DATABASE_PORT=(str, ''),
    NAVER_ADDRESS=(str, ''),
    NAVER_ID=(str, ''),
    NAVER_PASSWORD=(str, ''),
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)


def sendAll():
    try:
        connection = MySQLdb.connect(
            host=env('DATABASE_HOST'),
            user=env('DATABASE_USER'),
            passwd=env('DATABASE_PASSWORD'),
            db=env('DATABASE_NAME')
        )

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Notice WHERE isSended = TRUE") # 원래 FALSE 지금은 체크용도
        notices = cursor.fetchall()

        # 전송된 공지 개수
        count = 0

        # 공지 레코드마다 title, link 값 가져오기
        for notice in notices:
            send_list = []
            title = notice[0]
            link = notice[1]
            cid = notice[4]
            # 각 공지 레코드의 Cid 값이랑 같은 Keyword 레코드만 가져옴
            query = "SELECT * FROM Keyword WHERE Cid_id = %s"
            cursor.execute(query, (cid,))
            keywords = cursor.fetchall()
            if keywords:
                for keyword in keywords :
                    email_address = keyword[3]
                    keyword_text = keyword[1]
                    keywords_similar = getSimKey(keyword_text, 5)
                    is_overlapped = False   #키워드가 매칭 되었는데 유사단어도 매칭된다면 중복 발송 방지

                    # 가져온 key값이 공지 레코드의 title의 substring과 매치된다면 send_list에 이메일주소 저장
                    if keyword_text in title:
                        send_list.append(email_address)
                        is_overlapped = True

                    # key값이 매치안되었으면 유사단어로 매칭
                    if not is_overlapped:
                        for keyword_similar in keywords_similar:
                            if keyword_similar in title:
                                send_list.append(email_address)
                                break   #한번이라도 매칭되었으면 탈출 (중복 방지)

            else:
                print("해당 Notice의 Cid와 매칭하는 Keyword 레코드가 없음")

            # 중복 방지
            send_list = list(set(send_list))
            if send_list:
                # 공지마다 관련 유저들에게  발송
                sendEmail(send_list, title, link)

                # 체크용도
                print(send_list)
                print(title)
                print(link)
                print(count)

                count += 1

        cursor.close()
        connection.close()


    except Exception as e:
        # 예외 처리
        print('An error occurred:', str(e))




def sendEmail(send_list, title, link):
    # 수신자
    recipients = send_list
    message = MIMEMultipart()
    message['Subject'] = title
    message['From'] = env('NAVER_ADDRESS')
    message['To'] = ",".join(recipients)

    text1 = title
    text2 = link


    content = """
        <html>
        <body>
            <h2>{}</h2>
            <p> {} </p>
        </body>
        </html>
    """.format(text1, text2)

    mimetext = MIMEText(content, 'html')
    message.attach(mimetext)

    email_id = env('NAVER_ID')
    email_pw = env('NAVER_PASSWORD')

    server = smtplib.SMTP('smtp.naver.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email_id, email_pw)
    server.sendmail(message['From'], recipients, message.as_string())
    server.quit()

sendAll()