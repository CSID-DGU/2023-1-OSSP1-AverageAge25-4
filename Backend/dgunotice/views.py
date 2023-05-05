from django.shortcuts import render

# Create your views here.
# 크롤링 관련
import threading
import urllib
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
import datetime
import re

def DBInitial():
    category_list = [
        # 동국대메인사이트
        [0, 'http://www.dongguk.edu/article/GENERALNOTICES/', '일반공지'],
        [0, 'http://www.dongguk.edu/article/HAKSANOTICE/', '학사공지'],
        [0, 'http://www.dongguk.edu/article/JANGHAKNOTICE/', '장학공지'],
        [0, 'http://www.dongguk.edu/article/IPSINOTICE/', '입시공지'],
        [0, 'http://www.dongguk.edu/article/GLOBALNOLTICE/', '국제공지'],
        [0, 'http://www.dongguk.edu/article/HAKSULNOTICE/', '학술/행사공지'],
        [0, 'http://www.dongguk.edu/article/BUDDHISTEVENT/', '행사공지'],
        [0, 'http://www.dongguk.edu/article/ALLIM/', '알림사항'],

        # 불교대학
        [1, 'https://bs.dongguk.edu/article/notice/', '불교학부'],
        [1, 'https://ch.dongguk.edu/article/notice/', '문화재학과'],

        # 문과대학
        [1, 'https://liberal.dongguk.edu/article/notice/', '문과대학'],
        [1, 'https://kor-cre.dongguk.edu/article/notice2/', '국어국문문예창작학부'],
        [1, 'https://english.dongguk.edu/article/notice1/', '영어영문학부'],
        [1, 'https://dj.dongguk.edu/article/notice/', '일본학과'],
        [1, 'https://china.dongguk.edu/article/notice/', '중어중문학과'],
        [1, 'https://sophia.dongguk.edu/article/notice/', '철학과'],
        [1, 'https://history.dongguk.edu/article/notice/', '사학과'],

        # 이과대학
        [1, 'https://science.dongguk.edu/article/notice/', '이과대학'],
        [1, 'https://math.dongguk.edu/article/notice/', '수학과'],
        [1, 'https://chem.dongguk.edu/article/notice/', '화학과'],
        [1, 'https://stat.dongguk.edu/article/board1/', '통계학과'],
        [1, 'https://physics.dongguk.edu/article/notice1/', '물리반도체과학부'],

        # 법과대학
        [2, 'https://law.dongguk.edu/article/notice1/', '법학과'],

        # 사회과학대학
        [1, 'https://social.dongguk.edu/article/notice/', '사회과학대학'],
        [1, 'https://politics.dongguk.edu/article/notice2/', '정치외교학전공'],
        [1, 'https://pa.dongguk.edu/article/notice/', '행정학전공'],
        [1, 'https://nk.dongguk.edu/article/notice/', '북한학전공'],
        [1, 'https://econ.dongguk.edu/article/notice/', '경제학과'],
        [2, 'https://itrade.dongguk.edu/article/notice/', '국제통상학전공'],
        [1, 'https://comm.dongguk.edu/article/notice1/', '미디어커뮤니케이션학과'],
        [1, 'https://foodindus.dongguk.edu/article/notice1/', '식품산업관리학과'],
        [1, 'https://sociology.dongguk.edu/article/notice/', '사회학전공'],
        [1, 'https://welfare.dongguk.edu/article/notice/', '사회복지학과'],
        [5, 'http://dguadpr.kr/bbs/board.php?bo_table=table31&page=2', '광고홍보학과'],

        # 경찰사법대학
        [1, 'https://justice.dongguk.edu/article/notice/', '경찰사법대학'],
        [1, 'https://police.dongguk.edu/article/notice1/', '경찰행정학부'],

        # 경영대학
        [1, 'https://sba.dongguk.edu/article/notice/', '경영대학'],
        [2, 'https://mgt.dongguk.edu/article/notice/', '경영학과'],
        [1, 'https://acc.dongguk.edu/article/notice1/', '회계학과'],
        [1, 'https://mis.dongguk.edu/article/news/', '경영정보학과'],

        # 바이오시스템대학
        [1, 'https://life.dongguk.edu/article/notice/', '바이오시스템대학'],

        # 공과대학
        [1, 'https://engineer.dongguk.edu/article/notice1/', '공과대학'],
        [2, 'https://dee.dongguk.edu/article/notice1/', '전자전기공학부'],
        [1, 'https://ice.dongguk.edu/article/notice/', '정보통신공학과'],
        [1, 'https://civil.dongguk.edu/article/notice/', '건설환경공학과'],
        [1, 'https://chembioeng.dongguk.edu/article/notice1/', '화공생물공학과'],
        [1, 'https://mecha.dongguk.edu/article/notice/', '기계로봇에너지공학과'],
        [1, 'https://archi.dongguk.edu/article/info1/', '건축공학과,건축학과'],
        [1, 'https://ise.dongguk.edu/article/notice1/', '산업시스템공학과'],
        [1, 'https://me.dongguk.edu/article/notice/', '융합에너지신소재공학과'],

        # AI융합대학
        [1, 'https://ai.dongguk.edu/article/notice/', 'AI융합대학'],
        [1, 'https://cse.dongguk.edu/article/notice1/', '컴퓨터공학과'],
        [4, 'http://mme.dongguk.edu/k3/sub5/sub1.php?tsort=51&msort=62', '멀티미디어공학과'],

        # 사범대학
        [2, 'https://edu.dongguk.edu/article/notice/', '사범대학'],
        [1, 'https://education.dongguk.edu/article/news2/', '교육학과'],
        [1, 'https://duce.dongguk.edu/article/notice/', '국어교육과'],
        [1, 'https://historyedu.dongguk.edu/article/notice1/', '역사교육과'],
        [1, 'https://geoedu.dongguk.edu/article/notice/', '지리교육과'],
        [1, 'https://dume.dongguk.edu/article/notice/', '수학교육과'],
        [1, 'https://homeedu.dongguk.edu/article/notice/', '가정교육과'],
        [1, 'https://pe.dongguk.edu/article/notice/', '체육교육과'],

        # 예술대학
        [1, 'https://art.dongguk.edu/article/notice/', '예술대학'],
        [1, 'https://aart.dongguk.edu/article/notice/', '미술학부'], #공지사항 없음
        [1, 'https://theatre.dongguk.edu/article/notice/', '연극학부'],
        [1, 'https://kmart.dongguk.edu/article/notice/', '한국음악과'],
        [5, 'https://movie.dongguk.edu/bbs/board.php?bo_table=movie1_3_1', '영화영상학과'],

        # 약학대학
        [1, 'https://pharm.dongguk.edu/article/notice/', '약학과'],

        # 다르마칼리지
        [1, 'https://dharma.dongguk.edu/article/notice/', '다르마칼리지'],

        #미래융합대학
        [3, 'https://security.dongguk.edu/bbs/data/list.do?menu_idx=30', '융합보안학과'],
        [3, 'https://swc.dongguk.edu/bbs/data/list.do?menu_idx=46', '사회복지상담학과'],
        [3, 'https://gt.dongguk.edu/bbs/data/list.do?menu_idx=58', ' 글로벌무역학과'],

        #시설공지
        [6,'https://lib.dongguk.edu/bbs/list/1','중앙도서관'],
        [1,'https://dorm.dongguk.edu/article/notice/list', '기숙사'],
        [7,'https://dgucoop.dongguk.edu/board/board.php?w=1', '생협'],

        #기타공지



    ]
    for i,category in enumerate(category_list):
        pass






