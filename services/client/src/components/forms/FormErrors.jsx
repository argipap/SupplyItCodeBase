import React from 'react';

import './FormErrors.css';


const Error = ({touched, message}) => {

    if (message) {
        return <div className="form-message invalid">{message}</div>;
    }
    if (!touched) {
        return <div className="form-message invalid"/>;
    }
    return <div className="form-message valid"/>;
};

export default Error;