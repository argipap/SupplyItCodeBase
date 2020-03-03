import React from 'react';
import { mount } from 'enzyme';
import renderer from 'react-test-renderer';

import Footer from '../Footer';

test('Footer renders properly', () => {
    const wrapper = mount(<Footer/>);
    const element = wrapper.find('div.footer-copyright');
    expect(element.length).toBe(1);
    expect(element.text()).toBe('©2019 Supplyit.gr');
});

test('Footer renders a snapshot properly', () => {
    const tree = renderer.create(<Footer/>).toJSON();
    expect(tree).toMatchSnapshot();
});