import * as React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
  
// 모든 공지사항을 받아와서 출력하는 형태
  const PinnedSubheaderList = (props) => {

    const [notices, setNotices] = useState(null);

    // User 테이블에서 notice_order에 따라서 백에서 순서에 맞게 반환
    // 그 공지사항들을 get하여 출력

    /* useEffect(() => {
      fetchNotices();
    }, []); */

    /* const fetchNotices = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:8000/mainPage/notices/');
        console.log(res.data);
        setNotices(res.data);
      } catch (error) {
        console.error(error);
      }
    }; */

    // props로 받은 Cid와 같은 공지들만 notify에 담도록 수정 예정 
    // -> 애초에 Cid와 일치하는 공지만 가져오는게 좋을듯
    
    // for문 길이 추후 설정 예정
    // primary, secondary 다시 수정 예정

    let notify = [];
    /* for (let i = 0; i < 10; i++) {
      let a = notices[i];
      notify.push(
        <li key={a.id}>
          <a href={a.link}>
            <ListItem sx={{ height: '23px' }}>
              <ListItemText
                primaryTypographyProps={{ fontSize: '14px' }}
                primary={a.title}
                secondary={a.time}
                sx={{ display: 'flex', justifyContent: 'space-between' }}
              />
            </ListItem>
          </a>
        </li>
      );
    } */
  
    return (
      <List
        sx={{
          width: '100%',
          height: '100%',
          bgcolor: 'background.paper',
          position: 'relative',
          overflow: 'auto',
          maxHeight: 250,
          '& ul': { padding: 0 },
          fontSize: '16px',
          borderRadius: '0%',
          boxShadow: '2px 2px 2px #D5D5D5',
        }}
        subheader={<li />}
      >
        {notify}
      </List>
    );
  };
  export default PinnedSubheaderList;