import { useState, useEffect } from "react";
import axios from "axios";

function PtsConfigDetails({ ptsconfigId }) {
  const [ptsConfigData, setPtsConfigData] = useState(null);

  useEffect(() => {
    fetchPtsConfigData();
  }, []);

  async function fetchPtsConfigData() {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/api/v1/pts_config/${ptsconfigId}/`
      );
      const data = response.data;
      setPtsConfigData(data);
    } catch (error) {
      console.error(error);
    }
  }
console.log('PTSCONFIG', ptsConfigData)
  return (
    <div>
      {ptsConfigData ? (
        <div>
          <h2>{ptsConfigData.name}</h2>
          <p>
            Автор: {ptsConfigData.author.first_name} {ptsConfigData.author.last_name}
          </p>
        </div>
      ) : (
        <p>Loading PTS config data...</p>
      )}
    </div>
  );
}

export default PtsConfigDetails;
