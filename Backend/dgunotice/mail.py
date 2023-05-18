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