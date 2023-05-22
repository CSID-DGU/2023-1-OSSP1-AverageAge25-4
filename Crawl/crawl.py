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
    env_file=os.path.join(BASE_DIR, 'Backend', '.env')
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

def crawlInitial():
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

        for category in category_list[0:74]:
            url = category[2]
            page_type = category[5]

            page_num = 1  #페이지

            while True:
                isNext = True
                normal_notice_count = 0  # 페이지내 일반 공지 갯수
                fixed_notice_count = 0  # 페이지내 고정 공지 갯수
                print('\n----- Current Page : {}'.format(page_num), '------\noriginal url : ' + url)
                # 변경된 url에 페이지 번호를 붙임
                url_change = url + f'{page_num}'
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
                            INSERT INTO notice (Cid_id, title, link, time, isSended)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                        try:
                            cursor.execute(insert_query, (category[0], name, link, ntime, True))
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
                    page_num += 1
                else:
                    print('------------------ 게시판의 마지막 페이지라 크롤링 종료 ------------------')
                    break

        cursor.close()
        connection.close()

    except Exception as e:
        # 예외 처리
        print('An error occurred:', str(e))

def crawl(crawl_list):
    try:
        connection = MySQLdb.connect(
            host=env('DATABASE_HOST'),
            user=env('DATABASE_USER'),
            passwd=env('DATABASE_PASSWORD'),
            db=env('DATABASE_NAME')
        )
        cursor = connection.cursor()
        
        print("연결 성공")

        for category in crawl_list:
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
                         INSERT INTO notice (Cid_id, title, link, time, isSended)
                         VALUES (%s, %s, %s, %s, %s)
                     """
                    try:
                        cursor.execute(insert_query, (category[0], name, link, ntime, True))
                        connection.commit()
                    except MySQLdb.IntegrityError as e:
                        # 중복된 항목 처리
                        print("이미 삽입된 항목입니다. 건너뜁니다.")

    except Exception as e:
        # 예외 처리
        print('An error occurred:', str(e))

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
        
        ###기존 내용 확인
        select_query = f"SELECT Cname, time_initial FROM category"
        cursor.execute(select_query)
        old_categories = cursor.fetchall()
        print("기존 category 내용:")
        for old_category in old_categories:
            cname = old_category[0]
            time_initial = old_category[1]
            print(f"Cname: {cname}, time_initial: {time_initial}")

        print("=================================================")

        #가중치를 24개 구간으로 쪼개기
        categories_query = "SELECT * FROM category"
        cursor.execute(categories_query)
        categories = cursor.fetchall()

        #관련 변수 값을 담을 리스트
        keyword_list, day_list, week_list, month_list = [], [], [], []

        #관련 변수값을 리스트에 담기
        for category in categories:
            keyword_query = f"SELECT COUNT(*) FROM keyword WHERE Cid_id = {category[0]}"
            cursor.execute(keyword_query)
            keyword_num = cursor.fetchone()[0]

            day_query = f"SELECT COUNT(*) FROM notice WHERE Cid_id = {category[0]} AND time >= NOW() - INTERVAL 1 DAY"
            cursor.execute(day_query)
            day_num = cursor.fetchone()[0]

            week_query = f"SELECT COUNT(*) FROM notice WHERE Cid_id = {category[0]} AND time >= NOW() - INTERVAL 7 DAY"
            cursor.execute(week_query)
            week_num = cursor.fetchone()[0]

            month_query = f"SELECT COUNT(*) FROM notice WHERE Cid_id = {category[0]} AND time >= NOW() - INTERVAL 30 DAY"
            cursor.execute(month_query)
            month_num = cursor.fetchone()[0]

            keyword_list.append(keyword_num)
            day_list.append(day_num)
            week_list.append(week_num)
            month_list.append(month_num)

        #구간 설정을 위한 최대, 최소 구하기
        keyword_max = max(keyword_list)
        day_max = max(day_list)
        week_max = max(week_list)
        month_max = max(month_list)

        keyword_min = min(keyword_list)
        day_min = min(day_list)
        week_min = min(week_list)
        month_min = min(month_list)


        for category in categories:
            keyword_query = f"SELECT COUNT(*) FROM keyword WHERE Cid_id = {category[0]}"
            cursor.execute(keyword_query)
            keyword_num = cursor.fetchone()[0]

            day_query = f"SELECT COUNT(*) FROM notice WHERE Cid_id = {category[0]} AND time >= NOW() - INTERVAL 1 DAY"
            cursor.execute(day_query)
            day_num = cursor.fetchone()[0]

            week_query = f"SELECT COUNT(*) FROM notice WHERE Cid_id = {category[0]} AND time >= NOW() - INTERVAL 7 DAY"
            cursor.execute(week_query)
            week_num = cursor.fetchone()[0]

            month_query = f"SELECT COUNT(*) FROM notice WHERE Cid_id = {category[0]} AND time >= NOW() - INTERVAL 30 DAY"
            cursor.execute(month_query)
            month_num = cursor.fetchone()[0]

            #가중치를 시간으로 환산
            keyword_percentile = get_percentile(keyword_num, keyword_min, keyword_max)
            day_percentile = get_percentile(day_num, day_min, day_max)
            week_percentile = get_percentile(week_num, week_min, week_max)
            month_percentile = get_percentile(month_num, month_min, month_max)

            #시간에 우선도 반영
            weight = (100 - (keyword_percentile + day_percentile + week_percentile + month_percentile))/4

            update_query = f"UPDATE category SET time_initial = {weight} WHERE Cid = {category[0]}"
            cursor.execute(update_query)

        # 변경 사항을 커밋하여 데이터베이스에 반영
        connection.commit()

        ### 업데이트 된 내용 확인
        select_query = f"SELECT Cname, time_initial FROM category"
        cursor.execute(select_query)
        updated_categories = cursor.fetchall()
        print("업데이트된 category 내용:")
        for updated_category in updated_categories:
            cname = updated_category[0]
            time_initial = updated_category[1]
            print(f"Cname: {cname}, time_initial: {time_initial}")

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