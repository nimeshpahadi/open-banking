import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { HelmetProvider, Helmet } from 'react-helmet-async';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

import getTheme from './theme/theme';
import Layout from './layout/Layout';
import Home from './pages/Home';
import ProductTabs from "./components/ProductTabs";
import About from "./components/About";
import Contact from "./components/Contact";
import Products from "./components/Products";

const App = (): JSX.Element => {  
  return (
    <HelmetProvider>
      <Helmet 
        titleTemplate="%s | Open Banking Product Portal"
        defaultTitle="Open Banking Product Portal"
      />
      <ThemeProvider theme={getTheme()}>
        <CssBaseline />
        <BrowserRouter>
          <Layout>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/products" element={<Products />} />
              <Route path="/productDetails/:id" element={<ProductTabs />} />
              <Route path="/about" element={<About />} />
              <Route path="/contact" element={<Contact />} />
            </Routes>
          </Layout>
        </BrowserRouter>
      </ThemeProvider>
    </HelmetProvider>
  );
};

export default App;