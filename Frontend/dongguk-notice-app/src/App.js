import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import SearchBar from './SearchBar';
import MenuBar from './components/MenuBar';
import PinnedSubheaderList from './lists';
import './App.css';
import LoginPage from './LoginPage';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

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
  
return (

  <div className="container" >
    <BrowserRouter>
      <Routes>
        <Route path={""} element={<LoginPage/>}></Route>
        <Route path={"/mainPage/"} element={<SearchBar/>}></Route>
      </Routes>
    </BrowserRouter>
  </div>

  
    /* <div className="up"> 
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
    </div> */
    

    
  
  
    );
  }
  

export default App;