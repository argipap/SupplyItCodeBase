import React, {Component} from 'react';
import {Link} from 'react-router-dom';

class HowItWorks extends Component {
    constructor(props) {
        super(props);
    };

    render() {
        return (
            <div className="how-it-works">
                <div className="container has-text-left">
                    <div className="columns">
                        <div className="column is-half">
                            <h1 className="title is-2">The Best Ordering Experience, Every Time</h1>
                            <hr/>
                            <h1 className="title is-3">All Your Suppliers In One Place</h1>
                            <p>Order from all your Suppliers in one place. And when you want to try someone new,
                                choose from our network of hundreds of Suppliers across 12 categories.</p>
                            <br/>
                            <h1 className="title is-3">Free tools To Make Your Life Easier</h1>
                            <p>Full cost reporting, one-tap reordering, Pantry List for frequently ordered items,
                                talk directly with your Suppliers and easily manage your accounting - anywhere,
                                anytime.
                            </p>
                            <br/>
                            {!this.props.isAuthenticated &&
                            <Link to="/getStarted" className="button is-danger">GET STARTED</Link>
                            }
                            &nbsp;
                            <Link to="/#" className="button is-success">FREE DEMO</Link>
                        </div>
                    </div>
                </div>
            </div>
        );
    };
}

export default HowItWorks;