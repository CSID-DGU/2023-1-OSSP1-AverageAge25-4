from django.test import TestCase

# Create your tests here.
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
    [5, 'http://dguadpr.kr/bbs/board.php?bo_table=table31&page=', '광고홍보학과'],

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
    [4, 'http://mme.dongguk.edu/k3/sub5/sub1.php?page=', '멀티미디어공학과'],

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
    [1, 'https://aart.dongguk.edu/article/notice/', '미술학부'],  # 공지사항 없음
    [1, 'https://theatre.dongguk.edu/article/notice/', '연극학부'],
    [1, 'https://kmart.dongguk.edu/article/notice/', '한국음악과'],
    [5, 'https://movie.dongguk.edu/movie1_3_1/p', '영화영상학과'],  # p1, p2...

    # 약학대학
    [1, 'https://pharm.dongguk.edu/article/notice/', '약학과'],

    # 다르마칼리지
    [1, 'https://dharma.dongguk.edu/article/notice/', '다르마칼리지'],

    # 미래융합대학
    [3, 'https://security.dongguk.edu/bbs/data/list.do?menu_idx=30&pageIndex=', '융합보안학과'],
    [3, 'https://swc.dongguk.edu/bbs/data/list.do?menu_idx=46&pageIndex=', '사회복지상담학과'],
    [3, 'https://gt.dongguk.edu/bbs/data/list.do?menu_idx=58&pageIndex=', ' 글로벌무역학과'],

    # 시설공지
    [6, 'https://lib.dongguk.edu/bbs/list/1?pn=', '중앙도서관'],
    [1, 'https://dorm.dongguk.edu/article/notice/', '기숙사'],
    [7, 'https://dgucoop.dongguk.edu/board/board.php?w=1&page=', '생협'],

    # 기타공지

]

for item in category_list:
    if item[0] == 0 or item[0] == 1 or item[0] == 2:
        item[1] += 'list?pageIndex='
    temp = item[0]
    item[0] = item[2]
    item[2] = temp
    print(item, end=",\n")