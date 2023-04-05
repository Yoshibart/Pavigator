import { useState } from 'react';
import Maps from './Maps';

export default function Search({API_URL,getCookie}){
  const [times, seTimes] = useState([]);
  const [locale, setLocale] = useState([]);
  const [start, setStart] = useState([]);
  const [end, setEnd] = useState([]);
  const [stop, setStop] = useState("");
  const [banner, setBanner] = useState("")
  const [error, getError] = useState(false)
  const [inputs, setInputs] = useState({
    origin:"",
    destination:""
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

  const setSearchElements = event =>{
    setStop(event.target.value)
  }

  const handleSearch = async (event) =>{ 
    event.preventDefault();
    const postRequest = {
      method:'GET',
      headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':getCookie('csrftoken')
      },
    }
    const Getresponse = await fetch(`${API_URL}/timetable/${stop}`, postRequest);
    getError(!Getresponse.ok)
    const json = await Getresponse.json();
    seTimes(json["TimeTable"]);
    setBanner(json["Stop"])
  }

  const handleLocate = async (event) =>{
    event.preventDefault();
    const postRequest = {
      method:'POST',
      headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':getCookie('csrftoken')
      },
      body:JSON.stringify(inputs)
    }
    const Getresponse = await fetch(`${API_URL}/routing/`, postRequest);
    getError(!Getresponse.ok)
    const json = await Getresponse.json();
    setLocale(json["Location"]);
    setStart(json["start"]);
    setEnd(json["end"]);
    console.log(json["extras"])
  }

  const stoptimes = times.map((number) =>
    <li key={number.TripID}><span>{number["Bus"]}</span> --------- <span>{number["scheduledArrivalTime"]}</span></li>
  );
  // console.log(locale)
  return (
    <main>    
        <div>
            <div id="section--1">
              <h2>Pavigator</h2>
              <form>
                  <p>
                      <input 
                          onChange={setSearchElements}
                          type="text" 
                          name="search" 
                          placeholder="Enter Stop Number" 
                          value={stop}
                      />
                      <button  onClick={handleSearch} >Search</button>
                  </p>
              </form>
              <form>
                  <p>
                    <label htmlFor="origin">Origin:</label>
                    <input 
                        onChange={setNewInputs}
                        type="text" 
                        name="origin" 
                        placeholder="location" 
                        value={inputs.origin}
                        required
                        id="id_origin"
                      />
                  </p>
                  <p>
                    <label htmlFor="destination">Destination:</label>
                    <input 
                        onChange={setNewInputs}
                        type="text" 
                        name="destination" 
                        placeholder="destination" 
                        value={inputs.destination}
                        required
                        id="id_destination"
                      />
                  </p>
                  <p>
                      <button onClick={handleLocate}>Locate</button>
                  </p>
              </form>
              <div>
                  {times.length !== 0 && !error? <ul><span>BusNumber</span><span>Minutes</span>{stoptimes}</ul> : <p>No Stop Times</p>}
              </div>
                  <button type="button">Log Out</button>
            </div>

            <div id="section--2" style={{width:"50%",height:"35rem" }}>
                <Maps
                  points={locale.length !== 0 ? locale : undefined}
                  start={start.length !== 0 ? start : undefined}
                  end={end.length !== 0 ? end : undefined}
                  
                />
            </div>
        </div>
    </main>
  );
}
