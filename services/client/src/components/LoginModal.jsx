// import React, { Component, useEffect, useState } from 'react';
// import { Link, Redirect } from 'react-router-dom';
// import { Modal, Button } from 'react-bootstrap'
// import Form from './components/forms/Form';



// function LoginModal() {
//   const [show, setShow] = useState(false);

//   const handleClose = () => setShow(false);
//   const handleShow = () => setShow(true);

//   return (
//     <>
//       <Button variant="primary" onClick={handleShow}>
//         Launch demo modal
//       </Button>

//       <Modal show={show} onHide={handleClose}>
//         <Modal.Header closeButton>
//           <Modal.Title>Modal heading</Modal.Title>
//         </Modal.Header>
//           <Modal.Body>
//               <Form
//                           formType={'Login'}
//                           isAuthenticated={this.isAuthenticated}
//                           loginUser={this.loginUser}
//                           createMessage={this.createMessage}
//                       />
//            </Modal.Body>
//           <Modal.Footer>
//           <Button variant="secondary" onClick={handleClose}>
//             Close
//           </Button>
//         </Modal.Footer>
//       </Modal>
//     </>
//   );
// }


// <Container className="login-container">
// 									<Row>
// 										<Col />
// 										<Col sm={6}>
// 											<Form
// 												formType={'Login'}
// 												isAuthenticated={this.isAuthenticated}
// 												loginUser={this.loginUser}
// 												createMessage={this.createMessage}
// 											/>
// 										</Col>
// 									</Row>
// 								</Container>


// // function LoginModal(props) {

// //    const [modalShow, setModalShow] = useState(false)
   
// //     return (
// //       <Modal
// //         {...props}
// //         size="md"
// //         aria-labelledby="contained-modal-title-vcenter"
// //         centered
// //       >
// //         <Modal.Header closeButton>
// //           <Modal.Title id="contained-modal-title-vcenter">
// //             Modal heading
// //           </Modal.Title>
// //         </Modal.Header>
// //         <Modal.Body>
// //           <h4>Centered Modal</h4>
// //           <p>
// //           </p>
// //         </Modal.Body>
// //         <Modal.Footer>
// //           <Button onClick={props.onHide}>Σύνδεση</Button>
// //         </Modal.Footer>
// //       </Modal>
// //     );
// //   }


//   export default LoginModal