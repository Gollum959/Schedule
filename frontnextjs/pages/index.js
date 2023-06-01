import Head from 'next/head'
import Image from 'next/image'
import { Inter } from 'next/font/google'
import { Router } from 'next/router'
import styles from '../styles/Home.module.css'
import { useEffect, useState } from 'react'
import dateFormat from 'dateformat'
import { i18n } from "dateformat";
import Link from 'next/link'
import { useRouter } from 'next/router'
import axios from 'axios';
import { Table, TableHead, TableRow, TableCell, TableBody } from '@mui/material';
import PlaceDetails from './PlaceDetails';

function Home() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  
  async function fetchData() {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/v1/pts_requests/');
      const data = response.data;
      setData(data);
    } catch (error) {
      console.error(error);
    }
  }
  
console.log('DATA', data)
 
    return (
    <div>
      {data ? (
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Дата трансляции</TableCell>
              <TableCell>Время трансляции</TableCell>
              <TableCell>Название передачи</TableCell>
              <TableCell>Статус</TableCell>
              <TableCell>Автор</TableCell>
              <TableCell>Имя ПТС</TableCell>
              <TableCell>Конфигурация ПТС</TableCell>
              <TableCell>Место работы</TableCell>
              {/* Add more table headers for additional fields */}
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((item) => (
              <TableRow key={item.id}>
                <TableCell>{item.id}</TableCell>
                <TableCell>{item.start_date}</TableCell>
                <TableCell>{item.start_time}-{item.end_time}</TableCell>
                <TableCell>{item.name}</TableCell>
                <TableCell>{item.status}</TableCell>
                <TableCell>{item.author}</TableCell>
                <TableCell>{item.pts_name?.name}</TableCell>
                <TableCell>{item.pts_cfg?.name}</TableCell>
                <TableCell>
                <button onClick={() => console.log('Clicked on city name')}>
                  {item.place?.city_name.name}
                </button>
                </TableCell>
                {/* Add more table cells for additional fields */}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      ) : (
        <p>Loading data...</p>
      )}
       {data && (
        <div>
            <PlaceDetails placeId={9} />
        </div>
      )}
    </div>
    );
  }

export default  Home





