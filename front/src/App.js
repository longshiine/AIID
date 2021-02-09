// import KakaoMap from "./KakaoMap"
import KakaoMap from "./Cor"
import {data} from "./data"
import React, { useState, useEffect } from "react";

function App() {
  // const [seconds, setSeconds] = useState(0);
  // const [marker, setMarker] = useState({});
  // useEffect(() => {
  //   const countdown = setInterval(() => {
  //     setSeconds(parseInt(seconds) + 1);
  //     if (seconds % 4 == 3){
  //       setMarker(data[3])
  //     } 
  //     else if (seconds % 4 == 2) {
  //       setMarker(data[2])
  //     }
  //     else if (seconds % 4 == 1) {
  //       setMarker(data[1])
  //     }
  //     else {
  //       setMarker(data[0])
  //     }
  //   }, 1000);
  //   return () => clearInterval(countdown);
  // }, [seconds]);
  const latlng = {
    lat: 37,
    lng: 127.128
  }
  return (
    <div className="App">
      {/* <KakaoMap latlng={latlng} data={data}/> */}
      <KakaoMap/>
    </div>
  );
}

export default App;
