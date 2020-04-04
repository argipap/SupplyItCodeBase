import React from 'react';
import {shallow, mount} from 'enzyme';
import renderer from 'react-test-renderer';

import Message from '../Message';


describe('When given a success message', () => {
    const removeMessage = jest.fn();

    const messageSuccessProps = {
        messageName: 'Hello, World!',
        messageTitle: 'Title',
        messageType: 'success',
        removeMessage: removeMessage,
    };


    it(`Should have a Toast component`, () => {
        const wrapper = shallow(<Message {...messageSuccessProps} />);
        expect(wrapper.find('Toast')).toHaveLength(1);
    });

    it(`Message renders properly`, () => {
        const wrapper = mount(
            <Message {...messageSuccessProps} />
        );
        expect(wrapper.find('div.fade').prop('variant')).toEqual('success');
        const button = wrapper.find('button');
        expect(removeMessage).toHaveBeenCalledTimes(0);
        button.simulate('click');
        expect(removeMessage).toHaveBeenCalledTimes(1);
    });

    test('Message renders a snapshot properly', () => {
        const tree = renderer.create(
            <Message {...messageSuccessProps} />
        ).toJSON();
        expect(tree).toMatchSnapshot();
    });
});

describe('When given a danger message', () => {
    const removeMessage = jest.fn();

    const messageDangerProps = {
        messageName: 'Hello, World!',
        messageType: 'danger',
        removeMessage: removeMessage,
    };

    it(`Message renders properly`, () => {
        const wrapper = mount(
            <Message {...messageDangerProps} />
        );
        expect(wrapper.find('div.fade').prop('variant')).toEqual('danger');
        const button = wrapper.find('button');
        expect(removeMessage).toHaveBeenCalledTimes(0);
        button.simulate('click');
        expect(removeMessage).toHaveBeenCalledTimes(1);
    });

    test('Message renders a snapshot properly', () => {
        const tree = renderer.create(
            <Message {...messageDangerProps} />
        ).toJSON();
        expect(tree).toMatchSnapshot();
    });
});