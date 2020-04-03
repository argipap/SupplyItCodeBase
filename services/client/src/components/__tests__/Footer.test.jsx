import React from 'react';
import { mount } from 'enzyme';
import renderer from 'react-test-renderer';
import {BrowserRouter as Router} from 'react-router-dom';


import Footer from '../Footer';

const isAuthenticated = jest.fn();

test('Footer renders properly', () => {
    const wrapper = mount(<Router><Footer isAuthenticated={isAuthenticated}/></Router>);
    const element = wrapper.find('div.footer-copyright');
    expect(element.length).toBe(1);
    expect(element.text()).toBe('©2019 Supplyit.gr');
});

test('Footer renders a snapshot properly', () => {
    const tree = renderer.create(<Router><Footer isAuthenticated={isAuthenticated}/></Router>).toJSON();
    expect(tree).toMatchSnapshot();
});