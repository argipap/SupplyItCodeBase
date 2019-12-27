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
                        <div className="column is-three-fifths">
                            <h1 className="title is-3">THE BEST ORDERING EXPERIENCE, <br/> EVERY TIME</h1>
                            <hr/>
                            <h1 className="title is-4">ALL YOUR SUPPLIERS IN ONE PLACE</h1>
                            <p>Order from all your Suppliers in one place. And when you want to try someone new,
                                choose from our network of hundreds of Suppliers across 12 categories.</p>
                            <br/>
                            <h1 className="title is-4">FREE TOOLS TO MAKE YOUR LIFE EASIER</h1>
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