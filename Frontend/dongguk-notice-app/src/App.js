import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import './App.css';
import Login from './pages/LoginPage';
import MainPage from './pages/MainPage';
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

return (

  <div className="container">
    <BrowserRouter>
      <Routes>
        <Route path={""} element={<Login/>}></Route>
        <Route path={"/mainPage/"} element={<MainPage/>}></Route>
      </Routes>
    </BrowserRouter>
  </div>
)}

export default App