import { useFormik } from 'formik';
import {TextField, Select, MenuItem, FormControl, InputLabel, Button, Container, Box} from '@mui/material';

export default function Createrequest() {
  const formik = useFormik({
    initialValues: {
      city: '',
      place: '',
      event: '',
      txName: '',
      director: '',
    },
    onSubmit: values => {
      // handle form submission here
    },
  });

  return (
      <Container sx={{ paddingTop: '50px'}}>

    <form onSubmit={formik.handleSubmit}>
      <Box sx={{display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'space between'}}>
      <FormControl sx={{ m: 1, minWidth: 120 }} >
        <InputLabel>City</InputLabel>
        <Select  value={formik.values.city} onChange={formik.handleChange('city')}>
            <MenuItem value="Minsk">Minsk</MenuItem>
            <MenuItem value="Pinsk">Pinsk</MenuItem>
            <MenuItem value="Moscow">Moscow</MenuItem>
            <MenuItem value="Orsha">Orsha</MenuItem>
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
