import React from 'react';
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';

export default function Paginations({ onChange = () => { }, currentPage = 1, total = 0 }) {
  const count = Math.ceil(total / 10);

  const handleChange = (event, value) => {
    onChange(event, value);
  };

  return (
    <div className='w-full flex flex-col items-center justify-center'>
      {
        count >= 1 ? <Stack spacing={2}>
          <Pagination onChange={handleChange} color="primary" count={count} page={currentPage} showFirstButton showLastButton />
        </Stack> : <></>
      }
    </div>
  );
}
