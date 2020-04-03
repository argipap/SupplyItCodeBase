import React, {useState} from 'react';
import {Toast, ToastHeader, ToastBody} from 'react-bootstrap';

const Message = (props) => {
	const [ show, setShow ] = useState(false);

	const toggleClose = props.removeMessage;

	return (
			<Toast variant={`${props.messageType}`} show={show} onClose={toggleClose}>
				<ToastHeader>{props.messageTitle}</ToastHeader>

				<ToastBody>{props.messageName}</ToastBody>
			</Toast>
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
