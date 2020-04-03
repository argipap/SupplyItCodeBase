import React from 'react';
import {mount} from 'enzyme';
import renderer from 'react-test-renderer';
import {MemoryRouter as Router} from 'react-router-dom';
import routeData from 'react-router';


import NavBar from '../NavBar';

const title = 'SupplyIT logo';
const mockLocation = {
    pathname: '/login',
    hash: '',
    search: '',
    state: '',
};

const isAuthenticated = jest.fn();
const logoutUser = jest.fn();


beforeEach(() => {
    jest.spyOn(routeData, 'useLocation').mockReturnValue(mockLocation);
});

test('NavBar renders properly', () => {
    const component = <Router><NavBar title={title} isAuthenticated={isAuthenticated} logoutUser={logoutUser}/></Router>;

    const wrapper = mount(component);
    const element = wrapper.find('nav[role="navigation"]');
    expect(element.length).toBe(1);
    const img = wrapper.find('img');
    expect(img.get(0).props['alt']).toBe(title);
});

test('NavBar renders a snapshot properly', () => {
    const tree = renderer.create(
        <Router location="/"><NavBar title={title} isAuthenticated={isAuthenticated} logoutUser={logoutUser}/></Router>
    ).toJSON();
    expect(tree).toMatchSnapshot();
});