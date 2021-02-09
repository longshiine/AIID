import csv
import requests

read_f = open('data/data.csv', 'r', encoding='utf-8')
write_f = open('data/new.csv', 'w', encoding='utf-8')
rdr = csv.reader(read_f)
wdr = csv.writer(write_f)

for idx,line in enumerate(rdr):
  # line의 구성: 대상구분, 성별, 나이, 관할관서, 접수관서, 접수일자, 주소, 실종(가출)경력, 주로 다니는 장소
  row = line[:6] # 새로운 csv의 한줄
  if idx == 0:
    row += '주소' + 'X' + 'Y' + line[7:]
    wdr.writerow(row)
    continue

  # 주소 -> 좌표 변환코드(Geocoder사용)
  # 지번, 도로명 주소 둘다 제대로 있기만 하면 변환 가능
  # line[6] -> line[6] 주소, line[7] x좌표, line[8] y좌표
  # 주소에 대한 정보 없는 경우에는 -> 주소, 0, 0
  if len(line[6].split()) > 2:
    r = requests.get('http://apis.vworld.kr/new2coord.do?q='+line[6]+'&apiKey=767B7ADF-10BA-3D86-AB7E-02816B5B92E9&domain=http://map.vworld.kr/&output=json')
    result = dict(r.json())
    if len(result) == 1:
      r = requests.get('http://apis.vworld.kr/jibun2coord.do?q='+line[6]+'&apiKey=767B7ADF-10BA-3D86-AB7E-02816B5B92E9&domain=http://map.vworld.kr/&output=json')
      result = dict(r.json())
      if len(result) == 1:
        row += [line[6],0,0]
      else:
        row += [result['JUSO'], result['EPSG_4326_X'], result['EPSG_4326_Y']]
    else:
      row += [result['JUSO'], result['EPSG_4326_X'], result['EPSG_4326_Y']]
  
  row += line[7:] # 나머지도 그대로 입력
  print(row)
  wdr.writerow(row)