import React, { useState } from 'react';

function MenuBar(props) {
  const [newKeyword, setNewKeyword] = useState('');

  function handleKeywordAdd() {
    const newId = props.keywords.length + 1;
    const newTitle = newKeyword.trim();
    if (newTitle) {
      const newKeyword = { id: newId, title: newTitle };
      props.onKeywordAdd(newKeyword);
      setNewKeyword('');
    }
  }

  function handleKeywordDelete(keywordId) {
    props.onKeywordDelete(keywordId);
  }

  function handleKeywordEdit(keywordId, newTitle) {
    props.onKeywordEdit(keywordId, newTitle);
  }

  function handleChange(event) {
    setNewKeyword(event.target.value);
  }

  const keywordItems = props.keywords.map(keyword => (
    <li key={keyword.id}>
      {keyword.title}
      <button onClick={() => handleKeywordDelete(keyword.id)}>삭제</button>
      <button onClick={() => handleKeywordEdit(keyword.id, prompt("새로운 키워드를 입력해주세요."))}>수정</button>
    </li>
  ));

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <h5 style={{ color: '#37484B', fontWeight: 'bold', marginBottom: '1em', fontSize: '1.2rem' }}>
          &nbsp;&nbsp; &nbsp;&nbsp; KEYWORDS
        </h5>
        <input type="text" value={newKeyword} onChange={handleChange} />
        <button onClick={handleKeywordAdd}>추가</button>
      </div>
      <ul style={{ fontSize: '0.7rem' }}>{keywordItems}</ul>
    </div>
  );
}

export default MenuBar;
