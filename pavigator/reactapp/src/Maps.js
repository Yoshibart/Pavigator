import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import icon from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";
import { useState, useEffect } from 'react';

export default function Maps({points, start,end}) {
  // console.log(points)
  useEffect(() => {
    const map = L.map("section--2", { center: [53.3522443611407,-6.26372321891882], zoom: 13 });

    if (!map.hasLayer(map)) {
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(map);

    if(start !== undefined){
      map.fitBounds(L.polyline(start, {color: 'red',dashArray:'5,10'}).addTo(map).getBounds());
    }
    if(end !== undefined){
      map.fitBounds(L.polyline(end, {color: 'red',dashArray:'5,10'}).addTo(map).getBounds());
    }
    if(points !== undefined){
      map.fitBounds(L.polyline(points, {color: 'red'}).addTo(map).getBounds());
    }
    
    }

    return () => {
      map.remove();
    };
  }, [start,points,end]);

  return (
    <div id="section--2" style={{ width: '50%', height: '25rem' }}></div>
  );
}
