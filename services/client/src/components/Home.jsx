import React, {Component} from 'react';
import {Link} from 'react-router-dom';

class Home extends Component {
    constructor(props) {
        super(props);
    };

    render() {
        return (
            <div className="get-started">
                <div className="container has-text-left">
                    <div className="columns">
                        <div className="column is-half">
                            <h1 className="title is-2">ALL YOUR SUPPLIERS<br/>IN ONE PLACE</h1>
                            <hr/>
                            <br/>
                            <p>Supplyit is a one-stop-shop for all your wholesale foodservice suppliers. Instant sign
                                up, one order, one payment, zero headaches.</p>
                            <br/>
                            <Link to="/getStarted" className="button is-danger">GET STARTED</Link>
                        </div>
                    </div>
                </div>
            </div>
        );
    };
}

export default Home;