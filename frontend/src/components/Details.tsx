import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import { useParams } from "react-router-dom";

interface DetailsProps {
  id: number;
  product_id: string;
  name: string;
  description: string;
  brand: string;
}

const Details = (): JSX.Element => {
  //const theme = useTheme();

  const { id } = useParams();

  const [details, setDetails] = useState<DetailsProps>();

  const fetchDetails = () => {
    axios.get<DetailsProps>(`http://127.0.0.1:8000/api/products/${id}`, {
      headers: {
        'Accept': 'application/json'
      }
    })
      .then(response => {
        setDetails(response.data);
      })
      .catch(error => console.log(error));
  };

  useEffect(() => {
    fetchDetails();
  }, []);

  return (
    <Box sx={{ width: '100%' }}>
      <div className="product-details">
        <p>Product Id: {details?.product_id}</p>
        <p>Name: {details?.name}</p>
        <p>Description: {details?.description}</p>
        <p>Name: {details?.brand}</p>
      </div>
    </Box>
  );
};

export default Details;