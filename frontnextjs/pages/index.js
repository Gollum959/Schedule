import { useEffect, useState } from 'react'
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
import { startOfWeek, endOfWeek, addWeeks, subWeeks, isWithinInterval } from 'date-fns';
import { useSelector} from 'react-redux'

function Home() {
const [data, setData] = useState(null);
const [open, setOpen] = useState(false);
const [openPtsConfig, setOpenPtsConfig] = useState(false);
const [openPtsRequest, setOpenPtsRequest] = useState(false);
const [selectedPlace, setSelectedPlace] = useState(false)
const [selectedPtsConfig, setSelectedPtsConfig] = useState(false)
const [selectedPtsRequest, setSelectedPtsRequest] = useState(false);
const [filter, setFilter] = useState('thisWeek');
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
const handleFilter = (filter) => {
  setFilter(filter);
};

const getWeekInterval = (weekOffset) => {
  const start = startOfWeek(addWeeks(new Date(), weekOffset));
  const end = endOfWeek(addWeeks(new Date(), weekOffset));
  return { start, end };
};

const filteredData = data?.filter(item => {
  const itemDate = new Date(item.broadcast_start_date);
  let weekInterval;

  switch (filter) {
    case 'lastWeek':
      weekInterval = getWeekInterval(-1);
      break;
    case 'nextWeek':
      weekInterval = getWeekInterval(1);
      break;
    default:
      weekInterval = getWeekInterval(0);
  }

  return isWithinInterval(itemDate, weekInterval);
});
const counter = useSelector(state => state.counter)
    return (
      <div>
        <h1>COUNTER</h1>
        <h2>{counter}</h2>

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
            {data ? (
            <TableBody>
              {filteredData.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>{item.id}</TableCell>
                  <TableCell>{item.broadcast_start_date}</TableCell>
                  <TableCell>
                    {item.broadcast_start_time}-{item.broadcast_end_time}
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
        ) : (
          <p>Loading data...</p>
        )}
         </Table>
         <div>
            <button onClick={() => handleFilter('thisWeek')}>This Week</button>
            <button onClick={() => handleFilter('lastWeek')}>Last Week</button>
            <button onClick={() => handleFilter('nextWeek')}>Next Week</button>
          </div>
      </div>
    );
  }

export default  Home





