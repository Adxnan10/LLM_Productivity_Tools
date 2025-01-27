import axios from 'axios';

const fetcher = async (url, token) => {
  const response = await axios.post(
    url,
    {},
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return response.data;
};

export default fetcher;