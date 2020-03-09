import React from 'react';
import {Container} from 'react-bootstrap';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

const UsersList = (props) => {
    return (
        <Container className="mt-3">
            <h1>Χρήστες</h1>
            <hr/>
            <TableContainer component={Paper}>
                <Table aria-label="user table">
                    <TableHead>
                        <TableRow>
                            <TableCell>ID</TableCell>
                            <TableCell align="right">Email</TableCell>
                            <TableCell align="right">Username</TableCell>
                            <TableCell align="right">Confirmed</TableCell>
                            <TableCell align="right">Admin</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {props.users.map((user) => (
                            <TableRow key={user.id}>
                                <TableCell component="th" scope="user">
                                    {user.id}
                                </TableCell>
                                <TableCell align="right">{user.email}</TableCell>
                                <TableCell align="right">{user.username}</TableCell>
                                <TableCell align="right">{String(user.confirmed)}</TableCell>
                                <TableCell align="right">{String(user.admin)}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Container>
    );
};

export default UsersList;
