import React from 'react';
import SearchBar from './SearchBar';
import MenuBar from './components/MenuBar';
//import Content from '.components/Content';

import Component2 from './components/Component2';
import Component3 from './components/Component3';
import Component4 from './components/Component4';
import PinnedSubheaderList from './lists';


import './App.css';

function App() {
  const keywords = [
    { id: 1, title: "국가장학금" },
    { id: 2, title: "개별연구" },
    { id: 3, title: "근로장학" },
    { id: 4, title: "계절학기" }
  ];
  const notifys=[
    { id: 0, title: "국가장학금 신청기간" ,link: 'https://cse.dongguk.edu/article/notice1/detail/176573?article_seq=&prt_seq=&category_cd=&searchCondition=TA.SUBJECT&searchKeyword='},
    { id: 1, title: "2023 -1 개별연구..." ,link: 'https://cse.dongguk.edu/article/notice1/detail/176573?article_seq=&prt_seq=&category_cd=&searchCondition=TA.SUBJECT&searchKeyword='},
    { id: 2, title: "근로장학 신청..." ,link: 'https://cse.dongguk.edu/article/notice1/detail/176573?article_seq=&prt_seq=&category_cd=&searchCondition=TA.SUBJECT&searchKeyword='},
    { id: 3, title: "공지1" ,link: '/'},
    { id: 4, title: "공지2" ,link: '/'},
    { id: 5, title: "공지3" ,link: '/'},
    { id: 6, title: "공지4" ,link: '/'},
    { id: 7, title: "공지5" ,link: '/'}
  
  ];

 return (

      <div className="container">
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
          <h3>&nbsp; 키워드 </h3> 
           <PinnedSubheaderList notifys={notifys} />
          </div>
          <div className="component-container">
            <h3>&nbsp; 장학 </h3>
            <PinnedSubheaderList notifys={notifys}/>
          </div>
          </div>
          <div className="row2">
          <div className="component-container">
            <h3>&nbsp; 학과 </h3>
            <PinnedSubheaderList notifys={notifys}/>
          </div>
          <div className="component-container">
            <h3>&nbsp; 공지 </h3>
            <PinnedSubheaderList notifys={notifys}/>
          </div>
          </div>
        </div>
      </div>
      </div>
    );
  }
  
 
  

export default App;