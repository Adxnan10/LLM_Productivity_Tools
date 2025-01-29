import axios from 'axios';

const fetcher = async (url, token, method = "post") => {
  if (method.toLowerCase() === "post") {
    const response = await axios.post(
      url,
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    );
    return response.data;
  }
  else if (method.toLowerCase() === "get") {
    const response = await axios.get(
      url,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    return response.data;
  }
};

export default fetcher;