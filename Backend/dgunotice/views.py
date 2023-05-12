from django.db.models import F
from django.views import View
from django.shortcuts import render, redirect
from .models import Pagetype, Category, User, Keyword, Notice
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import PagetypeSerializer, CategorySerializer,UserSerializer, KeywordSerializer, NoticeSerializer
from django.db.models import F

# Create your views here.
# 크롤링 관련
import urllib
from bs4 import BeautifulSoup
import time
import random
import threading
import datetime
import re

def testPage(request):
    return render(request, 'test.html')

def DBInitial(request):
    #먼저 테이블 데이터 전체 제거후 진행
    Pagetype.objects.all().delete()
    Category.objects.all().delete()
    User.objects.all().delete()
    Keyword.objects.all().delete()
    Notice.objects.all().delete()

    #페이지타입(pid), 공지리스트(Nlist), 공지이름(Nname), 공지링크(Nlink), 공지시간(Ntime)
    pageType_list = [
        [0, 'div.board_list > ul > li', 'a > div.mark > span', 'a > div.top > p.tit', 'a', 'a > div.top > div.info > span:nth-child(1)'],
        [1, 'table.board > tbody > tr', 'td.td_num > span', 'td.td_tit > a', 'td.td_tit > a', 'td:nth-child(4)'],
        [2, 'table.board > tbody > tr', 'td.td_num > span', 'td.td_tit > a', 'td.td_tit > a', 'td:nth-child(4)'],
        [3, 'table > tbody > tr', '', 'td.cell_type > a', 'td.cell_type > a', 'td:nth-child(5)'],
        [4, 'table> tbody > tr', ' td:nth-child(1)', ' td.subject > a', ' td.subject > a', 'td.w_date'],
        [5, 'table > tbody >  tr', '', 'td.td_subject > a:nth-child(2)', 'td.td_subject > a:nth-child(2)', 'd.td_date'],
        [6, 'table > tbody > tr ', '', 'td.title.expand > a', 'td.title.expand > a', 'td.reportDate'],
        [7, 'table > tbody > tr', '', 'td:nth-child(2)', '', ' td:nth-child(5)']
    ]

    for page in pageType_list:
        p = Pagetype(
            Pid=page[0],
            Nlist=page[1],
            Nfixed=page[2],
            Nname=page[3],
            Nlink=page[4],
            Ntime=page[5]
        )
        p.save()

    # 카테고리(Cname), URL링크(Clink), 페이지타입(pid)
    category_list = [
        ['일반공지', 'http://www.dongguk.edu/article/GENERALNOTICES/list?pageIndex=', 0],
        ['학사공지', 'http://www.dongguk.edu/article/HAKSANOTICE/list?pageIndex=', 0],
        ['장학공지', 'http://www.dongguk.edu/article/JANGHAKNOTICE/list?pageIndex=', 0],
        ['입시공지', 'http://www.dongguk.edu/article/IPSINOTICE/list?pageIndex=', 0],
        ['국제공지', 'http://www.dongguk.edu/article/GLOBALNOLTICE/list?pageIndex=', 0],
        ['학술/행사공지', 'http://www.dongguk.edu/article/HAKSULNOTICE/list?pageIndex=', 0],
        ['행사공지', 'http://www.dongguk.edu/article/BUDDHISTEVENT/list?pageIndex=', 0],
        ['알림사항', 'http://www.dongguk.edu/article/ALLIM/list?pageIndex=', 0],
        ['불교학부', 'https://bs.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['문화재학과', 'https://ch.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['문과대학', 'https://liberal.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['국어국문문예창작학부', 'https://kor-cre.dongguk.edu/article/notice2/list?pageIndex=', 1],
        ['영어영문학부', 'https://english.dongguk.edu/article/notice1/list?pageIndex=', 1],
        ['일본학과', 'https://dj.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['중어중문학과', 'https://china.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['철학과', 'https://sophia.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['사학과', 'https://history.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['이과대학', 'https://science.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['수학과', 'https://math.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['화학과', 'https://chem.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['통계학과', 'https://stat.dongguk.edu/article/board1/list?pageIndex=', 1],
        ['물리반도체과학부', 'https://physics.dongguk.edu/article/notice1/list?pageIndex=', 1],
        ['법학과', 'https://law.dongguk.edu/article/notice1/list?pageIndex=', 2],
        ['사회과학대학', 'https://social.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['정치외교학전공', 'https://politics.dongguk.edu/article/notice2/list?pageIndex=', 1],
        ['행정학전공', 'https://pa.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['북한학전공', 'https://nk.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['경제학과', 'https://econ.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['국제통상학전공', 'https://itrade.dongguk.edu/article/notice/list?pageIndex=', 2],
        ['미디어커뮤니케이션학과', 'https://comm.dongguk.edu/article/notice1/list?pageIndex=', 1],
        ['식품산업관리학과', 'https://foodindus.dongguk.edu/article/notice1/list?pageIndex=', 1],
        ['사회학전공', 'https://sociology.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['사회복지학과', 'https://welfare.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['광고홍보학과', 'http://dguadpr.kr/bbs/board.php?bo_table=table31&page=', 5],
        ['경찰사법대학', 'https://justice.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['경찰행정학부', 'https://police.dongguk.edu/article/notice1/list?pageIndex=', 1],
        ['경영대학', 'https://sba.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['경영학과', 'https://mgt.dongguk.edu/article/notice/list?pageIndex=', 2],
        ['회계학과', 'https://acc.dongguk.edu/article/notice1/list?pageIndex=', 1],
        ['경영정보학과', 'https://mis.dongguk.edu/article/news/list?pageIndex=', 1],
        ['바이오시스템대학', 'https://life.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['공과대학', 'https://engineer.dongguk.edu/article/notice1/list?pageIndex=', 1],
        ['전자전기공학부', 'https://dee.dongguk.edu/article/notice1/list?pageIndex=', 2],
        ['정보통신공학과', 'https://ice.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['건설환경공학과', 'https://civil.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['화공생물공학과', 'https://chembioeng.dongguk.edu/article/notice1/list?pageIndex=', 1],
        ['기계로봇에너지공학과', 'https://mecha.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['건축공학과,건축학과', 'https://archi.dongguk.edu/article/info1/list?pageIndex=', 1],
        ['산업시스템공학과', 'https://ise.dongguk.edu/article/notice1/list?pageIndex=', 1],
        ['융합에너지신소재공학과', 'https://me.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['AI융합대학', 'https://ai.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['컴퓨터공학과', 'https://cse.dongguk.edu/article/notice1/list?pageIndex=', 1],
        ['멀티미디어공학과', 'http://mme.dongguk.edu/k3/sub5/sub1.php?page=', 4],
        ['사범대학', 'https://edu.dongguk.edu/article/notice/list?pageIndex=', 2],
        ['교육학과', 'https://education.dongguk.edu/article/news2/list?pageIndex=', 1],
        ['국어교육과', 'https://duce.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['역사교육과', 'https://historyedu.dongguk.edu/article/notice1/list?pageIndex=', 1],
        ['지리교육과', 'https://geoedu.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['수학교육과', 'https://dume.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['가정교육과', 'https://homeedu.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['체육교육과', 'https://pe.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['예술대학', 'https://art.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['미술학부', 'https://aart.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['연극학부', 'https://theatre.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['한국음악과', 'https://kmart.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['영화영상학과', 'https://movie.dongguk.edu/movie1_3_1/p', 5],
        ['약학과', 'https://pharm.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['다르마칼리지', 'https://dharma.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['융합보안학과', 'https://security.dongguk.edu/bbs/data/list.do?menu_idx=30&pageIndex=', 3],
        ['사회복지상담학과', 'https://swc.dongguk.edu/bbs/data/list.do?menu_idx=46&pageIndex=', 3],
        ['글로벌무역학과', 'https://gt.dongguk.edu/bbs/data/list.do?menu_idx=58&pageIndex=', 3],
        ['중앙도서관', 'https://lib.dongguk.edu/bbs/list/1?pn=', 6],
        ['기숙사', 'https://dorm.dongguk.edu/article/notice/list?pageIndex=', 1],
        ['생협', 'https://dgucoop.dongguk.edu/board/board.php?w=1&page=', 7]
    ]

    # Pagetype 테이블에 저장된 객체 중 Pid 값이 0, 1, 2, ... 인 객체들을
    # 찾아서 pid_list에 저장한다.
    pid_list = list(Pagetype.objects.filter(Pid__in=range(len(category_list))))

    # Category 테이블에 데이터를 추가한다.
    for i in range(len(category_list)):
        c = Category(Cid=i + 1,
                     Cname=category_list[i][0],
                     Clink=category_list[i][1],
                     Pid=pid_list[category_list[i][2]])
        c.save()

    u = User(Uid="9999",
             phone="010-1234-5678",
             college=Category.objects.get(Cname='AI융합대학'),
             department=Category.objects.get(Cname='컴퓨터공학과'),
             sub_college=Category.objects.get(Cname='이과대학'),
             sub_department=Category.objects.get(Cname='물리반도체과학부')
    )
    u.save()

    return render(request, 'DBtest.html')


def crawlInitial(request):
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

            # 변경된 url로 이동하여 크롤링하기 위해 html 페이지를 파싱
            html = urllib.request.urlopen(url_change).read()
            soup = BeautifulSoup(html, 'html.parser')

            # 게시글 리스트 선택
            notice_list = soup.select(category.Pid.Nlist)

            for notice in notice_list:
                #고정 공지는 건너뛰기
                is_fixed = notice.select_one(category.Pid.Nfixed)
                if (page_type == 0 and is_fixed.get("class") == ["fix"]) or \
                    (page_type in [1, 2] and is_fixed.get("class") == ["mark"]) or \
                    (page_type == 3 and notice.get("class") == ["cell_notice"]) or \
                    (page_type == 4 and is_fixed.find("img") is not None) or \
                    (page_type == 5 and is_fixed.get("class") == ["bo_notice"]) or \
                    (page_type == 6 and notice.get("class") == ["always"]):
                    fixed_notice_count += 1
                    continue

                #게시글 제목
                name_tag = notice.select_one(category.Pid.Nname)
                if page_type == 2:
                    name_tag = name_tag.select_one("span").extract()

                name = name_tag.text.strip()

                #게시글 링크
                link_tag = notice.select_one(category.Pid.Nlink)
                link = ""
                if page_type == 0:
                    link = re.sub(r'list\?pageIndex=', 'detail/', url) + re.sub(r'[^0-9]', '', link_tag.get('onclick'))
                elif page_type == 1 or page_type == 2:
                    link = re.sub(r'\/article\/(notice\d*|news\d*|info\d*|board\d*)\/list\?pageIndex=', '', url) + link_tag.get('href')
                elif page_type == 3:
                    link = link_tag.get('href') #추가 조치 필요
                elif page_type == 4:
                    link = re.sub(r'/k3/sub5/sub1.php\?page=', '', url) + link_tag.get('href')
                elif page_type == 5:
                    link = link_tag.get('href')
                elif page_type == 6:
                    link = re.sub(r'/bbs/list/1\?pn=', '', url) + link_tag.get('href')
                elif page_type == 7:
                    link = link_tag.get('onclick') #추가 조치 필요
                    
                #게시글 날짜
                ntime = notice.select_one(category.Pid.Ntime).text.strip()

                print("카테고리 : ", category)
                print("공지이름 : ", name.replace("\xa0", " "))
                print("링크 : ", link)
                print("시간 : ", ntime)

                n = Notice(Cid=category,
                           title=name.replace("\xa0", " "),
                           link=link,
                           time=ntime)
                n.save()

                # 크롤링 한 게시글 개수 증가
                normal_notice_count += 1

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

    return render(request, 'crawlTest.html')

def crawl(crawl_list):
    pass

def frequencyUpdate():
    #하루마다 업데이트
    threading.Timer(86400, frequencyUpdate).start()


   #가중치를 24개 구간으로 쪼개기
    def get_percentile(value, min_value, max_value):
        percentile = (value - min_value) / (max_value - min_value) * 23 + 1
        return int(percentile)


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

    #구간 설정을 위한 최대, 최소 구하기
    keyword_max = max(keyword_list)
    day_max = max(day_list)
    week_max = max(week_list)
    month_max = max(week_list)

    keyword_min = min(keyword_list)
    day_min = min(day_list)
    week_min = min(week_list)
    month_min = min(month_list)

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
        weight = (100 - keyword_percentile + day_percentile + week_percentile + month_percentile)/4

        Category.objects.filter(pk=category.Cid).update(time_initial=weight)

def crawlCheck():
    # 1시간마다 주기 체크
    threading.Timer(3600, crawlCheck).start()
    Category.objects.filter(time_remaining__gt=0).update(
        time_remaining=F('time_remaining') - 1
    )
    crawl_list = Category.objects.filter(time_remaining=0)
    crawl_list.update(time_remaining=F('time_initial'))
    return crawl(crawl_list)

class LoginPageView(View):
    def get(self, request):
        return render(request, 'loginPage.html')

    def post(self, request):
        uid = request.POST.get('uid')
        phone = request.POST.get('phone')

        user = User.objects.filter(Uid=uid, phone=phone).first()

        if user:
            request.session['user_id'] = uid
            return redirect('mainPage')
        else:
            context = {'error_message': '해당하는 유저가 없습니다.'}
            return render(request, 'loginPage.html', context)

class NoticeR(APIView):
    def get(self, request):
        # 세션에서 Uid값을 가져옴
        Uid = request.session.get('Uid')

        # User.notice_order에서 Cid값을 가져옴
        cid_list = list(map(int, list(str(User.objects.get(Uid=Uid).notice_order))))

        # Category와 그에 연결된 Notice를 가져옴
        categories = Category.objects.filter(Cid__in=cid_list)
        notices = Notice.objects.filter(Cid__in=cid_list)

        # Category와 Notice 객체를 serialize
        category_serializer = CategorySerializer(categories, many=True)
        notice_serializer = NoticeSerializer(notices, many=True)

        # Serializer로부터 JSON Response 생성
        response_data = {
            'categories': category_serializer.data,
            'notices': notice_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)

class KeywordCR(generics.ListCreateAPIView):
    serializer_class = KeywordSerializer

    def get_queryset(self):
        #get요청시 user_id에 해당하는 키워드 리스트 전달
        user_id = self.request.session.get('user_id')
        queryset = Keyword.objects.filter(Uid_id=user_id)
        return queryset

    def create(self, request, *args, **kwargs):
        #POST요청시 키워드 추가
        #전달된 데이터(request.data)를 serializer에 저장 many = True로 복수개 생성 가능
        serializer = self.get_serializer(data=request.data, many=True)

        #전달된 데이터의 유효성 검사
        serializer.is_valid(raise_exception=True)

        #세션에 저장된 유저id 가져와 serializer에 넣고 객체 추가
        user_id = request.session.get('user_id')
        serializer.save(Uid_id=user_id)

        #마지막으로 생성된 객체를 클라이언트에게 반환
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class KeywordUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = KeywordSerializer

    def get_queryset(self):
        #Uid와 삭제하고 싶은 key에 해당하는 쿼리셋을 queryset에 저장
        user_id = self.request.session.get('user_id')
        queryset = Keyword.objects.filter(Uid_id=user_id, key=self.kwargs.get('key'))
        return queryset

    def delete(self, request, *args, **kwargs):
        #queryset 삭제 진행
        queryset = self.get_queryset()
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)