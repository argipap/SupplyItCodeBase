import React from 'react';
import { Alert } from 'react-bootstrap';

const Message = (props) => {
	return (
		<Alert
			variant={`${props.messageType}`}
			onClick={() => {
				props.removeMessage();
			}}
			dismissible
		>
			<Alert.Heading>{props.messageTitle}</Alert.Heading>
			<p>{props.messageName}</p>
		</Alert>
	);
};

export default Message;
