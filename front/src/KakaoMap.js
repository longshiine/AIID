/*global kakao*/
import React, { useEffect } from "react";
import styled from "styled-components";
import seoulGeo from "./seoul"
 
const KakaoMap = (props) => {
  useEffect(() => {
    // 0. Map initialize
    const script = document.createElement("script");
    script.async = true;
    script.src = "https://dapi.kakao.com/v2/maps/sdk.js?appkey=5c8b46c9fb95f0c357280a31672c2ffe&autoload=false&libraries=services,clusterer";
    document.head.appendChild(script);
    script.onload = () => {
      kakao.maps.load(() => {
        // 1. 지도 객체 생성 및 document에 bind
        let container = document.getElementById("Mymap");
        let options = {
          center: new kakao.maps.LatLng(props.latlng.lat, props.latlng.lng),
          level: 3
        };
        const map = new window.kakao.maps.Map(container, options);
        var infowindow = new kakao.maps.InfoWindow({zIndex:1});
        var customOverlay = new kakao.maps.CustomOverlay({});
        

        // 2. 레이어 관련 로직
        boundsWithMarkers(props.data, kakao.maps.services.Status.OK)
        seoulGeo.features.forEach((val, index) => {
          const coordinates = val.geometry.coordinates;
          const name = val.properties.name;
          displayArea(coordinates, name, index);
        });

        // 3. Functions
        function boundsWithMarkers (data, status) { // 마커들을 표시하고, 마커들 기준으로 지도를 다시 세팅
            if (status === kakao.maps.services.Status.OK) {
                // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
                // LatLngBounds 객체에 좌표를 추가합니다
                var bounds = new kakao.maps.LatLngBounds();
                data.forEach(element => {
                  bounds.extend(new kakao.maps.LatLng(element.y, element.x));
                  displayMarker(element);
                });
                map.setBounds(bounds);
            } 
        }
        function displayMarker(place) { // 지도에 마커를 표시하는 함수입니다
            // 마커를 생성하고 지도에 표시합니다
            var marker = new kakao.maps.Marker({
                map: map,
                position: new kakao.maps.LatLng(place.y, place.x) 
            });
            // 마커에 클릭이벤트를 등록합니다
            kakao.maps.event.addListener(marker, 'click', function() {
                // 마커를 클릭하면 장소명이 인포윈도우에 표출됩니다
                infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>');
                infowindow.open(map, marker);
            });
            return marker
        }
        function AIIDInfo(name){
          const color = {'노원구': '#E03F3C', '동작구': '#fff', '성북구': '#F7A49B', '용산구': '#E3C4BD', '영등포구': '#E3C4BD', '중랑구': '#F7A49B', '강서구': '#E03F3C', '송파구': '#E03F3C', '서초구': '#E3C4BD', '관악구': '#F7A49B', '광진구': '#E3C4BD', '구로구': '#F7A49B', '은평구': '#E03F3C', '마포구': '#E3C4BD', '양천구': '#F7A49B', '도봉구': '#F7A49B', '강동구': '#E03F3C', '강남구': '#E3C4BD', '강북구': '#E3C4BD', '동대문구': '#753B39', '금천구': '#E3C4BD', '종로구': '#fff', '성동구': '#E3C4BD', '서대문구': '#F7A49B', '중구': '#fff'}
          const count = {'노원구': 1395, '동작구': 591, '성북구': 1110, '용산구': 759, '영등포구': 721, '중랑구': 1021, '강서구': 1332, '송파구': 1338, '서초구': 608, '관악구': 1106, '광진구': 644, '구로구': 989, '은평구': 1463, '마포구': 884, '양천구': 1084, '도봉구': 1174, '강동구': 1320, '강남구': 776, '강북구': 861, '동대문구': 1816, '금천구': 782, '종로구': 312, '성동구': 675, '서대문구': 1040, '중구': 346}
          return {
            color: color[name],
            count: count[name]
          };
        }
        function displayArea(coordinates, name, index) {
          let path = [];            //폴리곤 그려줄 path
          let points = [];        //중심좌표 구하기 위한 지역구 좌표들
          const {color, count} = AIIDInfo(name)
          coordinates[0].forEach((coordinate) => {
              let point = new Object();
              point.x = coordinate[1];
              point.y = coordinate[0];
              points.push(point);
              path.push(new kakao.maps.LatLng(coordinate[1], coordinate[0]));  
          })
          // 다각형을 생성합니다 
          const polygon = new kakao.maps.Polygon({
              map : map, // 다각형을 표시할 지도 객체
              path : path,
              strokeWeight : 1,
              strokeColor : '#fff',
              strokeOpacity : 0.7,
              fillColor : color,
              fillOpacity : 0.5
          });
          kakao.maps.event.addListener(polygon, 'mouseover', function(mouseEvent) {
            polygon.setOptions({fillColor: '#09f'});
            customOverlay.setContent('<div style="position: absolute; background: #fff; border: 1px solid #888; border-radius:3px; font-size: 12px; top: -5px;left: 15px;padding:2px;">' + name + ', 실종건수: '+ count + '</div>');
            customOverlay.setPosition(mouseEvent.latLng); 
            customOverlay.setMap(map);
          });
          // 다각형에 mousemove 이벤트를 등록하고 이벤트가 발생하면 커스텀 오버레이의 위치를 변경합니다 
          kakao.maps.event.addListener(polygon, 'mousemove', function(mouseEvent) {
              customOverlay.setPosition(mouseEvent.latLng); 
          });
          // 커스텀 오버레이를 지도에서 제거합니다 
          kakao.maps.event.addListener(polygon, 'mouseout', function() {
              polygon.setOptions({fillColor: color});
              customOverlay.setMap(null);
          }); 
        } 
      });
    };
  }, []);
  
  return (
    <Container >
      <Title>
        실시간 이상행동 위치
      </Title>
      <MapContents id="Mymap" />
      <InfoTitle>실종가능성</InfoTitle>
      <Info>300이상: 매우낮음, 600이상: 낮음, 900이상: 중간, 1200이상: 위험,  1500이상: 매우위험</Info>
    </Container>
  );
}

const Container = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 10px;
  align-items: center;
  justify-content: center;
`
const Title = styled.div`
  border: 2px solid;
  padding: 10px;
  margin-bottom: 10px;
  font-size: 20px;
  font-weight: heavy;
  align-items: center;
`
const MapContents = styled.div`
  width: 95%;
  height: 400px;
  align-items: center;
`
const InfoTitle = styled.div`
  border: 1px solid;
  padding: 5px;
  margin-top: 10px;
`
const Info = styled.div`
  border: 1px solid;
  padding: 5px;
  margin-top: 5px;
`


export default KakaoMap;