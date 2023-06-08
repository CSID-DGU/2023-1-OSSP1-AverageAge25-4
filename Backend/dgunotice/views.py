from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from django.urls import reverse
from .models import Pagetype, Category, User, Keyword, Notice, Verify
from .similar2 import getSimKey
from .smtp2 import verify_email_token, generate_token, sendEmail, generate_verification_link
from .SecurityModule import Key
path = '../Background/model/ko_modified.bin'


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
        key = Key()
        print(key.key)

        uid = request.POST.get('uid')
        uid_encrypt = key.encrypt(uid)
        password = request.POST.get('password')
        pwcheck = request.POST.get('pwcheck')
        email_consent = request.POST.get('email_consent')

        error_message = None
        # print(email_consent)
        # 이메일 수신 동의 확인
        if not email_consent:
            error_message = "이메일 수신 비 동의시 서비스 회원가입이 제한됩니다"

        # 이메일 중복 및 패스워드 확인
        user_uids = list(User.objects.values_list('Uid', flat=True))
        duplicate_check = False
        print(user_uids)

        if user_uids:
            for user_uid in user_uids:
                if uid == key.decrypt(user_uid):
                    duplicate_check = True
                    break

        if duplicate_check == True:
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

        # print(hashed_password)
        # print(password)

        # 중복 테스트 ( 이메일은 같은데 토큰이 여러개 생기면 안되기때문 )
        verify_temp_ids = list(Verify.objects.values_list('temp_id', flat=True))

        if verify_temp_ids:
            for verify_temp_id in verify_temp_ids:
                if uid == key.decrypt(verify_temp_id):
                    Verify.objects.filter(temp_id=verify_temp_id).first().delete()
                    break

        # record = Verify.objects.filter(temp_id=uid_encrypt).first()
        #
        # # 중복이면 삭제
        # if record:
        #     record.delete()

        # 토큰 생성
        tok = generate_token(15)

        # Verify 레코드 생성
        verify = Verify(
            temp_id=uid_encrypt,
            temp_password=hashed_password,
            token=tok
        )
        print(uid_encrypt)
        verify.save()

        # 인증 링크 생성
        link = generate_verification_link(uid_encrypt, tok)

        # 인증 링크 메일로 보냄
        sendEmail(uid, "메일 인증", link)

        return redirect('Login')



class verifyEmailView(View):
    def get(self, request):
        key = Key()

        # 인증 링크에서 이메일 토큰 GET
        email_encrypt = request.GET.get('email')
        a1 = key.encrypt('123')
        email_decrypt = key.decrypt(email_encrypt)
        token = request.GET.get('token')

        # DB에서 비밀번호 구하기
        verify_temp_ids = Verify.objects.values_list('temp_id', flat=True)
        exists_check = False

        for verify_temp_id in verify_temp_ids:
            if email_decrypt == key.decrypt(verify_temp_id):
                verify = Verify.objects.get(temp_id=verify_temp_id)
                password = verify.temp_password
                break

        # 인증 링크에서 받은 이메일, 토큰 매치되는지 확인
        verification_success = verify_email_token(email_decrypt, token, key)

        # 매칭되면 유저 생성
        if verification_success:
            user = User(
                Uid=email_encrypt,
                password=password,
            )
            user.save()

        # 회원가입 성공했다는 html로 이동
        return render(request, 'verificationResult.html', {'verification_success': verification_success})


