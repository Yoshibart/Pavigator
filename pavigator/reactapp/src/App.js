import './App.css';
import Maps from './Maps';
import Search from './Search';
import Sign from './Sign';
import Log from './Log';
import SHA256 from 'sha256-es';
import useState from 'react';

 export default function App() {
  const API_URL = "http://127.0.0.1:8000";
 
  const getCookie = name=> {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  const hashPasswd = password => SHA256.hash(password);
  const passwdLength = (password)=> password.length < 9;  

  const validateEmail = email =>{
    //const re = /[a-zA-Z0-9]+[@][a-zA-Z0-9]+[.][a-zA-Z0-9]+/
    //found the pattern at
    //https://stackoverflow.com/questions/201323/how-can-i-validate-an-email-address-using-a-regular-expression
    const re = /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/
    return !re.test(email);
  }
  const passwordLength = (password)=> password.length;
  return (
    // <Sign 
    //   hashPasswd={hashPasswd}
    //   validateEmail={validateEmail}
    //   passwdLength={passwdLength}
    //   API_URL={API_URL}
    //   getCookie={getCookie}
    // />
    // <Log 
    //   hashPasswd={hashPasswd}
    //   validateEmail={validateEmail}
    //   passwdLength={passwdLength}
    //   API_URL={API_URL}
    //   getCookie={getCookie}
    // />
    <Search 
      getCookie={getCookie}
      API_URL={API_URL}
    />
  );
}





