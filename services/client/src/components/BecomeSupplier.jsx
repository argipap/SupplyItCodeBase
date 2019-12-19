import React, {Component} from 'react';
import './mystyle.css';
import Form from "./forms/Form";

class BecomeSupplier extends Component {
    constructor(props) {
        super(props);
    };

    render() {
        return (
            <div className="become-supplier">
                <div className="container has-text-centered">
                    <div className="columns is-8 is-variable ">
                        <div className="column is-three-fifths has-text-left">
                            <h1 className="title is-2">BECOME A SUPPLIER</h1>
                            <hr/>
                            <h1 className="title is-3">FREE TO JOIN, EASY TO USE</h1>
                            <p>
                                Join SupplyIt for free and pay a small fee for the sales we get you. Easily manage your
                                products and customers in the cloud. Give customers the best ordering experience
                                on desktop and mobile every time.
                            </p>
                            <br/>
                            <h1 className="title is-3">NEW CUSTOMERS, NO HEADACHES</h1>
                            <p>
                                SupplyIt facilitates payments so you get paid on time everytime (no accounts receivable
                                team necessary). Our fantastic customer service team is here to help solve any issues,
                                meaning your sales can increase rapidly without any headaches for your business.
                            </p>
                            <br/>
                            <h1 className="title is-3">YOUR PRODUCT, OUR SALES & MARKETING</h1>
                            <p>
                                We have an on ground sales force in addition to an incredible marketing and promotions
                                platform. With SupplyIt your products and business will be pushed to our growing list of
                                foodservice venues. We'll work with you to find the best customers for your product and
                                help you grow.
                            </p>
                        </div>
                        <div className="column is-two-fifths has-text-left">
                            <h1 className="title is-2">JOIN US</h1>
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

export default BecomeSupplier;