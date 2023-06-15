import React, {useState} from 'react'
import styles from './index.module.scss';
import {Autocomplete, FormControl, FormLabel, TextField, Typography} from "@mui/material";


export default function PtsRequest() {
   const [selectedCity, setSelectedCity] = useState(null);
    const [citySelected, setCitySelected] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');


const cityList = [ { id: 1,
    name:'Minsk'},
    {id: 2,
        name:'Borisov'},
    {id: 3,
        name: 'Orsha'}]
  return (
      <div className={styles['form-wrapper']}>
          <FormControl>
              <FormLabel>Заявка на ПТС</FormLabel>
              <FormControl>
                  <TextField> Название Передачи</TextField>
                  <Autocomplete
                      id='city-names'
                      options={cityList}
                      autoHighlight
                      getOptionLabel={(option) => option.name}
                      onChange={(event, newValue) => {
                          setSelectedCity(newValue);
                          setCitySelected(!!newValue);
                      }}
                      inputValue={searchQuery}
                      onInputChange={(event, newInputValue) => {
                          setSearchQuery(newInputValue);
                      }}

                      filterOptions={(options, state) =>
                          options.filter(
                              (option) =>
                                  option.name
                                      .toLowerCase()
                                      .startsWith(state.inputValue.toLowerCase())
                          )
                      }
                      renderInput={(params) => (
                          <TextField
                              {...params}
                              label='City name'
                              placeholder='Please select City'
                              fullWidth
                              InputProps={{
                                  ...params.InputProps,
                              }}
                          />
                          <TextField
                      {...params}
                          label='City name'
                          placeholder='Please select City'
                          fullWidth
                          InputProps={{
                          ...params.InputProps,
                      }}
                          />
                      )}
                      renderOption={(props, option) => (
                          <li {...props}>
                              <Typography sx={{ paddingLeft: '5px' }}>
                                  {option.name}
                              </Typography>
                          </li>
                      )}
                  />


              </FormControl>
          </FormControl>


      </div>
  )
}
