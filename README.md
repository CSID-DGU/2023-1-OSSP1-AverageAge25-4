# 공지사항알리미 
동국대학교 홈페이지 상의 다양한 공지사항을 개인 맞춤형 통합 홈페이지를 통해 한눈에 확인할 수 있는 서비스

<br> 

## 팀 소개

| 이름   | 학번 | 주요 파트 | ID                                             |
| ------ | ---- | --------- |------------------------------------------------|
| 장우진 |2018113340|Backend| [@JangWooJin1](https://github.com/JangWooJin1) |
| 박지민 |2017110451|Backend| [@imbatmin](https://github.com/imbatmin)       |
| 신호현 |2018113339|Backend| [@seayen](https://github.com/seayen)           |
| 정고은 |2020113393|Frontend| [@chgoeun](https://github.com/chgoeun)         |
| 최인성 |2017111758|Frontend| [@Kakaomacao](https://github.com/Kakaomacao)   |
| 하유진 |2020113387|Frontend| [@yuunha](https://github.com/yuunha)           |

<br> 

## 1. 프로젝트 목표

 본 프로젝트는 동국대학교 홈페이지 상의 다양한 공지사항을 개인맞춤형 통합 홈페이지를 통해 한눈에 확인할 수 있는 서비스를 제공한다. 사용자는 자신이 관심 있는 키워드를 설정하여, 관련 공지사항이 게시될 경우 알림 받을 수 있다. 이를 통해 학생들은 홈페이지 곳곳에 분산되어 있는 공지들을 편리하게 확인할 수 있으며 중요한 공지사항을 놓치지 않도록 보장받는 것이다.

 > [참고 프로젝트] [동국대학교 컴퓨터공학과 챗봇 기반 키워드 알림 서비스](https://github.com/CSID-DGU/2021-2-OSSP1-NotifyService-1)

<br> 

## 2. 개선 사항

1. 검색 및 모니터링 기능 추가
   - 기존   : 크롤링한 공지사항들을 저장하고, 저장된 공지사항들을 중복 크롤링 방지 및 word2vec학습에 사용
   - 문제점 : DB에서 가장 큰 용량을 차지하는 것에 비해, 하는 역할이 없음
   - 개선   : 해당 공간을 더 효율적으로 사용하기 위해 아래와 같은 기능 추가 
      - 모니터링 기능: 키워드를 등록하지 않거나 모르는 경우에도 공지확인이 가능   
      - 검색 기능: 키워드 등록 시점 이전에 올라온 공지도 확인
<br> 

2. 키워드 범위 설정 및 유사 단어 추천 on/off 기능 추가   
   - 기존   : 사용자가 키워드 등록시 아래의 옵션들이 존재x
       - 알림을 받고 싶은 게시판 선택
       - 유사단어 추천 여부 선택
   - 문제점 : 특정 게시판의 특정 키워드에 대한 알림만 받고 싶었던 사용자들에게는 스팸 알림과 마찬가지
   - 개선   : 키워드 등록시 아래의 기능을 추가
       - 키워드 범위 설정 기능      : 사용자가 알림을 받고싶은 게시판 범위를 선택 
       - 유사 단어 추천 on/off 기능 : 사용자가 지정한 키워드만 알림을 받을지 키워드와 유사한 단어까지 모두 알림을 받을지 선택
<br> 

3. 챗봇에서 웹 서비스로 전환
   - 기존   : 챗봇을 통해 유저와 상호작용을 함, 유저와 상호작용하는 부분은 아래와 같음
       - 키워드 추가 및 삭제
       - 유저 정보 등록
   - 문제점 : 프로젝트 개선으로 여러 기능들이 추가되어 유저와의 상호작용이 하였고 그렇기에 서비스의 복잡성 또한 증가
   - 개선   : 웹 서비스로 전환
       - 사용자 경험(UI/UX)를 통해 여러가지 기능들을 직관적으로 이해 가능
       - 유저 편의성 증가
<br> 

4. 알림 전송 방식 변경
   - 기존   : 카카오 알림톡API(Solapi)을 이용하여 사용자에게 키워드 공지 알림 전송
   - 문제점 : Solapi는 유료 정책으로 알림 전송 비용이 발생
   - 개선   : 무료로 사용할 수 있는 이메일 방식으로 변경
<br> 

5. 크롤링 작업 서버에서 분리
   - 기존   : 서버에서 제공하는 ORM을 사용하였기에, 크롤링 작업이 웹 서버내에서 동작
   - 문제점 : 크롤링 작업은 소요시간이 길고 과정이 복잡한 작업이기에, 서버 자원을 점유하면서 다른 사용자 요청 처리에 영향을 줌
   - 개선   : 독립적인 DB커넥터를 사용하여 크롤링 작업을 서버에서 분리
<br> 

6. 게시판별로 크롤링 주기 설정  
   - 기존   : 주기적으로 1시간마다 모든 게시판을 동국대 서버에 요청
   - 문제점 : 동국대 서버에 큰 부당이 발생하여 IP 차단 위험성 증가
   - 개선   : 게시판마다 가중치를 설정
       - 가중치에 따라 주기를 1~24시간으로 설정
       - 서버 부담 저하 및 IP 차단 위험성을 감소  
<br>

7. 크롤링 예외처리를 통한 안정성 향상   
   - 기존   : 크롤링 코드 내에 별도의 예외처리를 하지 않음
   - 문제점 : 크롤링에서 발생하는 다양한 예외 사항(네트워크 오류, 정보 위치 변경 등...)이 발생하면 크롤링 작업이 도중에 종료되어 다시 처음부터 크롤링 진행
   - 개선   : 크롤링에서 발생하는 예외처리 진행
       - 특이 공지(비밀글, 삭제된글 등..) 발생시 건너뛰기
       - 예외 발생 지점부터 이어서 진행 가능  
<br>

8. 서버 구동 전, 각 기능들이 정상적으로 동작하는지 검증
   - 기존   : 서버 구동 전, 각 기능들이 정상적으로 동작하는지 검증을 하지 않음
   - 문제점 : 변경사항이 발생하여 일부 기능들이 동작하지 않아 서비스 안정성과 품질문제 발생 가능
   - 개선   : 각 기능별 테스트 케이스를 작성하여, 서버 구동 전 기능들이 모두 정상적으로 동작하는지 검증 진행
       - Python 내장 테스트 도구 'unnittest' 사용
<br>

<br> 

## 3. 평가 항목

1. 크롤링 주기 설정을 통한 6개월간 동국대 서버 요청 수 감소 분석   
   - 목표 : 각 게시판에 별도의 크롤링 주기 설정 후, 실제로 동국대 서버에 보내는 요청 수가 감소했는지 분석
   - 방법 :
      - 크롤링 주기 설정 전후의 6개월간 73개의 모든 게시판의 하루 요청 수를 비교
      - matplotlib을 이용하여 결과 시각화 진행  
   - 결과 :
     <p align="center"><img src="https://github.com/CSID-DGU/2023-1-OSSP1-AverageAge25-4/assets/110288718/4ad315fb-3c79-433e-ba90-aa56fe222ce4" width="60%" height="60%"/></p>
     
      - 개선전후의 6개월간 평균 요청 횟수
         - 개선전 : 평균 1752회
         - 개선후 : 평균 230회
      - 약 87% 성능 향상을 확인하였고, 이로 인해 게시판 별 주기 설정 방식이 동국대 서버 부하에 효과적이라는 결론 도출 
<br>

2. 크롤링 코드 분리를 통한 웹 서비스 제공 품질 향상 분석   
   - 목표 : 크롤링 작업을 서버에서 분리한 후, 실제로 사용자 요청 처리 능력이 향상되었는지 분석
   - 방법 :
      - 서버 내외에서 크롤링 코드 실행 시 성능 비교
      - 웹 스트레스 테스트로 동시 접속자수 대비 서버 부담 확인
      - 오픈소스 로드 테스트 소프트웨어 Locust 활용
   - 결과 :
     <p align="center"><img src="https://github.com/CSID-DGU/2023-1-OSSP1-AverageAge25-4/assets/110288718/b1a4d3c1-90eb-4eec-95c4-bcbd004ecaf3" width="60%" height="60%"/></p>
     
      - 초당 요청수(RPS)가 떨어지고 응답시간(ms)가 늘어나기 시작하는 평균 유저수
         - 서버 내 존재 : 419명
         - 서버와 분리  : 649명
      - 약 54% 성능 향상을 확인하였고, 이로 인해 크롤링 코드를 서버와 분리한 방식이 웹 서비스 안정성 향상에 효과적이라는 결론 도출 

<br> 

## 4. 사용한 OSS
1. Django: 웹 애플리케이션 제작을 위해 사용
    - 프로젝트에서 다음과 같은 기능을 활용
      - 템플릿 시스템을 통한 프론트엔드 구축
      - 관리자 페이지를 이용한 DB 관리
      - SQL Injection 방어를 위한 ORM 사용
      - django.contrib.auth.hashers 패키지를 통한 정보 암호화
<br>    

2. Word2Vec: 연관 검색어 제공 및 유사 키워드를 포함한 공지 알림 기능을 위해 사용
<br>

4. Smtplib & email : 회원 가입 시 인증 메일 발송과 키워드 알림 발송 기능을 위해 사용
<br>

6. Locust: 웹 부하 테스트를 위해 사용되며, 서비스의 안정성 평가와 향상된 성능 측정을 위해 사용

<br> 

## 5. 시연 영상

1. 회원가입-로그인 시연영상 <br> 
https://github.com/CSID-DGU/2023-1-OSSP1-AverageAge25-4/assets/110288718/979e995f-e672-4595-8bb3-68189083ff70

<br> 

2. 검색 시연 영상 <br> 
https://github.com/CSID-DGU/2023-1-OSSP1-AverageAge25-4/assets/110288718/e4de4894-0480-4b28-8c55-bf4dabbbd0cc

<br> 

3. 키워드 추가 및 알림 전송 시연 영상 <br>
https://github.com/CSID-DGU/2023-1-OSSP1-AverageAge25-4/assets/110288718/02af02db-ce82-4d9e-bd1f-60f2d04898b0



