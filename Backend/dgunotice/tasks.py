from django_cron import CronJobBase, Schedule
from .crawl import crawlCheck, frequencyUpdate

class CrawlCheckJob(CronJobBase):
    RUN_EVERY_MINS = 60  # 1시간에 한 번 실행

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'dgunotice.crawl_check_job'    # 임의의 코드 이름

    def do(self):
        crawlCheck()

class FrequencyUpdateJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # 24시간에 한 번 실행

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'dgunotice.frequency_update_job'    # 임의의 코드 이름

    def do(self):
        frequencyUpdate()