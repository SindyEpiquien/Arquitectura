import React from 'react';
import { shallow } from 'enzyme';

 
import UsersList from '../UsersList';
 
const users = [
  {
    'active': true,
    'email': 'raquel@gmail.com',
    'id': 1,
    'username': 'raquel'
  },
  {
    'active': true,
    'email': 'sindyepiquien@upeu.edu.pe',
    'id': 2,
    'username': 'sindy'
  }
];
 
test('UsersList renders properly', () => {
  const wrapper = shallow(<UsersList users={users}/>);
  const element = wrapper.find('h4');
  expect(element.length).toBe(2);
  expect(element.get(0).props.children).toBe('raquel');
});

  
