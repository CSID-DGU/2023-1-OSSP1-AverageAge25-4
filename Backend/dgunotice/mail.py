import gmail

# 프로젝트 ID 설정
project_id = '임시'

# 클라이언트 ID, 시크릿 ID
client_id = '임시'
client_secret = '임시'

# 사용자 인증 정보
credentials = gmail.credentials.get_application_default(
    project_id=project_id,
    client_id=client_id,
    client_secret=client_secret)

# 이메일 개체 생성
message = gmail.Message()
message.set_from('내 주소')
message.set_to('보낼 주소')
message.set_subject('제목')
message.set_text('내용')

# 이메일 보내기.
gmail.send_message(credentials, message)


# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

import requests

# 네이버 SMTP API URL
NAVER_SMTP_API_URL = "https://apis.naver.com/mail/v1/send"

# 네이버 SMTP API 인증 키
NAVER_SMTP_API_KEY = "YOUR_NAVER_SMTP_API_KEY"

# 이메일 메시지
message = {
  "from": "내주소",
  "to": "보낼 주소",
  "subject": "제목",
  "body": "내용"
}

# 네이버 SMTP API에 요청을 보내고 결과를 가져오기
response = requests.post(NAVER_SMTP_API_URL, headers={"Authorization": "Bearer {}".format(NAVER_SMTP_API_KEY)}, data=message)

# 결과를 확인합니다.
if response.status_code == 200:
  print("이메일을 성공적으로 보냈습니다.")
else:
  print("이메일을 보내지 못했습니다.")