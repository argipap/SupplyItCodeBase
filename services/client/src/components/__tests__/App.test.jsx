import React from 'react';
import { shallow, mount } from 'enzyme';

import App from '../../App';

beforeAll(() => {
    global.localStorage = {
        getItem: () => 'someToken'
    };
});

test('App renders without crashing', () => {
    const wrapper = shallow(<App/>);
});
