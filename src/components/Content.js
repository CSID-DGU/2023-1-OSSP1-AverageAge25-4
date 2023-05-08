import React from 'react';
import Component1 from './Component1';
import Component2 from './Component2';
import Component3 from './Component3';
import Component4 from './Component4';

function Content() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'flex', flex: 1 }}>
        <Component1 />
        <Component2 />
      </div>
      <div style={{ display: 'flex', flex: 1 }}>
        <Component3 />
        <Component4 />
      </div>
    </div>
  );
}

export default Content;