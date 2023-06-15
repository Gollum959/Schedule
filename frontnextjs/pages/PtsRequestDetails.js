import { useState, useEffect } from "react";
import axios from "axios";

function PtsRequestDetails({ ptsrequestId }) {
  const [ptsRequestData, setPtsRequestData] = useState(null);

  useEffect(() => {
    fetchPtsRequestData();
  }, []);

  async function fetchPtsRequestData() {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/api/v1/pts_requests/${ptsrequestId}/`
      );
      const data = response.data;
      setPtsRequestData(data);
    } catch (error) {
      console.error(error);
    }
  }
  console.log("PTSRequest", ptsRequestData);
  return (
    <div>
      {ptsRequestData ? (
        <div>
          <h2>{ptsRequestData.name}</h2>
          {/* <p>
            Автор: {ptsRequestData.author.first_name}{" "}
            {ptsConfigData.author.last_name}
          </p> */}
        </div>
      ) : (
        <p>Loading PTS request data...</p>
      )}
    </div>
  );
}

export default PtsRequestDetails;
