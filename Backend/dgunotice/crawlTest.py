import datetime
import MySQLdb
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import random
import re
from pathlib import Path
import environ
import os

env = environ.Env(
    DATABASE_NAME=(str, ''),
    DATABASE_USER=(str, ''),
    DATABASE_PASSWORD=(str, ''),
    DATABASE_HOST=(str, ''),
    DATABASE_PORT=(str, ''),
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

def getHtml(url):
    # 변경된 url로 이동하여 크롤링하기 위해 html 페이지를 파싱
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def getNoticeInfo(category, notice):
    url = category[2]
    page_type = category[5]

    # 고정 공지는 건너뛰기
    is_fixed = notice.select_one(category[8])
    if is_fixed != None: #고정 표시가 없는 경우 (예외처리)
        if (page_type == 0 and is_fixed.get("class") == ["fix"]) or \
                (page_type in [1, 2] and is_fixed.get("class") == ["mark"]) or \
                (page_type == 3 and notice.get("class") == ["cell_notice"]) or \
                (page_type == 4 and is_fixed.find("img") is not None) or \
                (page_type == 5 and notice.get("class") == ["bo_notice"]) or \
                (page_type == 6 and notice.get("class") == ["always"]):
            return None

    # 게시글 제목
    name_tag = notice.select_one(category[9])
    if name_tag == None:    #제목이 없는 경우 (예외처리)
        name = "None"
    else:
        if page_type == 2:
            span_tag = name_tag.select_one("span")
            if span_tag:
                span_tag.extract()

        name = name_tag.text.strip()

    # 게시글 링크
    link = ""
    link_tag = notice.select_one(category[10])
    if link_tag == None:    #링크가 없는 경우 (예외처리)
        link = category[2]
    else:
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
    ntime = notice.select_one(category[11])
    if ntime == None:   #게시글 시간이 없는 경우 (예외처리)
        ntime = "0000-1-1"
    else:
        ntime = ntime.text.strip()

    #### 테스트용 ####
    print("카테고리 : ", category[1])
    print("공지이름 : ", name.replace("\xa0", " "))
    print("링크 : ", link)
    print("시간 : ", ntime)

    return category, name.replace("\xa0", " "), link, ntime

def crawlInitialTest(category_index=0, page_index=0):
    try:
        connection = MySQLdb.connect(
            host=env('DATABASE_HOST'),
            user=env('DATABASE_USER'),
            passwd=env('DATABASE_PASSWORD'),
            db=env('DATABASE_NAME')
        )
        cursor = connection.cursor()

        category_list_query = """
            SELECT *
            FROM category
            INNER JOIN pagetype ON category.Pid_id = pagetype.Pid
        """
        cursor.execute(category_list_query)
        category_list = cursor.fetchall()

        for category in category_list[category_index:]:
            url = category[2]
            page_type = category[5]

            category_index += 1
            page_index = 1

            while True:
                isNext = True
                normal_notice_count = 0  # 페이지내 일반 공지 갯수
                fixed_notice_count = 0  # 페이지내 고정 공지 갯수
                print('\n----- Current Page : {}'.format(page_index), '------\noriginal url : ' + url)
                # 변경된 url에 페이지 번호를 붙임
                url_change = url + f'{page_index}'
                print('changed url : ' + url_change + '\n-------------------------------------------------')

                # 페이지가 변경됨에 따라 delay 발생 시킴
                time.sleep(random.uniform(4, 7))

                soup = getHtml(url_change)

                # 게시글 리스트 선택
                notice_list = soup.select(category[7])

                for notice in notice_list:
                    #마지막 페이지면 해당 게시판 크롤링 종료 (
                    if (page_type == 0) and notice.find('div', class_='board_empty'):
                        isNext = False
                        break
                    elif (page_type == 1 or page_type == 2) and notice.find('td', class_='no_data'):
                        isNext = False
                        break
                    elif (page_type == 5) and notice.find('td', class_='empty_table'):
                        isNext = False
                        break
                    elif (page_type == 7):
                        pass #다시한번가서 봐바

                    notice_info = getNoticeInfo(category, notice)

                    if notice_info is not None: #일반 공지인 경우
                        category, name, link, ntime = notice_info

                        insert_query = """
                            INSERT INTO notice (Cid_id, title, link, time, isSended, isTrained)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """
                        try:
                            cursor.execute(insert_query, (category[0], name, link, ntime, True, False))
                            connection.commit()

                        except MySQLdb.IntegrityError as e:
                            # 중복된 항목 처리
                            print("이미 삽입된 항목입니다. 건너뜁니다.")

                        # 크롤링 한 게시글 개수 증가
                        normal_notice_count += 1

                    else: #고정 공지인 경우
                        fixed_notice_count += 1

                #마지막페이지면 크롤링 종료
                if (page_type == 3 or page_type == 4 or  page_type == 6) and normal_notice_count < 10:
                    isNext = False

                if isNext:
                    #다음 페이지 탐색
                    page_index += 1
                else:
                    print('------------------ 게시판의 마지막 페이지라 크롤링 종료 ------------------')
                    break

        cursor.close()
        connection.close()

    except Exception as e:
        # 예외 처리
        print('An error occurred:', str(e))
        crawlInitial(category_index-1, page_index-1)

def crawl(crawl_list, category_index=0):
    try:
        connection = MySQLdb.connect(
            host=env('DATABASE_HOST'),
            user=env('DATABASE_USER'),
            passwd=env('DATABASE_PASSWORD'),
            db=env('DATABASE_NAME')
        )
        cursor = connection.cursor()
        
        print("연결 성공")

        for category in crawl_list[category_index:]:
            category_index+=1
            url = category[2] + '1'

            print('\n----- Current Page : {}'.format(1), '------\noriginal url : ' + url + '\n-------------------------------------------------')

            # 페이지가 변경됨에 따라 delay 발생 시킴
            time.sleep(random.uniform(4, 7))

            soup = getHtml(url)

            # 게시글 리스트 선택
            notice_list = soup.select(category[7])
            for notice in notice_list:
                notice_info = getNoticeInfo(category, notice)

                if notice_info is not None:  # 일반 공지인 경우
                    category, name, link, ntime = notice_info

                    insert_query = """
                         INSERT INTO notice (Cid_id, title, link, time, isSended, isTrained)
                         VALUES (%s, %s, %s, %s, %s, %s)
                     """
                    try:
                        cursor.execute(insert_query, (category[0], name, link, ntime, True, False))
                        connection.commit()
                    except MySQLdb.IntegrityError as e:
                        # 중복된 항목 처리
                        print("이미 삽입된 항목입니다. 건너뜁니다.")

    except Exception as e:
        # 예외 처리
        print('An error occurred:', str(e))
        crawl(crawl_list, category_index-1)

def get_percentile(value, min_value, max_value):
    percentile = (value - min_value) / (max_value - min_value) * 23 + 1
    return int(percentile)

def frequencyUpdate():
    try:
        connection = MySQLdb.connect(
            host=env('DATABASE_HOST'),
            user=env('DATABASE_USER'),
            passwd=env('DATABASE_PASSWORD'),
            db=env('DATABASE_NAME')
        )
        cursor = connection.cursor()
        
        ###기존 내용 확인 ###
        select_query = f"SELECT Cname, time_initial FROM category"
        cursor.execute(select_query)
        old_categories = cursor.fetchall()
        print("기존 category 내용:")
        for old_category in old_categories:
            cname = old_category[0]
            time_initial = old_category[1]
            print(f"Cname: {cname}, time_initial: {time_initial}")

        print("=================================================")
        ###기존 내용 확인 ###

        # 현재 날짜
        current_date = datetime.date.today()

        # 일별 카운트 쿼리
        daily_query = f'''
        SELECT Category.Cid, IFNULL(COUNT(Notice.Cid_id), 0) AS day_count
        FROM category
        LEFT JOIN Notice ON Category.Cid = Notice.Cid_id AND DATE(Notice.time) = '{current_date}'
        GROUP BY Category.Cid
        '''
        cursor.execute(daily_query)
        daily_counts = cursor.fetchall()

        print("일별 카운트 가져오기")
        print(daily_counts)

        # 주별 카운트 쿼리
        start_of_week = current_date - datetime.timedelta(days=current_date.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)
        weekly_query = f'''
        SELECT Category.Cid, IFNULL(COUNT(Notice.Cid_id), 0) AS week_count
        FROM category
        LEFT JOIN Notice ON Category.Cid = Notice.Cid_id AND DATE(Notice.time) >= '{start_of_week}' AND DATE(Notice.time) <= '{end_of_week}'
        GROUP BY Category.Cid
        '''
        cursor.execute(weekly_query)
        weekly_counts = cursor.fetchall()

        print("주별 카운트 가져오기")
        print(weekly_counts)

        # 월별 카운트 쿼리
        start_of_month = current_date.replace(day=1)
        end_of_month = current_date.replace(day=28) + datetime.timedelta(days=4)
        monthly_query = f'''
        SELECT Category.Cid, IFNULL(COUNT(Notice.Cid_id), 0) AS month_count
        FROM category
        LEFT JOIN Notice ON Category.Cid = Notice.Cid_id AND DATE(Notice.time) >= '{start_of_month}' AND DATE(Notice.time) <= '{end_of_month}'
        GROUP BY Category.Cid
        '''
        cursor.execute(monthly_query)
        monthly_counts = cursor.fetchall()

        print("월별 카운트 가져오기")
        print(monthly_counts)

        # 키워드 카운트 쿼리
        keyword_query = f'''
        SELECT Category.Cid, IFNULL(COUNT(keyword.Cid_id), 0) AS key_count
        FROM category
        LEFT JOIN keyword ON Category.Cid = keyword.Cid_id
        GROUP BY Category.Cid
        '''

        cursor.execute(keyword_query)
        keyword_counts = cursor.fetchall()

        print("키워드 카운트 가져오기")
        print(keyword_counts)

        # 일별 최대, 최소 카운트
        day_max = max(daily_counts, key=lambda x: x[1])
        day_min = min(daily_counts, key=lambda x: x[1])

        print("일별 최대, 최소 카운트")
        print(day_max, day_min)

        # 주별 최대, 최소 카운트
        week_max = max(weekly_counts, key=lambda x: x[1])
        week_min = min(weekly_counts, key=lambda x: x[1])

        print("주별 최대, 최소 카운트")
        print(week_max, week_min)

        # 월별 최대, 최소 카운트
        month_max = max(monthly_counts, key=lambda x: x[1])
        month_min = min(monthly_counts, key=lambda x: x[1])

        print("월별 최대, 최소 카운트")
        print(month_max, month_min)

        # 키워드별 최대, 최소 카운트
        keyword_max = max(keyword_counts, key=lambda x: x[1])
        keyword_min = min(keyword_counts, key=lambda x: x[1])

        print("키워드별 최대, 최소 카운트")
        print(keyword_max, keyword_min)

        #가중치를 시간으로 환산
        keyword_percentile = [get_percentile(count[1], keyword_min[1], keyword_max[1]) for count in keyword_counts]
        print("키워드별 퍼센트 값")
        print(keyword_percentile)
        day_percentile = [get_percentile(count[1], day_min[1], day_max[1]) for count in daily_counts]
        print("일별 퍼센트 값")
        print(day_percentile)
        week_percentile = [get_percentile(count[1], week_min[1], week_max[1]) for count in weekly_counts]
        print("주별 퍼센트 값")
        print(week_percentile)
        month_percentile = [get_percentile(count[1], month_min[1], month_max[1]) for count in monthly_counts]
        print("월별 퍼센트 값")
        print(month_percentile)

        # weight 계산
        weights = [(100 - (keyword_percentile[i] + day_percentile[i] + week_percentile[i] + month_percentile[i]))/4
                   for i in range(len(keyword_percentile))]

        print("최종 weight값")
        print(weights)

        # category의 time_initial 값으로 weight 지정
        for i in range(len(weights)):
            cid = keyword_counts[i][0]  # cid 값 가져오기
            weight = weights[i]  # 해당 cid에 대한 weight 값 가져오기

            # category 업데이트 쿼리
            update_query = f'''
            UPDATE category
            SET time_initial = {weight}
            WHERE Cid = {cid}
            '''
            cursor.execute(update_query)

        # 변경 사항을 커밋하여 데이터베이스에 반영
        connection.commit()

        ### 업데이트 된 내용 확인 ###
        select_query = f"SELECT Cname, time_initial FROM category"
        cursor.execute(select_query)
        updated_categories = cursor.fetchall()
        print("업데이트된 category 내용:")
        for updated_category in updated_categories:
            cname = updated_category[0]
            time_initial = updated_category[1]
            print(f"Cname: {cname}, time_initial: {time_initial}")
        ### 업데이트 된 내용 확인 ###

        # 커서와 연결 종료
        cursor.close()
        connection.close()

    except Exception as e:
        # 예외 처리
        print('An error occurred:', str(e))

def crawlCheck():
    try:
        connection = MySQLdb.connect(
            host=env('DATABASE_HOST'),
            user=env('DATABASE_USER'),
            passwd=env('DATABASE_PASSWORD'),
            db=env('DATABASE_NAME')
        )
        cursor = connection.cursor()

        # 1시간마다 주기 체크
        update_query = """
            UPDATE category
            SET time_remaining = time_remaining - 1
            WHERE time_remaining > 0
        """
        cursor.execute(update_query)
        connection.commit()

        # 잔여시간이 0인거 추출
        select_query = """
            SELECT *
            FROM category
            INNER JOIN pagetype ON category.Pid_id = pagetype.Pid
            WHERE time_remaining = 0
        """
        cursor.execute(select_query)
        crawl_list = cursor.fetchall()

        # 잔여시간 0이 되면 다시 초기 설정된 주기로 업데이트
        update_query = """
            UPDATE category
            SET time_remaining = time_initial
            WHERE time_remaining = 0
        """
        cursor.execute(update_query)
        connection.commit()

        cursor.close()
        connection.close()

        return crawl(crawl_list)

    except Exception as e:
        # 예외 처리
        print('An error occurred:', str(e))