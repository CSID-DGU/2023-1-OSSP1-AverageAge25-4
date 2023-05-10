import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
  
  const PinnedSubheaderList = (props) => {
    let notify = [];
    for (let i = 0; i < props.notifys.length; i++) {
      let a = props.notifys[i];
      notify.push(
        <li key={a.id}>
          <a href={a.link}>
            <ListItem sx={{ height: '23px' }}>
              <ListItemText
                primaryTypographyProps={{ fontSize: '14px' }}
                primary={a.title}
                secondary={a.date}
                sx={{ display: 'flex', justifyContent: 'space-between' }}
          />
        </ListItem>
          </a>
        </li>
      );
    }
  
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
          borderRadius: '2%',
          boxShadow: '2px 2px 2px #b4b4b4',
        }}
        subheader={<li />}
      >
        {notify}
      </List>
    );
  };
  export default PinnedSubheaderList;