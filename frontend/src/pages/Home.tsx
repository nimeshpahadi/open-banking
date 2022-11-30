import React from 'react';

import Hero from '../components/Hero';
import Products from '../components/Products';
import About from '../components/About';
import Contact from '../components/Contact';

const Home = (): JSX.Element => {
  return (
    <div id="home">
      <Hero />
      <Products />
      <About />
      <Contact />
    </div>
  );
};

export default Home;