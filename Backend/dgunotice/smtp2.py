import secrets
import string
from pathlib import Path
from random import random

import MySQLdb
import environ
import os

from django.template.defaultfilters import length
from django.urls import reverse

from .models import Verify
from .similar2 import getSimKey
from .similar2 import tokenizedKey
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

        # 키워드 전송된 공지 개수
        count = 0
        # notice 탐색 횟수
        notice_cycle = 0

        # 공지 레코드마다 title, link 값 가져오기
        for notice in notices:
            send_keyword = []
            send_similar = []
            title = notice[0]
            link = notice[1]
            cid = notice[4]
            # 각 공지 레코드의 Cid 값이랑 같은 Keyword 레코드만 가져옴
            query = "SELECT * FROM Keyword WHERE Cid_id = %s"
            cursor.execute(query, (cid,))
            keywords = cursor.fetchall()
            if keywords:
                for keyword in keywords :
                    email_address = keyword[3] # 유저 이메일
                    keyword_text = keyword[1] # 등록된 키워드
                    keywords_similar = getSimKey(keyword_text, 5)
                    similar_on = keyword[4] # 키워드 유사단어로 공지 받아볼지 여부
                    keywords_tokenized = tokenizedKey(keyword_text) # 키워드 토큰화

                    is_overlapped = False   #키워드가 매칭 되었는데 유사단어도 매칭된다면 중복 발송 방지

                    # 토큰화된 키워드값이 공지 레코드의 title의 substring과 매치된다면 send_key에 이메일주소 저장
                    for keyword_tokenized in keywords_tokenized:
                        if keyword_tokenized in title:
                            send_keyword.append(email_address)
                            is_overlapped = True

                            break #한번이라도 매칭되었으면 탈출 (중복 방지)

                    # key값이 매치안되었고 유사단어 onoff 가 on일때만 유사단어로
                    # 공지 레코드의 title의 substring과 매치된다면 send_similar에 이메일주소 저장
                    if not is_overlapped and similar_on:
                        for keyword_similar in keywords_similar:
                            if keyword_similar in title:
                                send_similar.append(email_address)
                                break   #한번이라도 매칭되었으면 탈출 (중복 방지)

            else:
                print("해당 Notice의 Cid와 매칭하는 Keyword 레코드가 없음")

            # List into Set (중복 방지)
            send_keyword = list(set(send_keyword))
            send_similar = list(set(send_similar))
            # Empty Set 전송 방지
            if send_keyword:
                sendEmail(send_keyword, title, link, 0)

                count += 1
                # 테스트
                print("전송된 유저 목록 : ", send_keyword)
                print("[키워드 공지] : ", title)
                print("링크 : ", link)
                print("전송된 공지 카운트 : ", count)

            if send_similar:
                sendEmail(send_similar, title, link, 1)

                count += 1
                # 테스트
                print("[전송된 유저 목록] : ", send_similar)
                print("[유사키워드 공지] : ", title)
                print("[링크] : ", link)
                print("[전송된 공지 카운트] : ", count)

            notice_cycle += 1
            print("공지 탐색 횟수 : ", notice_cycle)
            print("")

        cursor.close()
        connection.close()

    except Exception as e:
        # 예외 처리
        print('An error occurred:', str(e))


def sendEmail(recipient, title, link):
    # 수신자

    message = MIMEMultipart()

    message['Subject'] = title
    message['From'] = env('NAVER_ADDRESS')
    message['To'] = ",".join(recipient)

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
    server.sendmail(message['From'], recipient, message.as_string())
    server.quit()


def generate_token(length=15):
    token = secrets.token_urlsafe(length)
    return token


def verify_email_token(email, token):
    try:
        # Retrieve the user from the database based on the email
        verify = Verify.objects.get(temp_id=email)

        # Verify if the token matches the user's token in the database
        if verify.token == token:
            # Update the user's email verification status
            verify.delete()

            # Return True to indicate successful verification
            return True

    except verify.DoesNotExist:
        pass

    # Return False for any other case (invalid email, token mismatch, etc.)
    return False

def generate_verification_link(email, token):
    base_url = 'http://127.0.0.1:8000'
    url = reverse('verify_email')
    link = f"{base_url}{url}?email={email}&token={token}"
    return link
