import { useFormik } from 'formik';
import {TextField, Select, MenuItem, FormControl, InputLabel, Button, Container, Box} from '@mui/material';
import axios from "axios";
import {useEffect, useState} from "react";

export default function Createrequest() {
  const [cityData, setCityData] = useState(null);
  const formik = useFormik({
    initialValues: {
      city: 'Minsk',
      place: '',
      event: '',
      txName: '',
      director: '',
    },
    onSubmit: values => {
      // handle form submission here
    },
  });
  useEffect(() => {
    fetchCityData();
  }, []);
  async function fetchCityData() {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/v1/city/');
      const data = response.data;
      setCityData(data);
    } catch (error) {
      console.error(error);
    }
  }
  console.log('CityData', cityData)


  return (
      <Container sx={{ paddingTop: '50px'}}>

    <form onSubmit={formik.handleSubmit}>
      <Box sx={{display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'space between'}}>
      <FormControl sx={{ m: 1, minWidth: 120 }} >
        <InputLabel>City</InputLabel>
        <Select  value={formik.values.city} onChange={formik.handleChange('city')}>
          {cityData?.map((city) => (
              <MenuItem key={city.id} value={city.name}>
                {city.name}
              </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl sx={{ m: 1, minWidth: 120 }}>
        <InputLabel>Place</InputLabel>
        <Select value={formik.values.place} onChange={formik.handleChange('place')}>
          {/* Insert options here */}
        </Select>
      </FormControl >
      <FormControl sx={{ m: 1, minWidth: 120 }}>
        <InputLabel>Event</InputLabel>
        <Select value={formik.values.event} onChange={formik.handleChange('event')}>
          {/* Insert options here */}
        </Select>
      </FormControl >
      <TextField sx={{ m: 1, minWidth: 200 }} label="TxName" value={formik.values.txName} onChange={formik.handleChange('txName')} />
      <FormControl sx={{ m: 1, minWidth: 120 }}>
        <InputLabel>Director</InputLabel>
        <Select value={formik.values.director} onChange={formik.handleChange('director')}>
          {/* Insert options here */}
        </Select>
      </FormControl>
        <Button type="submit">Submit</Button>
      </Box>
    </form>

      </Container>
  )
}