class LoginView(View):
    def post(self, request):
        uid = request.POST.get('uid')
        password = request.POST.get('password')
        uid_encrypt = ''
        key = Key()

        # Uid를 이용해 User 찾기 (없으면 None 반환)

        user_uids = list(User.objects.values_list('Uid', flat=True))
        find_check = False

        if user_uids:
            for user_uid in user_uids:
                if uid == key.decrypt(user_uid):
                    find_check = True
                    user = User.objects.get(Uid=user_uid)
                    uid_encrypt = user_uid
                    break

        if find_check == True and check_password(password, user.password):
            request.session['user_id'] = uid_encrypt
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
        key = Key()
        user_id = self.request.session.get('user_id')

        keywords = Keyword.objects.filter(Uid_id=user_id)
        # User.notice_order에서 Cid값을 가져옴
        notice_order = User.objects.get(Uid=user_id).notice_order
        cid_list = list(map(int, notice_order.split("/")))

        # Category와 그에 연결된 Notice를 가져옴
        categories = Category.objects.filter(Cid__in=cid_list)

        # 모든 Category를 가져옴
        allcategory = Category.objects.all()

        #
        context = {
            'keywords': keywords,
            'categories': categories,
            'allcategory' : allcategory
        }

        # Render the template with the data
        return render(request, 'mainPageTest.html', context)

    def post(self, request):

        #공지사항 순서 변경
        if 'reorder' in request.path:
            #새로운 공지사항 순서 저장 변수
            NewOrder = ''

            #input 값 가져와서 cid 값 찾아서 저장
            for i in range(1,7):
                input_i = f'input{i}'
                input_value = request.POST.get(input_i)

                Category_i = Category.objects.get(Cname=input_value)
                cid = Category_i.Cid
                if i==6:
                    NewOrder += str(cid)
                else:
                    NewOrder += str(cid) + '/'

            #새로 만들어진 CidList DB저장
            user_id = self.request.session.get('user_id')
            user = User.objects.get(Uid=user_id)
            user.notice_order=NewOrder
            user.save()

        return HttpResponseRedirect(reverse('main_page'))


class KeywordProcessView(View):

    def get(self, request, keyword):
        #정보 가져오기
        user_id = user_id = self.request.session.get('user_id')

        #삭제
        self.del_keyword(user_id,keyword)

        return redirect('main_page')

    def post(self, request, keyword):
        #정보 가져오기
        user_id = self.request.session.get('user_id')
        keyword = request.POST.get('now_keyword')
        edit_keyword = request.POST.get('edit_keyword')
        edit_catagory = request.POST.getlist('edit_category')
        similar_on = request.POST.get('similar_on')

        if not similar_on:
            similar_on = 'False'

        # 기존 정보 삭제
        self.del_keyword(user_id, keyword)

        # 추가
        self.add_keyword(user_id, edit_keyword, edit_catagory, similar_on)
        return redirect('main_page')

    # keyword 추가
    def add_keyword(self, uid, keyword, categories, similar):

        for i in categories:
            new_keyword = Keyword(
                key=keyword,
                Cid_id=i,
                Uid_id=uid,
                similar_on=similar

            )
            new_keyword.save()


    def del_keyword(self, uid, keyword):
        keywords = Keyword.objects.filter(Uid=uid, key=keyword)

        for keyword in keywords:
            keyword.delete()

class KeywordAddView(View):
    def get(self, request):
        #정보 가져오기
        user_id = self.request.session.get('user_id')
        keyword = request.GET.get('keyword_add')
        categories = request.GET.getlist('category_list')
        similar_on = request.GET.get('similar_on')

        if not similar_on:
            similar_on = 'False'

        #추가
        self.add_keyword(user_id, keyword, categories, similar_on)


        return redirect('main_page')

    def add_keyword(self, uid, keyword, categories, similar):

        for i in categories:
            new_keyword = Keyword(
                key=keyword,
                Cid_id=i,
                Uid_id=uid,
                similar_on=similar,
            )
            new_keyword.save()


class SearchView(View):

    def get(self, request):
        keyword = request.GET.get('keyword')
        keywords_similar = getSimKey(keyword, 5)

        # 제목 필드에서 검색어를 포함하는 공지사항 검색
        notices = Notice.objects.filter(title__icontains=keyword)

        context = {
            'notices': notices,
            'keyword': keyword,
            'keywords_similar': keywords_similar,
        }

        return render(request, 'searchPage.html', context)


