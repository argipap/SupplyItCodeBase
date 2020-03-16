import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter as Router} from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import ScrollToTop from './components/microcomps/ScrollToTop';


import App from "./App";


ReactDOM.render((
    // new
    <Router>
        <ScrollToTop />
        <App/>
    </Router>
), document.getElementById('root'));