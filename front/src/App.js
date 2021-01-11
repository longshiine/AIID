import KakaoMap from "./KakaoMap"
import {data} from "./data"
function App() {
  const latlng = {
    lat: 37,
    lng: 127.128
  }
  return (
    <div className="App">
      <KakaoMap latlng={latlng} data={data}/>
    </div>
  );
}

export default App;
