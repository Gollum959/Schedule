import { useState, useEffect } from 'react';
import axios from 'axios';

function PlaceDetails({ placeId }) {
  const [placeData, setPlaceData] = useState(null);

  useEffect(() => {
    fetchPlaceData();
  }, []);

  async function fetchPlaceData() {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/v1/place/${placeId}/`);
      const data = response.data;
      setPlaceData(data);
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div>
      {placeData ? (
        <div>
          <h2>{placeData.name}</h2>
          <p>Address: {placeData.address}</p>
          <p>Contact Name: {placeData.contact_name}</p>
          <p>Phone: {placeData.phone}</p>
          {/* Display more information about the place */}
        </div>
      ) : (
        <p>Loading place data...</p>
      )}
    </div>
  );
}

export default PlaceDetails;
