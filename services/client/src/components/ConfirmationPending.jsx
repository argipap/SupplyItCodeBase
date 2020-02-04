import React, { Component } from 'react';

class ConfirmationPending extends Component {

    render() {
        return (
            <div>
                <p>We just send you an activation link to your email {this.props.email}.
                    Please check your email and activate your account.</p>
            </div>
        )
    };
}

export default ConfirmationPending;