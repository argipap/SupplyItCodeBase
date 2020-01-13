import React, { useState } from 'react';
import { Alert } from 'react-bootstrap'

// const Message = (props) => {
//     return (
//         <div className={`notification is-${props.messageType}`}>
//             <button className="delete" onClick={()=>{props.removeMessage()}}></button>
//             <span>{props.messageName}</span>
//         </div>
//     )
// };


const Message = function AlertDismissible(props) {
    const [show, setShow] = useState(true);
  
   if(show){
    return (
        <Alert variant={`${props.messageType}`} onClose={() => setShow(false)} dismissible>
          <Alert.Heading>{props.messageTitle}</Alert.Heading>
          <p>
            {props.messageName}
          </p>
        </Alert>   
    );
}

}

export default Message;