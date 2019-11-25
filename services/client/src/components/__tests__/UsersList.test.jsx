import React from 'react';
import { shallow } from 'enzyme';

import UsersList from '../UsersList';
import renderer from 'react-test-renderer';

const users = [
    {
        'active': true,
        'email': 'test@gmail.com',
        'id': 1,
        'username': 'test'
    },
    {
        'active': true,
        'email': 'test2@gmail.org',
        'id': 2,
        'username': 'test2'
    }
];

test('UsersList renders properly', () => {
    const wrapper = shallow(<UsersList users={users}/>);
    const element = wrapper.find('h4');
    expect(element.length).toBe(2);
    expect(element.get(0).props.children).toBe('test');
    expect(element.get(1).props.children).toBe('test2');
});

test('UsersList renders a snapshot properly', () => {
    const tree = renderer.create(<UsersList users={users}/>).toJSON();
    expect(tree).toMatchSnapshot();
});