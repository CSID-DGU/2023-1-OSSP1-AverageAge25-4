import React from 'react';

function MenuBar (props) {
  const lis = []

  for(let i=0;i<props.keywords.length;i++){
    let t = props.keywords[i];
    lis.push(<li key={t.id}>
      {t.title}</li>)
  }
  
  return (
    <div>
      <h3>&nbsp; &nbsp; &nbsp; KEYWORD</h3> 
      <ul>
        {lis}
     </ul>
     </div>
  );
}

export default MenuBar;
