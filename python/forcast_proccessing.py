import csv
import requests

read_f = open('data/div_refine(4_7).csv', 'r', encoding='utf-8')
write_f = open('data/new.csv', 'w', encoding='utf-8')
rdr = csv.reader(read_f)
wdr = csv.writer(write_f)
apiKey = 'NgWMRgmrE%2FyHVKNO%2F2jwDafVAX3Z7J1SAVRoCtg%2FH2pnnW0JGFK4Xx3KodkqYD0fcInktDYBMzBipu144l50bQ%3D%3D'

count = 0 # 진행상황 보기
percentage = 0 # 퍼센테이지
miss_count = 0 # 안된 것

locations = ['속초', '북춘천', '철원', '동두천', '파주', '대관령', '춘천', '백령도', '북강릉', '강릉', '동해', '서울', '인천', '원주', '울릉도', '수원', '영월', '충주', '서산', '울진', '청주', '대전', '추풍령', '안동', '상주', '포항', '군산', '대구', '전주', '울산', '창원', '광주', '부산', '통영', '목포', '여수', '흑산도', '완도', '고창', '순천', '홍성', '제주', '고산', '성산', '서귀포', '진주', '강화', '양평', '이천', '인제', '홍천', '태백', '정선군', '제천', '보은', '천안', '보령', '부여', '금산', '세종', '부안', '임실', '정읍', '남원', '장수', '고창군', '영광군', '김해시', '순창군', '북창원', '양산시', '보성군', '강진군', '장흥', '해남', '고흥', '의령군', '함양군', '광양시', '진도군', '봉화', '영주', '문경', '청송군', '영덕', '의성', '구미', '영천', '경주시', '거창', '합천', '밀양', '산청', '거제', '남해']
location_numbers = ['90', '93', '95', '98', '99', '100', '101', '102', '104', '105', '106', '108', '112', '114', '115', '119', '121', '127', '129', '130', '131', '133', '135', '136', '137', '138', '140', '143', '146', '152', '155', '156', '159', '162', '165', '168', '169', '170', '172', '174', '177', '184', '185', '188', '189', '192', '201', '202', '203', '211', '212', '216', '217', '221', '226', '232', '235', '236', '238', '239', '243', '244', '245', '247', '248', '251', '252', '253', '254', '255', '257', '258', '259', '260', '261', '262', '263', '264', '266', '268', '271', '272', '273', '276', '277', '278', '279', '281', '283', '284', '285', '288', '289', '294', '295']

for idx,line in enumerate(rdr):

  row = line # 새로운 csv의 한줄
  if idx == 0: # 첫줄 입력
    row += ['기온(C)','강수량(mm)', '풍속(m/s)', '습도(%)', '일조(hr)', '일사(MJ/m2)'] # ta, rn, ws, hm, ss(빛이 비췄던 시간), icsr
    wdr.writerow(row)
    continue

  # api 요청 파라미터 값
  parameters = {
    'startDt': '20200120',
    'startHh': '01',
    'endDt': '20200120',
    'endHh':'01',
    'stnIds': '108',
  }
  # 요청파라미터 처리

  ## 시간 처리
  dates = line[1].split()
  parameters['startDt'] = dates[0].replace('-','')
  parameters['endDt'] = dates[0].replace('-','')
  time =  str(dates[1].split(':')[0])
  if len(time) == 1:
    time = '0' + time
  parameters['startHh'] = time
  parameters['endHh'] = time
  
  ## 지점코드 처리
  for idx, location in enumerate(locations):
    if location in line[2]:
      parameters['stnIds'] = str(location_numbers[idx]) 
      break

  # 요청 URL
  Url = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList?serviceKey='+apiKey+'&numOfRows=10&pageNo=1&dataType=JSON&dataCd=ASOS&dateCd=HR'
  Url += '&startDt='+parameters['startDt']+'&startHh='+parameters['startHh']+'&endDt='+parameters['endDt']+'&endHh='+parameters['endHh']+'&stnIds='+parameters['stnIds']
  
  l = requests.get(Url)
  result = {}
  try:
    result = dict(l.json())
    ta = result['response']['body']['items']['item'][0]['ta'] # 기온
    rn = result['response']['body']['items']['item'][0]['rn'] # 강수량
    ws = result['response']['body']['items']['item'][0]['ws'] # 풍속
    hm = result['response']['body']['items']['item'][0]['hm'] # 습도
    ss = result['response']['body']['items']['item'][0]['ss'] # 일조
    icsr = result['response']['body']['items']['item'][0]['icsr'] # 일사
    row += [ta, rn, ws, hm, ss, icsr]
    wdr.writerow(row)
  except:
    miss_count += 1
  
  count += 1
  if count % 42 == 0:
    percentage += 1
    print(percentage/10, "%")
    print((miss_count / count)*100, '%')
    print(miss_count, count)