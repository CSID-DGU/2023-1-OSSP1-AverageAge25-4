import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import SearchBar from './SearchBar';
import MenuBar from './components/MenuBar';
import PinnedSubheaderList from './lists';
import './App.css';

const Card = () => {
  const spacing = '1em';

  const card = document.createElement('div');
  card.classList.add('card');

  const cardBody = document.createElement('div');
  cardBody.classList.add('card-body');
  cardBody.style.marginRight = spacing;

  const cardTitle = document.createElement('h5');
  cardTitle.classList.add('card-title');
  cardTitle.textContent = 'Card title';

  const cardText = document.createElement('p');
  cardText.classList.add('card-text');
  cardText.textContent = "Some quick example text to build on the card title and make up the bulk of the card's content.";

  const cardButton = document.createElement('a');
  cardButton.classList.add('btn', 'btn-primary');
  cardButton.href = '#';
  cardButton.textContent = 'Go somewhere';

  cardBody.appendChild(cardTitle);
  cardBody.appendChild(cardText);
  cardBody.appendChild(cardButton);

  card.appendChild(cardBody);

  return card;
}

function App() {
  const keywords = [
    { id: 1, title: "국가장학금 - 학사, 장학" },
    { id: 2, title: "개별연구 - 학사" },
    { id: 3, title: "근로장학 - 장학" },
    { id: 4, title: "계절학기 " }
  ];
  const notifys1=[
    { id: 0, title: "강서구 꿈드림 검정고시 대비반 학습멘 " 
    ,link: 'https://cse.dongguk.edu/article/notice1/detail/176573?article_seq=&prt_seq=&category_cd=&searchCondition=TA.SUBJECT&searchKeyword='
    , date: "5.9"},
    { id: 1, title: "[참사람사회공헌센터] 2023 전공연계 동 " ,link: 'https://cse.dongguk.edu/article/notice1/detail/176573?article_seq=&prt_seq=&category_cd=&searchCondition=TA.SUBJECT&searchKeyword='
    ,date: "5.9"},
    { id: 2, title: "동국대학교 슬로건 공모전 결과 안내" ,link: 'https://cse.dongguk.edu/article/notice1/detail/176573?article_seq=&prt_seq=&category_cd=&searchCondition=TA.SUBJECT&searchKeyword='
    ,date: "5.4"},
    { id: 3, title: "국제학생증 ISIC 발급비 지원행사 안내" ,link: '/' ,date: "5.4"},
    { id: 4, title: "서울시설공단 시민경영참여단 모집공고" ,link: '/' ,date: "5.4"},
    { id: 5, title: "유네스코 국제무예센터 2023 제 6기 국" ,link: '/' ,date: "5.3"},
    { id: 6, title: "[5대 핵심역량 함양 프로그램] 나를 브" ,link: '/',date: "5.3"},
    { id: 7, title: "(예비군연대) 제 414차 민방위의 날 민" ,link: '/',date: "5.3"},
    { id: 8, title: "LINC3.0 만족도조사 참여하고 모바일 " ,link: '/',date: "5.2"},
    { id: 9, title: "[LINC3.0] 산학공동 기술개발과제 모집" ,link: '/',date: "5.2"}
  ];

  const notifys2=[
    { id: 0, title: "2023년 부처님오신날 대체공휴일 지정" ,link: 'https://cse.dongguk.edu/article/notice1/detail/176573?article_seq=&prt_seq=&category_cd=&searchCondition=TA.SUBJECT&searchKeyword='
    ,date: "5.9"},
    { id: 1, title: "제 10회 EAS 영어 발표(Presentation) " ,link: 'https://cse.dongguk.edu/article/notice1/detail/176573?article_seq=&prt_seq=&category_cd=&searchCondition=TA.SUBJECT&searchKeyword='
    ,date: "5.4"},
    { id: 2, title: "[신입생 모집] 2023학년도 후기 부디스" ,link: 'https://cse.dongguk.edu/article/notice1/detail/176573?article_seq=&prt_seq=&category_cd=&searchCondition=TA.SUBJECT&searchKeyword='
    ,date: "5.3"},
    { id: 3, title: "2023 - 여름학기 현장실습 참가학생 모" ,link: '/' ,date: "5.3"},
    { id: 4, title: "2023학년도 여름계절학기 서울시립대" ,link: '/' ,date: "5.3"},
    { id: 5, title: "2023학년도 여름계절학기 건국대학교 " ,link: '/' ,date: "5.3"},
    { id: 6, title: "5월 3일 모의토익 고사장 및 성적 확인" ,link: '/' ,date: "5.2"},
    { id: 7, title: "2023학년도 여름계절학기 상명대학교 " ,link: '/',date: "5.1"},
    { id: 8, title: "2023학년도 여름계절학기 숙명여자대학" ,link: '/',date: "4.28"},

  
  ];
  
  const notifys3=[
    { id: 0, title: "2023-1학기 동국리더장학 신청 안내" ,link: 'https://cse.dongguk.edu/article/notice1/detail/176573?article_seq=&prt_seq=&category_cd=&searchCondition=TA.SUBJECT&searchKeyword='
    ,date: "5.4"},
    { id: 1, title: "2023-1학기 동국인재육성장학 Dream" ,link: 'https://cse.dongguk.edu/article/notice1/detail/176573?article_seq=&prt_seq=&category_cd=&searchCondition=TA.SUBJECT&searchKeyword='
    ,date: "5.1"},
    { id: 2, title: "2023년도 보건장학회 연구지원 장학생" ,link: 'https://cse.dongguk.edu/article/notice1/detail/176573?article_seq=&prt_seq=&category_cd=&searchCondition=TA.SUBJECT&searchKeyword='
    ,date: "4.28"},
    { id: 3, title: "2023 강원랜드 멘토링 장학생 모집안 " ,link: '/',date: "4.27"},
    { id: 4, title: "<2023년 제 2기 동국건학장학생 최종" ,link: '/',date: "4.27"},
    { id: 5, title: "2023년도 특별상환유예제도 안내" ,link: '/',date: "4.27"},
    { id: 6, title: "2023 전기 파안장학문화재단 총장 추" ,link: '/',date: "4.27"},
    { id: 7, title: "제29기 미래에셋 해외교환 장학생 선" ,link: '/',date: "4.25"},
    { id: 8, title: "2023학년도 전기 일반대학원 신(편)" ,link: '/',date: "4.25"},

  ];
  
  const notifys4=[
    { id: 0, title: "2023학년도 후기 일반대학원 신(편)입" ,link: 'https://cse.dongguk.edu/article/notice1/detail/176573?article_seq=&prt_seq=&category_cd=&searchCondition=TA.SUBJECT&searchKeyword='
    ,date: "4.26"},
    { id: 1, title: "2023학년도 1학기 시간제 등록생 모집" ,link: 'https://cse.dongguk.edu/article/notice1/detail/176573?article_seq=&prt_seq=&category_cd=&searchCondition=TA.SUBJECT&searchKeyword='
    ,date: "1.30"},
    { id: 2, title: "2023학년도 전기 일반대학원 수시전형" ,link: 'https://cse.dongguk.edu/article/notice1/detail/176573?article_seq=&prt_seq=&category_cd=&searchCondition=TA.SUBJECT&searchKeyword='
    ,date: "1.16"},
    { id: 3, title: "2023학년도 전기 일반대학원 신(편)입" ,link: '/',date: "12.5"},
    { id: 4, title: "2023학년도 전기 일반대학원 신(편)입" ,link: '/',date: "12.1"},
    { id: 5, title: "2023학년도 전기 일반대학원 신(편)" ,link: '/',date: "11.18"},
    { id: 6, title: "2023학년도 전기 일반대학원 일반전형 " ,link: '/',date: "11.1"},
    { id: 7, title: "2023학년도 일반대학원 ‘스마트오션" ,link: '/',date: "10.14"},
    { id: 8, title: "2023학년도 전기 일반대학원 신(편)" ,link: '/',date: "10.11"},
    { id: 9, title: "2023학년도 전기 일반대학원 신(편)" ,link: '/',date: "9.15"}
  
  ];
  


return (

  <div className="container" >
    <div className="up"> 
      <SearchBar />
    </div>


    <div className="down">
        <div className="menubar">
          <MenuBar keywords={keywords}></MenuBar>
        </div>

        <div className="component-wrapper">

          <div className="row1">
            <div className="component-container">
              <h5>&nbsp; 일반 </h5> 
              <PinnedSubheaderList Cid={1} />
            </div>

            <div className="component-container">
              <h5>&nbsp; 학사 </h5>
              <PinnedSubheaderList Cid={2}/>
            </div>
          </div>


          <div className="row2">
            <div className="component-container">
              <h5>&nbsp; 장학 </h5>
              <PinnedSubheaderList Cid={3}/>
            </div>

            <div className="component-container">
              <h5>&nbsp; 입시 </h5>
              <PinnedSubheaderList Cid={4}/>
            </div>
          </div>

        </div>

    </div>
  </div>
    );
  }
  

export default App;