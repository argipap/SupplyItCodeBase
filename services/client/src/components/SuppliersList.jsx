import React, { Component } from 'react';
import axios from 'axios';
import { Container, ListGroup } from 'react-bootstrap';

class SuppliersList extends Component {
	constructor() {
		super();
		this.state = {
			suppliers: []
		};
	}

	componentDidMount() {
		axios.get('http://localhost/users/wholesale').then((res) => {
			const suppliers = res.data.data;
			this.setState({ suppliers });
		});
	}

	render() {
		return (
			<Container ClassName="mt-2">
				{this.state.suppliers.map((supplier) => (
					<ListGroup>
						<ListGroup.Item key={supplier.id}>{supplier.username}</ListGroup.Item>
					</ListGroup>
				))}
			</Container>
		);
	}
}

export default SuppliersList;
