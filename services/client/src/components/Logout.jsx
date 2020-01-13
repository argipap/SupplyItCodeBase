import React, { useEffect, useState } from 'react';
import { Link, Redirect } from 'react-router-dom';

function Logout(props) {
	useEffect(() => {
		props.logoutUser();
	});

	const [ redirect, setRedirect ] = useState(false);

	useEffect(() => {
		let timer1 = setTimeout(() => setRedirect(true), 1000);
		return () => {
			clearTimeout(timer1)
		}
	}, []);
	return ( 
		<div>
			<p>
				You are now logged out. Click <Link to="/login">here</Link> to log back in.
			</p>
			<Redirect to="/" />
		</div>
	);
}

export default Logout;

// --Class version--
// class Logout extends Component {
// 	componentDidMount() {
// 		this.props.logoutUser();
// 	}

// 	render() {
// 		return (
// 			<div>
// 				<p>
// 					You are now logged out. Click <Link to="/login">here</Link> to log back in.
// 				</p>
// 				<Redirect to="/" />
// 			</div>
// 		);
// 	}
// }
