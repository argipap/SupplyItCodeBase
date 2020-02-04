import React, { useState } from 'react';
import { Toast, ToastHeader, ToastBody } from 'react-bootstrap';
import styled from 'styled-components';

const StyledToast = styled(Toast)`
	position: fixed;
	transform: translateX(50%) translateY(50%);
	top: 5%;
	right: 15%;
	width: 45%;
`;

const StyledHeader = styled(ToastHeader)`
font-weight: 700;
`;

const Message = (props) => {
	const [ show, setShow ] = useState(true);

	const toggleShow = () => setShow(!show);

	return (
			<StyledToast variant={`${props.messageType}`} show={show} onClose={toggleShow}>
				<StyledHeader>{props.messageTitle}</StyledHeader>

				<Toast.Body>{props.messageName}</Toast.Body>
			</StyledToast>
	);
};

export default Message;

// <Alert
// variant={`${props.messageType}`}
// onClick={() => {
// 	props.removeMessage();
// }}
// dismissible
// >
// <Alert.Heading>{props.messageTitle}</Alert.Heading>
// <p>{props.messageName}</p>
// </Alert>
