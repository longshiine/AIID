/*global kakao*/
import React, { useEffect } from "react";
import styled from "styled-components";
import seoulGeo from "./seoul"
import {api_key} from "./config/config"

const KakaoMap = (props) => {
  useEffect(() => {
    // 0. Map initialize
    const script = document.createElement("script");
    script.async = true;
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${api_key}&autoload=false&libraries=services,clusterer`;
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
        var clusterer = new kakao.maps.MarkerClusterer({
          map: map, // 마커들을 클러스터로 관리하고 표시할 지도 객체 
          averageCenter: true, // 클러스터에 포함된 마커들의 평균 위치를 클러스터 마커 위치로 설정 
          minLevel: 10 // 클러스터 할 최소 지도 레벨 
        });
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
                var markers = [];
                data.forEach(element => {
                  bounds.extend(new kakao.maps.LatLng(element.lat, element.lng));
                  markers.push(displayMarker(element));
                });
                clusterer.addMarkers(markers);
                map.setBounds(bounds);

            } 
        }
        function displayMarker(place) { // 지도에 마커를 표시하는 함수입니다
            // 마커를 생성하고 지도에 표시합니다
            var marker = new kakao.maps.Marker({
                map: map,
                position: new kakao.maps.LatLng(place.lat, place.lng) 
            });
            // 마커에 클릭이벤트를 등록합니다
            kakao.maps.event.addListener(marker, 'click', function() {
                // 마커를 클릭하면 장소명이 인포윈도우에 표출됩니다
                infowindow.setContent('<div style="padding:5px;font-size:12px;">' + "sample" + '</div>');
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
          coordinates[0].forEach((coordinate, idx) => {
              let point = new Object();
              if (idx % 2) {
                point.x = coordinate[1];
                point.y = coordinate[0];
                points.push(point);
                path.push(new kakao.maps.LatLng(coordinate[1], coordinate[0]));  
              }
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
          kakao.maps.event.addListener(polygon, 'click', function(mouseEvent) {
            var level = map.getLevel()-2;
            map.setLevel(level, {anchor: centroid(points), animate: {
              duration: 350
            }})
          });
        }
        function centroid(points) {
          var i, j, len, p1, p2, f, area, x, y;
          area = x = y = 0;
          for (i =0, len = points.length, j = len -1; i< len; j = i++){
            p1 = points[i];
            p2 = points[j]
            f = p1.y * p2.x - p2.y * p1.x;
            x += (p1.x +p2.x) * f;
            y += (p1.y +p2.y) * f;
            area += f * 3;
          }
          return new kakao.maps.LatLng(x /area, y / area);
        } 
      });
    };
  }, [props.marker]);
  return (
    <Container >
      <Title>
        마커 디스플레이
      </Title>
      <MapContents id="Mymap" />
      {/* <InfoTitle>실종가능성</InfoTitle>
      <Info>
        <VeryLow>300이상: 매우낮음,</VeryLow> 
        <Low>600이상: 낮음,</Low> 
        <Middle>900이상: 중간,</Middle>
        <High>1200이상: 위험,</High> 
        <VeryHigh>1500이상: 매우위험</VeryHigh>
      </Info> */}
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
  background-color: black;
  color: #fff;
`
const Info = styled.div`
  background-color: black;
  border: 1px solid;
  padding: 5px;
  margin-top: 5px;
`
const VeryLow = styled.span`
  color: #fff;
  margin-right: 15px;
`
const Low = styled.span`
  color: #E3C4BD;
  margin-right: 15px;
`
const Middle = styled.span`
  color: #F7A49B;
  margin-right: 15px;
`
const High = styled.span`
  color: #E03F3C;
  margin-right: 15px;
`
const VeryHigh = styled.span`
  color: #753B39;
  margin-right: 15px;
`
export default KakaoMap;