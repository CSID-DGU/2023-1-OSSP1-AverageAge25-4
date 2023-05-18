# 크롤링 관련
from .models import Pagetype, Category, User, Keyword, Notice
from django.db.models import F
import urllib
from bs4 import BeautifulSoup
import time
import random
import threading
import datetime
import re

import logging

logger = logging.getLogger(__name__)
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
})

def getHtml(url):
    # 변경된 url로 이동하여 크롤링하기 위해 html 페이지를 파싱
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def getNoticeInfo(category, notice):
    url = category.Clink
    page_type = category.Pid.Pid

    # 고정 공지는 건너뛰기
    is_fixed = notice.select_one(category.Pid.Nfixed)
    if (page_type == 0 and is_fixed.get("class") == ["fix"]) or \
            (page_type in [1, 2] and is_fixed.get("class") == ["mark"]) or \
            (page_type == 3 and notice.get("class") == ["cell_notice"]) or \
            (page_type == 4 and is_fixed.find("img") is not None) or \
            (page_type == 5 and is_fixed.get("class") == ["bo_notice"]) or \
            (page_type == 6 and notice.get("class") == ["always"]):
        return None

    # 게시글 제목
    name_tag = notice.select_one(category.Pid.Nname)
    if page_type == 2:
        name_tag = name_tag.select_one("span").extract()

    name = name_tag.text.strip()

    # 게시글 링크
    link_tag = notice.select_one(category.Pid.Nlink)
    link = ""
    if page_type == 0:
        link = re.sub(r'list\?pageIndex=', 'detail/', url) + re.sub(r'[^0-9]', '', link_tag.get('onclick'))
    elif page_type == 1 or page_type == 2:
        link = re.sub(r'\/article\/(notice\d*|news\d*|info\d*|board\d*)\/list\?pageIndex=', '', url) + link_tag.get(
            'href')
    elif page_type == 3:
        link = link_tag.get('href')  # 추가 조치 필요
    elif page_type == 4:
        link = re.sub(r'/k3/sub5/sub1.php\?page=', '', url) + link_tag.get('href')
    elif page_type == 5:
        link = link_tag.get('href')
    elif page_type == 6:
        link = re.sub(r'/bbs/list/1\?pn=', '', url) + link_tag.get('href')
    elif page_type == 7:
        link = link_tag.get('onclick')  # 추가 조치 필요

    # 게시글 날짜
    ntime = notice.select_one(category.Pid.Ntime).text.strip()

    #### 테스트용 ####
    # print("카테고리 : ", category)
    # print("공지이름 : ", name.replace("\xa0", " "))
    # print("링크 : ", link)
    # print("시간 : ", ntime)
    logger.info("카테고리: %s", category)
    logger.info("공지이름: %s", name.replace("\xa0", " "))
    logger.info("링크: %s", link)
    logger.info("시간: %s", ntime)

    return category, name.replace("\xa0", " "), link, ntime

def saveNotice(notice_info):
    category, name, link, ntime = notice_info

    n = Notice(Cid=category,
               title=name,
               link=link,
               time=ntime)
    n.save()

def crawlInitial():
    category_list = Category.objects.select_related('Pid').all()

    for category in category_list:
        url = category.Clink
        page_type = category.Pid.Pid

        page_num = 1  #페이지 수
        normal_notice_count = 0  #페이지내 일반 공지 갯수
        fixed_notice_count = 0   #페이지내 고정 공지 갯수

        while page_num < 2:
            print('\n----- Current Page : {}'.format(page_num), '------\noriginal url : ' + url)
            # 변경된 url에 페이지 번호를 붙임
            url_change = url + f'{page_num}'
            print('changed url : ' + url_change + '\n-------------------------------------------------')

            # 페이지가 변경됨에 따라 delay 발생 시킴
            time.sleep(random.uniform(4, 7))

            soup = getHtml(url_change)

            # 게시글 리스트 선택
            notice_list = soup.select(category.Pid.Nlist)

            for notice in notice_list:
                notice_info = getNoticeInfo(category, notice)

                if notice_info is not None: #일반 공지인 경우
                    saveNotice(notice_info)
                    # 크롤링 한 게시글 개수 증가
                    normal_notice_count += 1

                else: #고정 공지인 경우
                    fixed_notice_count += 1

            if page_type == 5: #고정공지 + 일반공지 합쳐서 15개 - 고정공지 개념을 조금 다시 확인해봐야할거같음
                break
            elif page_type == 6: #고정공지 + 일반공지 합쳐서 10개 - 근데 애초에 고정공지가 그냥 일반공지임
                if normal_notice_count + fixed_notice_count < 10:
                    print('------------------ 게시글 개수가 적어서 현재 페이지에서 크롤링 종료 (10) ------------------')
                    break
            elif page_type == 7:
                if normal_notice_count < 20:
                    print('------------------ 게시글 개수가 적어서 현재 페이지에서 크롤링 종료 (20) ------------------')
                    break
            else:
                if normal_notice_count < 10:
                    print('------------------ 게시글 개수가 적어서 현재 페이지에서 크롤링 종료 (10) ------------------')
                    break

            #다음 페이지 탐색
            page_num += 1

