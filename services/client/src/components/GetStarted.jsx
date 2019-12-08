import React, {Component} from 'react';
import './mystyle.css';
import Form from "./forms/Form";

class GetStarted extends Component {
    constructor(props) {
        super(props);
    };

    render() {
        return (
            <div className="get-started">
                <div className="container has-text-centered">
                    <div className="columns is-8 is-variable ">
                        <div className="column is-two-thirds has-text-left">
                            <h1 className="title is-1">LET'S GET STARTED</h1>
                            <p className="is-size-4">No credit apps, instant ordering</p>
                            <ul class="ticked-list">
                                <li>
                                    FREE to use
                                </li>
                                <li>
                                    Access to your favourite suppliers near your region
                                </li>
                                <li>
                                    Orders history, last order ready to submit
                                </li>
                            </ul>
                        </div>
                        <div className="column is-one-third">
                            <Form
                                formType={this.props.formType}
                                createMessage={this.props.createMessage}
                                loginUser={this.props.loginUser}
                                isAuthenticated={this.props.isAuthenticated}
                            />
                        </div>
                    </div>
                </div>
            </div>
        );
    };
}

export default GetStarted;