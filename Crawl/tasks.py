from apscheduler.schedulers.background import BackgroundScheduler
from crawl import crawlCheck, frequencyUpdate
import time

# BackgroundScheduler 객체 생성
scheduler = BackgroundScheduler()

# 1시간마다 crawlCheck() 함수 호출
scheduler.add_job(crawlCheck, 'interval', hours=1)

# 24시간마다 frequencyUpdate() 함수 호출
scheduler.add_job(frequencyUpdate, 'interval', hours=24)

# 스케줄러 시작
scheduler.start()

try:
    while True:
        scheduler.print_jobs()  # 작업 목록 출력 또는 다른 로직을 추가로 수행
        time.sleep(10)  # 프로그램이 너무 많은 CPU 시간을 사용하지 않도록 잠시 대기
except KeyboardInterrupt:
    pass

# 스케줄러 종료
scheduler.shutdown()