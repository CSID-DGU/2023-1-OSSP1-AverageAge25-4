import React, { useState } from 'react';
import axios from 'axios';

function LoginPage() {
    const [userID, setUserID] = useState("");
    const [phoneNum, setPhoneNum] = useState("");

    const onIDHandler = (event) => {
        setUserID(event.currentTarget.value);
    }

    const onPhoneNumHandler = (event) => {
        setPhoneNum(event.currentTarget.value);
    }

    const sendPost = () => {
        axios.post('http://127.0.0.1:8000/login/', { uid : userID, phone : phoneNum })
        .then((response) => {
            console.log('Post sent successfully:', response.data);
        })
        .catch((error) => {
        console.error('Error sending post:', error);
        });
    }

    return (
        <div style={{ 
            display: 'flex', justifyContent: 'center', alignItems: 'center', 
            width: '100%', height: '15vh'
            }}>
            <form style={{ display: 'flex', flexDirection: 'column'}}
                
            >
                <label>UserID</label>
                <input type='text' value={userID} onChange={onIDHandler}/>
                <label>PhoneNum</label>
                <input type='text' value={phoneNum} onChange={onPhoneNumHandler}/>
                <br />
                <button formAction=''>
                    Login
                </button>
                <button onClick={sendPost}>
                    Send Post
                </button>
            </form>
        </div>
    )
}

export default LoginPage;