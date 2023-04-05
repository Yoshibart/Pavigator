import { render, screen } from '@testing-library/react';

test('Returns false for a valid email', () => {
  expect(!validateEmail(' john.doe@example.com ')).toBe(true);
});

test('Returns true for an invalid email', () => {
  expect(!validateEmail('john.doe@')).toBe(false);
});

test('Returns true for an empty email', () => {
  expect(!validateEmail('')).toBe(false);
});

test('Returns true for a null email', () => {
  expect(!validateEmail(null)).toBe(false);
});

const validateEmail = email =>{
  const re = /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/
  return !re.test(email);
}

test('Returns false password length above 9', () => {
  expect(passwdLength("sk%^&&HHHdfgsd")).toBe(false);
});

test('Returns true since password length is 8', () => {
  expect(passwdLength("password")).toBe(true);
});

test('Returns false password length equal 9', () => {
  expect(passwdLength("passwords")).toBe(false);
});

const passwdLength = (password)=> password.length < 9;  



