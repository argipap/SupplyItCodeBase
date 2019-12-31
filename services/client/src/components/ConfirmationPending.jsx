import React, { Component } from 'react';
// import { Redirect } from 'react-router-dom';

class ConfirmationPending extends Component {

    render() {
        // if (!this.props.email) {
        //     let HomeURL = '/home';
        //     return (
        //         <Redirect to = {HomeURL} />
        //     );
        // }
        return (
            <div>
                <p>We just send you an activation link to your email {this.props.email}.
                    Please check your email and activate your account.</p>
            </div>
        )
    };
}

export default ConfirmationPending;