def crawl(crawl_list):
    for category in crawl_list:
        url = category.Clink + '1'

        soup = getHtml(url)

        # 게시글 리스트 선택
        notice_list = soup.select(category.Pid.Nlist)
        for notice in notice_list:
            notice_info = getNoticeInfo(category, notice)

            if notice_info is not None:  # 일반 공지인 경우
                saveNotice(notice_info)


def get_percentile(value, min_value, max_value):
    percentile = (value - min_value) / (max_value - min_value) * 23 + 1
    return int(percentile)

def frequencyUpdate():
    print("실행은 됐음1111")
    #가중치를 24개 구간으로 쪼개기
    categories = Category.objects.all()

    #관련 변수 값을 담을 리스트
    keyword_list, day_list, week_list, month_list = [], [], [], []

    #관련 변수값을 리스트에 담기
    for category in categories:
        keyword_num = Keyword.objects.filter(Cid=category).count()
        day_num = Notice.objects.filter(Cid=category, time__gte=datetime.datetime.now()-datetime.timedelta(days=1)).count()
        week_num = Notice.objects.filter(Cid=category, time__gte=datetime.datetime.now()-datetime.timedelta(days=7)).count()
        month_num = Notice.objects.filter(Cid=category, time__gte=datetime.datetime.now()-datetime.timedelta(days=30)).count()

        keyword_list.append(keyword_num)
        day_list.append(day_num)
        week_list.append(week_num)
        month_list.append(month_num)
    print("실행은 됐음2222")
    #구간 설정을 위한 최대, 최소 구하기
    keyword_max = max(keyword_list)
    day_max = max(day_list)
    week_max = max(week_list)
    month_max = max(month_list)

    keyword_min = min(keyword_list)
    day_min = min(day_list)
    week_min = min(week_list)
    month_min = min(month_list)

    print("실행은 됐음2233")
    for category in categories:
        keyword_num = Keyword.objects.filter(Cid=category).count()
        day_num = Notice.objects.filter(Cid=category, time__gte=datetime.datetime.now()-datetime.timedelta(days=1)).count()
        week_num = Notice.objects.filter(Cid=category, time__gte=datetime.datetime.now()-datetime.timedelta(days=7)).count()
        month_num = Notice.objects.filter(Cid=category, time__gte=datetime.datetime.now()-datetime.timedelta(days=30)).count()

        #가중치를 시간으로 환산
        keyword_percentile = get_percentile(keyword_num, keyword_min, keyword_max)
        day_percentile = get_percentile(day_num, day_min, day_max)
        week_percentile = get_percentile(week_num, week_min, week_max)
        month_percentile = get_percentile(month_num, month_min, month_max)

        #시간에 우선도 반영
        weight = (100 - (keyword_percentile + day_percentile + week_percentile + month_percentile))/4

        Category.objects.filter(pk=category.Cid).update(time_initial=weight)
        print("실행은 됐음3333")

    print("실행은 됐음4444")

def crawlCheck():
    # 1시간마다 주기 체크
    Category.objects.filter(time_remaining__gt=0).update(
        time_remaining=F('time_remaining') - 1
    )
    crawl_list = Category.objects.filter(time_remaining=0)
    crawl_list.update(time_remaining=F('time_initial'))
    return crawl(crawl_list)