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
import {
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody, Modal, Box, Button
} from "@mui/material";
import PlaceDetails from './PlaceDetails';
import PtsConfigDetails from './PtsConfigDetails'

import PtsRequest from "@/components/PtsRequest";

function Home() {
  const [data, setData] = useState(null);
  const [open, setOpen] = useState(false);
  const [openPtsConfig, setOpenPtsConfig] = useState(false);
const [openPtsRequest, setOpenPtsRequest] = useState(false);

const [selectedPlace, setSelectedPlace] = useState(false)
const [selectedPtsConfig, setSelectedPtsConfig] = useState(false)
const [selectedPtsRequest, setSelectedPtsRequest] = useState(false);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const handlePtsConfigOpen = () => setOpenPtsConfig(true);
  const handlePtsConfigClose = () => setOpenPtsConfig(false);
  const handlePtsRequestOpen = () => setOpenPtsRequest(true);
  const handlePtsRequestClose = () => setOpenPtsRequest(false);

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
        <Modal open={openPtsRequest} onClose={handlePtsRequestClose}>
          <Box
            sx={{
              position: "absolute",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              bgcolor: "background.paper",
              boxShadow: 24,
              p: 4,
            }}
          >
            <PtsConfigDetails ptsreqiestId={selectedPtsRequest} />
            <Button variant="contained" onClick={handlePtsRequestClose}>
              Close
            </Button>
          </Box>
        </Modal>
        <Modal open={openPtsConfig} onClose={handlePtsConfigClose}>
          <Box
            sx={{
              position: "absolute",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              bgcolor: "background.paper",
              boxShadow: 24,
              p: 4,
            }}
          >
            <PtsConfigDetails ptsconfigId={selectedPtsConfig} />
            <Button variant="contained" onClick={handlePtsConfigClose}>
              Close
            </Button>
          </Box>
        </Modal>
        <Modal open={open} onClose={handlePtsConfigClose}>
          <Box
            sx={{
              position: "absolute",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              bgcolor: "background.paper",
              boxShadow: 24,
              p: 4,
            }}
          >
            <PlaceDetails placeId={selectedPlace} />
            <Button variant="contained" onClick={handleClose}>
              Close
            </Button>
          </Box>
        </Modal>
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
                  <TableCell>
                    {item.start_time}-{item.end_time}
                  </TableCell>
                  <TableCell>
                    <Button
                      variant="contained"
                      onClick={() => {
                        setSelectedPtsRequest(item.id);
                        handlePtsRequestOpen();
                      }}
                    >
                      {item.name}
                    </Button>
                    
                  </TableCell>
                  <TableCell>{item.status}</TableCell>
                  <TableCell>{item.author}</TableCell>
                  <TableCell>{item.pts_name?.name}</TableCell>
                  <TableCell>
                    <Button
                      variant="contained"
                      onClick={() => {
                        setSelectedPtsConfig(item.pts_cfg?.id);
                        handlePtsConfigOpen();
                      }}
                    >
                      {item.pts_cfg?.name}
                    </Button>
                  </TableCell>
                  <TableCell>
                    <Button
                      variant="contained"
                      onClick={() => {
                        setSelectedPlace(item.place.id);
                        handleOpen();
                      }}
                    >
                      {item.place?.city_name.name} -{item.place?.name}
                    </Button>
                  </TableCell>
                  {/* Add more table cells for additional fields */}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        ) : (
          <p>Loading data...</p>
        )}
      </div>
    );
  }

export default  Home





