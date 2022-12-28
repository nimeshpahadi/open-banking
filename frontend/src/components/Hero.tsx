import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { useTheme } from '@mui/material/styles';

import HeroButtons from './HeroButtons';
import Spacer from './Spacer';
import banner from '../assets/images/openbanking.jpg';

function Hero() {

  return (
    <React.Fragment>
      <div>
          <img src={banner} className="d-block w-300" alt='banner'/>
      </div>
    </React.Fragment>
  );
}

export default Hero;