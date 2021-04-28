// import KakaoMap from "./KakaoMap"
import KakaoMap from "./KakaoMap"
import {data} from "./data"
import React, { useState, useEffect } from "react";

function App() {
  const latlng = {
    lat: 37.1234,
    lng: 127.128
  }
  return (
    <div className="App">
      {/* <KakaoMap latlng={latlng} data={data}/> */}
      <KakaoMap latlng={latlng} data={data}/>
    </div>
  );
}

export default App;
