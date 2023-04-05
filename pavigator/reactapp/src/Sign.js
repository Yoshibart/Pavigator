import { useState }  from 'react';
import myImage from './image1.jpg';


export default function Sign({hashPasswd,validateEmail,passwdLength,API_URL,getCookie}) {
  const [inputs, setInputs] = useState({
    firstName:"",
    lastName:"",
    email:"",
    password:""
  });
  const [response, setResponse] = useState()
  const setNewInputs = event =>{
    setInputs(oldata =>{
      return {
            ...oldata,
            [event.target.name]:event.target.value
      }
    })
  }
  const handleSubmit = async (event) =>{
    event.preventDefault();
    const pass = {...inputs}//hashPasswd(inputs.password)
    pass.password = hashPasswd(pass.password)
    const postRequest = {
      method:'POST',
      headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':getCookie('csrftoken')
      },
      body: JSON.stringify(pass)
    }
    const Getresponse = await fetch(`${API_URL}/create/`, postRequest);
    const json = await Getresponse.json();
    setResponse(json);
  }

  return (
    <main>
      <h1>Create Account</h1>
      <div id="left-div"> 
        <h2>Pavigator</h2>
        <h2>{response !== null ? response : ''}</h2>
      <form onSubmit={handleSubmit}>
        <p>
          <label htmlFor="firstName">Firstname:</label>
          <input 
              onChange={setNewInputs}
              type="text" 
              name="firstName" 
              placeholder="First Name" 
              value={inputs.firstName}
              required
            />
        </p>    
        <p>
          <label htmlFor="lastName">Lastname:</label>
          <input 
              onChange={setNewInputs}
              type="text" 
              name="lastName" 
              placeholder="Last Name" 
              value={inputs.lastName}
              required            
            />
        </p>
        <p>
          {  document.getElementById("id_email") !== null && document.getElementById("id_email").value !== "" && validateEmail(inputs.email) && <span style={{color:"red"}}>wrong email format</span>}
          <br/><label htmlFor="email">Email:</label>
          <input 
              // style={validateEmail(inputs.email) ? {backgroundColor:"#ff0000"} : {backgroundColor:"green"}}
              onChange={setNewInputs}
              type="text" 
              name="email" 
              placeholder="Email" 
              value={inputs.email}
              required
              id="id_email"
            />
        </p>
        <p>
          { document.getElementById("id_password") !== null && document.getElementById("id_password").value !== "" && passwdLength(inputs.password) && (
            <span style={{color:"red"}}>short password</span>
          )}
          <br/><label htmlFor="password">Password:</label>
          <input
            // style={passwdLength(inputs.password) ? {backgroundColor:"#ff0000"} : {backgroundColor:"green"}}
            onChange={setNewInputs}
            type="password" 
            name="password" 
            placeholder="Password" 
            value={inputs.password}
            id="id_password"
            required
          />
        </p>
        <button disabled={validateEmail(inputs.email) || passwdLength(inputs.password)} >SignIn</button>
      </form>
      </div>
      {/*<div id="right-div"> <img src="image1.jpg" alt="Image description"/> </div>*/}
    </main>
  );
}
