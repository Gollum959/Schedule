import { useFormik } from 'formik';
import {TextField, Select, MenuItem, FormControl, InputLabel, Button, Container, Box} from '@mui/material';
import axios from "axios";
import React, {useEffect, useState} from "react";
import { useDispatch, useSelector } from 'react-redux';
import { fetchCitiesRequest } from '../store/actions/cities';

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
  const dispatch = useDispatch();
  const cities = useSelector((state) => state.cities); // As
  useEffect(() => {
    dispatch(fetchCitiesRequest());
  }, [dispatch]); // Run the effect when dispatch changes


  console.log('CITIES ARRAY', cities);
  return (
      <Container sx={{ paddingTop: '50px'}}>

    <form onSubmit={formik.handleSubmit}>
      <Box sx={{display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'space between'}}>
      <FormControl sx={{ m: 1, minWidth: 120 }} >
        <InputLabel>City</InputLabel>
        <Select  value={formik.values.city} onChange={formik.handleChange('city')}>

          {cities.cities.map((city) => (
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
