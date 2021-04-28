/*global kakao*/
import React, { useEffect } from "react";
import styled from "styled-components";
 
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
        var clusterer = new kakao.maps.MarkerClusterer({
          map: map, // 마커들을 클러스터로 관리하고 표시할 지도 객체 
          averageCenter: true, // 클러스터에 포함된 마커들의 평균 위치를 클러스터 마커 위치로 설정 
          minLevel: 10, // 클러스터 할 최소 지도 레벨 
          calculator: [10, 30, 50], // 클러스터의 크기 구분 값, 각 사이값마다 설정된 text나 style이 적용된다
          texts: getTexts, // texts는 ['삐약', '꼬꼬', '꼬끼오', '치멘'] 이렇게 배열로도 설정할 수 있다 
          styles: [{ // calculator 각 사이 값 마다 적용될 스타일을 지정한다
                  width : '30px', height : '30px',
                  background: 'rgba(51, 204, 255, .8)',
                  borderRadius: '15px',
                  color: '#000',
                  textAlign: 'center',
                  fontWeight: 'bold',
                  lineHeight: '31px'
              },
              {
                  width : '40px', height : '40px',
                  background: 'rgba(255, 153, 0, .8)',
                  borderRadius: '20px',
                  color: '#000',
                  textAlign: 'center',
                  fontWeight: 'bold',
                  lineHeight: '41px'
              },
              {
                  width : '50px', height : '50px',
                  background: 'rgba(255, 51, 204, .8)',
                  borderRadius: '25px',
                  color: '#000',
                  textAlign: 'center',
                  fontWeight: 'bold',
                  lineHeight: '51px'
              },
              {
                  width : '60px', height : '60px',
                  background: 'rgba(255, 80, 80, .8)',
                  borderRadius: '30px',
                  color: '#000',
                  textAlign: 'center',
                  fontWeight: 'bold',
                  lineHeight: '61px'
              }
          ]
        });
        // 2. 레이어 관련 로직
        boundsWithMarkers(props.data, kakao.maps.services.Status.OK)

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
        function getTexts(count) {
          // 한 클러스터 객체가 포함하는 마커의 개수에 따라 다른 텍스트 값을 표시합니다 
          if(count < 10) {
            return '100';        
          } else if(count < 30) {
            return '300';
          } else if(count < 50) {
            return '500';
          } else {
            return '1000';
          }
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