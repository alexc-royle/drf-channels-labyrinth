import React from 'react';
import Header from '../containers/Header';
import Content from '../containers/Content';
import Footer from './Footer';

const PageWrapper = () => <div className="pageWrapper">
  <Header />
  <Content />
  <Footer />
</div>

export default PageWrapper;
