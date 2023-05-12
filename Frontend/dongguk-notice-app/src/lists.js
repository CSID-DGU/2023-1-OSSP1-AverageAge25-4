import * as React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
  
// props로 어떤 카테고리인지 받음
  const PinnedSubheaderList = (props) => {

    const [notices, setNotices] = useState(null);

    // 'Notices/'+ props.Cid 등으로 해당 카테고리의 공지만 가져올 수 있도록 구현 예정
    // Cid별로 Notices들을 json으로 주는 url로 부탁드립니다
    // http://127.0.0.1:8000/notices/ => 모든 공지들
    // http://127.0.0.1:8000/notices/1 => Cid 1인 일반공지 notices들
    // http://127.0.0.1:8000/notices/2 => CId 2인 학사공지 notices들
    
    // 추후 user의 과에 해당하는 Cid를 받아서 해당 학과, 단과대 공지도 출력할 예정

    useEffect(() => {
      fetchNotices();
    }, []);

    const fetchNotices = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:8000/mainPage/');
        console.log(res.data);
        setNotices(res.data);
      } catch (error) {
        console.error(error);
      }
    };

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