import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { useTheme } from '@mui/material/styles';

import HeroButtons from './HeroButtons';
import Spacer from './Spacer';

const Hero = (): JSX.Element => {
  const theme = useTheme();

  return (
    <div id='home'>
      <Box
        sx={{
          py: 10,
          px: 2,
          backgroundColor: theme.palette.background.paper,
        }}
      >
      <Container
            maxWidth='md'
            sx={{
              alignItems: 'center',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            <Box marginBottom={2}>
              <Typography
                align='center'
                color={theme.palette.text.primary}
                variant='h3'
                sx={{ fontWeight: 700 }}
                gutterBottom
              >
                Open Banking Product Portal
              </Typography>
            </Box>
            <Box marginBottom={3}>
              <Typography
                variant='h6'
                component='p'
                color={theme.palette.text.secondary}
                sx={{ fontWeight: 400 }}
              >
                The open banking platform governed by ACCC regulates the consumer privacy over data sharing and benefits.
              </Typography>
            </Box>
            <HeroButtons />
          </Container>
      </Box>
      <Spacer sx={{ pt: 6 }} />
    </div> 
  );
};

export default Hero;