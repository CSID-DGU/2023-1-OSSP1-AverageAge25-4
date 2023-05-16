import React from 'react'
import searchIcon from './search-icon.png';
import './SearchBar.css';

function SearchBar() {

  return (
  
        <div className="input-wrapper">
          <img src={searchIcon} alt="search icon" 
            className="search-icon" />
          <input
            type="text"
            placeholder="검색어를 입력하세요"
          />
        </div>
  );
}

export default SearchBar;
