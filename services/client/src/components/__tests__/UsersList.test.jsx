import React from 'react';
import {mount} from 'enzyme';

import UsersList from '../UsersList';
import renderer from 'react-test-renderer';

const users = [
    {
        'confirmed': true,
        'admin': false,
        'email': 'argipap@gmail.com',
        'id': 1,
        'username': 'argi'
    },
    {
        'confirmed': true,
        'admin': false,
        'email': 'jimbill@gmail.com',
        'id': 2,
        'username': 'jimbill'
    }
];

test('UsersList renders properly', () => {
    const wrapper = mount(<UsersList users={users}/>);
    // table
    const table = wrapper.find('table');
    expect(table.length).toBe(1);
    // table head
    expect(wrapper.find('thead').length).toBe(1);
    const th = wrapper.find('th.MuiTableCell-root.MuiTableCell-head');
    expect(th.length).toBe(5);
    expect(th.get(0).props.children).toBe('ID');
    expect(th.get(1).props.children).toBe('Email');
    expect(th.get(2).props.children).toBe('Username');
    expect(th.get(3).props.children).toBe('Confirmed');
    expect(th.get(4).props.children).toBe('Admin');
    // table body
    expect(wrapper.find('tbody.MuiTableBody-root').length).toBe(1);
    expect(wrapper.find('tr.MuiTableRow-root').length).toBe(3);
    const td = wrapper.find('td.MuiTableCell-root.MuiTableCell-body.MuiTableCell-alignRight');
    expect(td.length).toBe(8);
    const th_body = wrapper.find('th.MuiTableCell-root.MuiTableCell-body')
    expect(th_body.get(0).props.children).toBe(1);
    expect(td.get(0).props.children).toBe('argipap@gmail.com');
    expect(td.get(1).props.children).toBe('argi');
    expect(td.get(2).props.children).toBe('true');
    expect(td.get(3).props.children).toBe('false');

});

test('UsersList renders a snapshot properly', () => {
    const tree = renderer.create(<UsersList users={users}/>).toJSON();
    expect(tree).toMatchSnapshot();
});