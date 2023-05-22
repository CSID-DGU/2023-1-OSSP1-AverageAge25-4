from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from .models import Pagetype, Category, User, Keyword, Notice
from Background.similar import tokenizedKey, getSimKey

os_path = '../../Crawl/model/ko.bin'
own_path = '../../Crawl/model/ko_own.bin'
combined_path = '../../Crawl/model/ko_combined.bin'

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
        [3, 'table > tbody > tr', 'self', 'td.cell_type > a', 'td.cell_type > a', 'td:nth-child(5)'],
        [4, 'table> tbody > tr', ' td:nth-child(1)', ' td.subject > a', ' td.subject > a', 'td.w_date'],
        [5, 'table > tbody >  tr', 'self', 'td.td_subject > a:nth-child(2)', 'td.td_subject > a:nth-child(2)', 'td.td_date'],
        [6, 'table > tbody > tr ', 'self', 'td.title > a', 'td.title > a', 'td.reportDate'],
        [7, 'table > tbody > tr', 'self', 'td:nth-child(2)', 'self', ' td:nth-child(5)']
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

    return render(request, 'DBtest.html')

# class NoticeR(APIView):
#     def get(self, request):
#         # 세션에서 Uid값을 가져옴
#         Uid = request.session.get('Uid')
#
#         # User.notice_order에서 Cid값을 가져옴
#         notice_order = User.objects.get(Uid=Uid).notice_order
#         cid_list = list(map(int, notice_order.split("/")))
#
#         # Category와 그에 연결된 Notice를 가져옴
#         categories = Category.objects.filter(Cid__in=cid_list)
#         notices = Notice.objects.filter(Cid__in=cid_list)
#
#         # Category와 Notice 객체를 serialize
#         category_serializer = CategorySerializer(categories, many=True)
#         notice_serializer = NoticeSerializer(notices, many=True)
#
#         # Serializer로부터 JSON Response 생성
#         response_data = {
#             'categories': category_serializer.data,
#             'notices': notice_serializer.data
#         }
#
#         return Response(response_data, status=status.HTTP_200_OK)
#
# class KeywordCR(generics.ListCreateAPIView):
#     serializer_class = KeywordSerializer
#
#     def get_queryset(self):
#         #get요청시 user_id에 해당하는 키워드 리스트 전달
#         user_id = self.request.session.get('user_id')
#         queryset = Keyword.objects.filter(Uid_id=user_id)
#         return queryset
#
#     def create(self, request, *args, **kwargs):
#         #POST요청시 키워드 추가
#         #전달된 데이터(request.data)를 serializer에 저장 many = True로 복수개 생성 가능
#         serializer = self.get_serializer(data=request.data, many=True)
#
#         #전달된 데이터의 유효성 검사
#         serializer.is_valid(raise_exception=True)
#
#         #세션에 저장된 유저id 가져와 serializer에 넣고 객체 추가
#         user_id = request.session.get('user_id')
#         serializer.save(Uid_id=user_id)
#
#         #마지막으로 생성된 객체를 클라이언트에게 반환
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
# class KeywordUD(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = KeywordSerializer
#
#     def get_queryset(self):
#         #Uid와 삭제하고 싶은 key에 해당하는 쿼리셋을 queryset에 저장
#         user_id = self.request.session.get('user_id')
#         queryset = Keyword.objects.filter(Uid_id=user_id, key=self.kwargs.get('key'))
#         return queryset
#
#     def delete(self, request, *args, **kwargs):
#         #queryset 삭제 진행
#         queryset = self.get_queryset()
#         queryset.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

class SignupView(View):
    template_name = 'signup.html'
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        uid = request.POST.get('uid')
        password = request.POST.get('password')
        pwcheck = request.POST.get('pwcheck')

        error_message = None

        # 이메일 중복 및 패스워드 확인
        if User.objects.filter(Uid=uid).exists():
            error_message = "해당 이메일이 이미 존재합니다."
        elif password != pwcheck:
            error_message = "패스워드 확인이 틀렸습니다."

        if error_message is not None:
            context = {
                'uid': uid,
                'password': password,
                'pwcheck': pwcheck,
                'error_message': error_message,
            }
            return render(request, self.template_name, context)

        hashed_password = make_password(password)

        print(hashed_password)
        print(password)
        user = User(
            Uid=uid,
            password=hashed_password
        )

        user.save()

        return redirect('Login')

class LoginView(View):
    def post(self, request):
        uid = request.POST.get('uid')
        password = request.POST.get('password')

        # Uid를 이용해 User 찾기 (없으면 None 반환)
        user = User.objects.filter(Uid=uid).first()
        if user is not None and check_password(password, user.password):
            request.session['user_id'] = uid
            return redirect('/mainPage')
        else:
            error_message = '이메일 또는 비밀번호가 잘못되었습니다.'
            context = {
                'uid': uid,
                'password': password,
                'error_message': error_message,
            }
            return render(request, 'loginPage.html', context)

    def get(self, request):
        return render(request, 'loginPage.html')

class MainPageView(View):
    def get(self, request):
        user_id = self.request.session.get('user_id')
        keywords = Keyword.objects.filter(Uid_id=user_id)
        # User.notice_order에서 Cid값을 가져옴
        notice_order = User.objects.get(Uid=user_id).notice_order
        cid_list = list(map(int, notice_order.split("/")))

        # Category와 그에 연결된 Notice를 가져옴
        categories = Category.objects.filter(Cid__in=cid_list)

        # 모든 Category를 가져옴
        allcategory = Category.objects.all()

        context = {
            'keywords': keywords,
            'categories': categories,
            'allcategory' : allcategory
        }

        # Render the template with the data
        return render(request, 'mainPageTest.html', context)

class SearchView(View):
    def get(self, request):
        keyword = request.GET.get('keyword')
        keywords_tokenized = tokenizedKey(keyword)
        keywords_similar = []

        for keyword_tokenized in keywords_tokenized:
            keywords_similar += getSimKey(keyword_tokenized, 5)


        # 제목 필드에서 검색어를 포함하는 공지사항 검색
        notices = Notice.objects.filter(title__icontains=keyword)

        context = {
            'notices': notices,
            'keyword': keyword,
            'keywords_similar' : keywords_similar,
        }

        return render(request, 'searchPage.html', context)