def crawl():
    print('======================================')
    print(datetime.datetime.now())
    print('======================================')
    threading.Timer(3600, crawl).start()  # 1시간 마다 주시적으로 실행

    new_crawl_list = []  # 알림 발송할 신규 크롤링 공지 리스트
    new_crawl_list.clear()  # 알림 발송할 신규 크롤링 공지 리스트 : 새로운 것만 들어가야 하므로, 크롤링 실행 전 초기화
    new_crawl_count = 0  # 신규로 크롤링한 건수 체크

    time.sleep(3)  # 검색 결과가 렌더링 될 때까지 잠시 대기
    curPage = 1  # 현재 페이지
    totalPage = 1  # 크롤링할 전체 페이지수
    site_per = 0  # 한 페이지의 게시글 체크용
    loop_index = 0  # 미융대 게시글 관련

    # 0. div.board_list > ul > li
    # 1. table.board > tbody > tr
    # 2. table.board_list n_list >tbody > tr.cell_notice > td.cell_type
    url_list = [

        # 동국대메인사이트
        [0, 'http://www.dongguk.edu/article/GENERALNOTICES/', '일반공지'],
        [0, 'http://www.dongguk.edu/article/HAKSANOTICE/', '학사공지'],
        [0, 'http://www.dongguk.edu/article/JANGHAKNOTICE/', '장학공지'],
        [0, 'http://www.dongguk.edu/article/IPSINOTICE/', '입시공지'],
        [0, 'http://www.dongguk.edu/article/GLOBALNOLTICE/', '국제공지'],
        [0, 'http://www.dongguk.edu/article/HAKSULNOTICE/', '학술/행사공지'],
        [0, 'http://www.dongguk.edu/article/BUDDHISTEVENT/', '행사공지'],
        [0, 'http://www.dongguk.edu/article/ALLIM/', '알림사항'],

        # 불교대학
        [1, 'https://bs.dongguk.edu/article/notice/', '불교학부'],
        [1, 'https://ch.dongguk.edu/article/notice/', '문화재학과'],

        # 문과대학
        [1, 'https://kor-cre.dongguk.edu/article/notice2/', '문과대학 국어국문문예창작학부'],
        [1, 'https://kor-cre.dongguk.edu/article/info/', '국어국문문예창작학부'],
        [1, 'https://english.dongguk.edu/article/notice1/', '영어영문학부'],
        [1, 'https://dj.dongguk.edu/article/notice/', '일본학과'],
        [1, 'https://china.dongguk.edu/article/notice/', '중어중문학과'],
        [1, 'https://sophia.dongguk.edu/article/notice/', '철학과'],
        [1, 'https://history.dongguk.edu/article/notice/', '사학과'],

        # 이과대학
        [1, 'https://math.dongguk.edu/article/notice/', '수학과'],
        [1, 'https://chem.dongguk.edu/article/notice/', '화학과'],
        [1, 'https://stat.dongguk.edu/article/board1/', '통계학과'],
        [1, 'https://physics.dongguk.edu/article/notice1/', '물리.반도체과학부'],

        # 법과대학
        [1, 'https://law.dongguk.edu/article/notice1/', '법학과'],

        # 사회과학대학
        [1, 'https://politics.dongguk.edu/article/notice2/', '정치외교학전공'],
        [1, 'https://pa.dongguk.edu/article/notice/', '행정학전공'],
        [1, 'https://nk.dongguk.edu/article/notice/', '북한학전공'],
        [1, 'https://econ.dongguk.edu/article/notice/', '경제학과'],
        [1, 'https://itrade.dongguk.edu/article/notice/', '국제통상학전공'],
        [1, 'https://comm.dongguk.edu/article/notice1/', '미디어커뮤니케이션학과 - 학사공지'],
        [1, 'https://comm.dongguk.edu/article/notice2/', '미디어커뮤니케이션학과 - 일반공지'],
        [1, 'https://comm.dongguk.edu/article/notice3/', '미디어커뮤니케이션학과 - 취업공지'],
        [1, 'https://foodindus.dongguk.edu/article/notice1/', '식품산업관리학과'],
        [1, 'https://sociology.dongguk.edu/article/notice/', '사회학전공'],
        [1, 'https://welfare.dongguk.edu/article/notice/', '사회복지학과'],

        # 경찰사법대학
        [1, 'https://police.dongguk.edu/article/notice1/', '경찰행정학부'],

        # 경영대학
        [1, 'https://mgt.dongguk.edu/article/notice/', '경영학과'],
        [1, 'https://acc.dongguk.edu/article/notice1/', '회계학과'],
        [1, 'https://mis.dongguk.edu/article/news/', '경영정보학과'],

        # 바이오시스템대학
        [1, 'https://life.dongguk.edu/article/notice/', '바이오시스템대학'],

        # 공과대학
        [1, 'https://dee.dongguk.edu/article/notice1/', '전자전기공학부'],
        [1, 'https://ice.dongguk.edu/article/notice/', '정보통신공학과'],
        [1, 'https://civil.dongguk.edu/article/notice/', '건설환경공학과'],
        [1, 'https://chembioeng.dongguk.edu/article/notice1/', '화공생물공학과'],
        [1, 'https://mecha.dongguk.edu/article/notice/', '기계로봇에너지공학과'],
        [1, 'https://archi.dongguk.edu/article/info1/', '건축공학과,건축학과'],
        [1, 'https://ise.dongguk.edu/article/notice1/', '산업시스템공학과'],
        [1, 'https://me.dongguk.edu/article/notice/', '융합에너지신소재공학과'],

        # AI융합대학
        [1, 'https://ai.dongguk.edu/article/notice/', 'AI소프트웨어융합학부'],
        [1, 'https://cse.dongguk.edu/article/notice1/', '컴퓨터공학과'],
        [4, 'http://mme.dongguk.edu/k3/sub5/sub1.php?tsort=51&msort=62', '멀티미디어공학과'],

        # 사범대학
        [2, 'https://edu.dongguk.edu/article/notice/', '사범대학'],
        [1, 'https://education.dongguk.edu/article/news2/', '교육학과'],
        [1, 'https://duce.dongguk.edu/article/notice/', '국어교육과'],
        [1, 'https://historyedu.dongguk.edu/article/notice1/', '역사교육과'],
        [1, 'https://geoedu.dongguk.edu/article/notice/', '지리교육과'],
        [1, 'https://dume.dongguk.edu/article/notice/', '수학교육과'],
        [1, 'https://homeedu.dongguk.edu/article/notice/', '가정교육과'],
        [1, 'https://pe.dongguk.edu/article/notice/', '체육교육과'],

        # 예술대학
        # [1, 'https://aart.dongguk.edu/article/notice/', '미술학부'], 공지사항 없음
        [1, 'https://theatre.dongguk.edu/article/notice/', '연극학부'],
        [1, 'https://kmart.dongguk.edu/article/notice/', '한국음악과'],

        # 약학대학
        [1, 'https://pharm.dongguk.edu/article/notice/', '약학과'],

        # 다르마칼리지
        [1, 'https://dharma.dongguk.edu/article/notice/', '다르마칼리지'],


    ]

    # 예외 사이트
    """
    # 융합대학

      # 멀미난다...

    """

    # 사이트마다 페이징을 위한 변수가 다름.
    page_list = [
        'list?pageIndex=',
        'list?pageIndex=',
        'list?pageIndex=',
    ]

    # 1. 전체 2. 공지글분류 3. url
    crawl_var_list = [
        ['div.board_list > ul > li', 'div.mark > span', 'a', 'p.tit'],
        ['table.board > tbody > tr', 'td.td_num > span', 'td.td_tit > a'],
        ['table.board > tbody > tr', 'td.td_num > span', 'td.td_tit > a'],
        ['table.board_list n_list > tbody > tr.cell_notice > td.cell_type']
    ]

    # 데이터베이스에 저장할 게시글의 링크용
    link_list = [
        '/article/notice/',
        '/article/notice/',
        '/article/notice1/',
    ]

    for list in url_list:

        url = list[1]  # url_list가 2차원 배열이므로, 공지사항 링크를 변수 url에 저장
        now_site_type = list[0]  # 현재 사이트 type 저장
        curPage = 1  # url_list의 loop를 돌면서 url이 변경될 때 마다 현재 페이지를 1로 설정
        site_per = 0  # url_list의 loop를 돌면서 url이 변경될 때 마다 크롤링 한 게시글의 개수 파악

        while curPage <= totalPage:

            # 페이지 번호 출력
            print('\n----- Current Page : {}'.format(curPage), '------\noriginal url : ' + url)

            # 변경된 url에 페이지 번호를 붙임
            if now_site_type == 0 or now_site_type == 1:
                url_change = url + page_list[now_site_type] + f'{curPage}'
            else:
                pass
            print('changed url : ' + url_change + '\n-------------------------------------------------')

            # 페이지가 변경됨에 따라 delay 발생 시킴
            time.sleep(3)

            # 변경된 url로 이동하여 크롤링하기 위해 html 페이지를 파싱
            html = urllib.request.urlopen(url_change).read()
            soup = BeautifulSoup(html, 'html.parser')

            # 게시글 리스트 선택
            if now_site_type == 0 or now_site_type == 1:
                board_list = soup.select(crawl_var_list[now_site_type][0])
            else:
                pass

            # 카테고리 정보는 크롤링하지 않고 2차원 배열에 저장한 값을 읽음.
            category = list[2]

            for board in board_list:
                # 고정된 공지는 td > img 형태인데, 이를 text로 변환하면 공백이 됨
                # type3는 None 값이 발생하여 예외처리
                if now_site_type == 0 or now_site_type == 1:
                    notice = board.select_one(crawl_var_list[now_site_type][1])
                else:
                    pass

                # 고정 공지인 경우 패스
                if notice['class'][0] == "fix" or notice['class'][0] == "mark":
                    continue

                else:  # 값이 있는 경우 일반공지로, 크롤링 진행
                    # 게시글 제목
                    if now_site_type == 0:
                        name = board.select_one(crawl_var_list[now_site_type][3]).text.strip()
                    elif now_site_type == 1:
                        name = board.select_one(crawl_var_list[now_site_type][2]).text.strip()

                    # 게시글 링크는 경우에 따라 편집 필요
                    # 1) 공백이면 편집
                    if now_site_type == 0:
                        link = url + 'detail/' + re.sub(r'[^0-9]', '',
                                                        board.select_one(crawl_var_list[now_site_type][2])['onclick'])
                    # 4) 특정 url 사용
                    else:
                        link = re.sub(r'\/article\/(notice\d*|news\d*|info\d*|board\d*)\/', '', url) + \
                               board.select_one(crawl_var_list[now_site_type][2])['href']

                    now_time = str(datetime.datetime.now())
                    print("카테고리 : ", category)
                    print("공지이름 : ", name.replace("\xa0", " "))
                    print("링크 : ", link)
                    print("시간 : ", now_time)

                    '''
                    # DB에 저장
                    results = session.query(Crawl.link).filter_by(category=category, link=link).all()
                    if not results:
                        now_time = str(datetime.datetime.now())
                        session.add(Crawl(category=category, title=name, link=link, crawl_time=now_time))
                        session.commit()
                        print('성공 : [' + category + ']' + name + ' >> ' + link)

                        # new_crawl_list를 2차원 형태로 만들어서 신규 크롤링 데이터 추가
                        new_crawl_list.append([])
                        new_crawl_list[new_crawl_count].append(category)
                        new_crawl_list[new_crawl_count].append(name.replace("\xa0", " "))
                        new_crawl_list[new_crawl_count].append(link)
                        new_crawl_list[new_crawl_count].append(now_time)

                        # 유사 단어 찾아서 알림 발송하기
                        #findSimilar(new_crawl_list)
                        #send_kakao(new_crawl_list[new_crawl_count])

                        new_crawl_count += 1
                    else:
                        print('     실패 : [' + category + ']' + name + ' >> ' + link)

                    '''
                    # 크롤링 한 게시글 개수 증가
                    site_per += 1

            # 현재 페이지의 게시글을 크롤링하는 for loop 종료

            # 페이지 수 증가
            curPage += 1

            if now_site_type == 9999:
                pass
            else:
                if site_per < 10:
                    print('------------------ 게시글 개수가 적어서 현재 페이지에서 크롤링 종료 (15) ------------------')
                    break

            if curPage > totalPage:
                print('------------------ ' + category + ' 크롤링 종료 ------------------')
                break

            # 3초간 대기
            time.sleep(3)

        # 미래융합대학 학과별 사이트 상세링크 관련
        if now_site_type == 6:
            loop_index += 1

    print("~~~ 크롤링 끄읕 !!!")

    del soup  # BeautifulSoup 인스턴스 삭제


#    session.close()  # DB 세션 종료
#    return "크롤링 페이지"

crawl()
