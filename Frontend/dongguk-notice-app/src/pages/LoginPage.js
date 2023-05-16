import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [uid, setUid] = useState('');
  const [phone, setPhone] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://localhost:8000/login/', { uid, phone });
      if (response.status === 200) {
        navigate('/mainPage/');
      } else {
        // Handle login failure
      }
    } catch (error) {
      // Handle error
    }
  };

  return (
    <div>
      <input type="text" value={uid} onChange={(e) => setUid(e.target.value)} placeholder="UID" />
      <input type="text" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="Phone" />
      <button onClick={handleLogin}>로그인</button>
    </div>
  );
};

export default Login;