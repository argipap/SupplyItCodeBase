import React, { useState } from 'react';
import { Container, Toast, ToastHeader, ToastBody } from 'react-bootstrap';
import styled from 'styled-components';

const StyledContainer = styled(Container)`
	/* position: 'relative'; */
`;

const StyledToast = styled(Toast)`
	position: fixed;
	transform: translateX(50%) translateY(50%);
	top: 5%;
	right: 15%;
	width: 50%;
`;

const StyledHeader = styled(ToastBody)`
font-weight: 700;
`

const Message = (props) => {
	const [ show, setShow ] = useState(true);

	const toggleShow = () => setShow(!show);

	return (
		// <StyledContainer>
			<StyledToast variant={`${props.messageType}`} show={show} onClose={toggleShow}>
				<StyledHeader>{props.messageTitle}</StyledHeader>

				<Toast.Body>{props.messageName}</Toast.Body>
			</StyledToast>
		// </StyledContainer>
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
