import React, {useEffect} from 'react';
import {Link, Redirect} from 'react-router-dom';

function Logout(props) {
    useEffect(() => {
        props.logoutUser();
    });

    return (
        <div>
            <p>
                You are now logged out. Click <Link to="/login">here</Link> to log back in.
            </p>
            <Redirect to="/"/>
        </div>
    );
}

export default Logout;
