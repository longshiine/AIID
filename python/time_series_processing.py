import csv
import math
import matplotlib.pyplot as plt
import requests
import json
import datetime

f = open('data/only_one_location.csv', 'r', encoding='utf-8')
ff = open('data/new.csv', 'w', encoding='utf-8')
rdr = csv.reader(f)
wdr = csv.writer(ff)

# locations = sorted(locations, key=lambda x: x[1])

# for year in range(2015, 2020):
#   for month in range(1, 13):
#     for day in range(1, 32):
#       if month == 2 and day > 28: continue
#       if (month in [4,6,9,11]) and day > 30: continue
#       for hour in range(0, 24):
#         date = '{} {}'.format(datetime.date(year, month, day), datetime.time(hour).isoformat(timespec='minutes'))
#         row = ['아동(18세미만)', date, '경기도 안산시 상록구 본오동', 126.867721205949, 37.2838256332649, 0]
#         if locations and date == locations[0][1]:
#           while locations and locations[0][1] == date:
#             row = locations.pop(0)
#             wdr.writerow(row)
#         else:
#           wdr.writerow(row)
        
# for idx,line in enumerate(rdr):
#   if idx == 0:
#     wdr.writerow(['실종여부','신고대상','발생일시','주소','X','Y','기온(C)','강수량(mm)','풍속(m/s)','습도(%)','일조(hr)','일사(MJ/m2)'])
#   else: 
#     row = [line[5], line[1]] + [line[2].rstrip()] +line[3:5]
#     wdr.writerow(row)

apiKey = 'ALz2vPSUQfHRKrNWGh2biyEBTpej1%2BGRZmciw5kdIWv76bNE6vKaYQ%2FopssPisYiLR08EGu%2Bv6LERqMn3PffAw%3D%3D'
count = 0
miss_count = 0
weather_data= []
index = 0
locations = []
for idx,line in enumerate(rdr):
  if idx == 0: # 첫줄 입력
    wdr.writerow(line)
    continue
  row = line
  if line[0] =='아동(18세미만)':
    locations.append(row)
locations = sorted(locations, key=lambda x: x[1])
for l in locations:
  wdr.writerow(l)
  # if line[1].split()[1] == '00:00':
  #   index = 0
  #   # api 요청 파라미터 값
  #   parameters = {
  #     'startDt': '20200120',
  #     'startHh': '00',
  #     'endDt': '20200120',
  #     'endHh':'23',
  #     'stnIds': '119',
  #   }
  #   ## 시간 처리
  #   dates = line[1].split()
  #   parameters['startDt'] = dates[0].replace('-','')
  #   parameters['endDt'] = dates[0].replace('-','')

  #   # 요청 URL
  #   Url = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList?serviceKey='+apiKey+'&numOfRows=24&pageNo=1&dataType=JSON&dataCd=ASOS&dateCd=HR'
  #   Url += '&startDt='+parameters['startDt']+'&startHh='+parameters['startHh']+'&endDt='+parameters['endDt']+'&endHh='+parameters['endHh']+'&stnIds='+parameters['stnIds']
    
  #   l = requests.get(Url)
  #   result = {}
  #   try:
  #     weather_data = dict(l.json())['response']['body']['items']['item']
  #   except:
  #     miss_count += 1
  # if weather_data:
  #   weather = weather_data.pop(0)
  #   row = line + [weather['ta'], weather['rn'], weather['ws'], weather['hm'], weather['ss'], weather['icsr']]
  #   wdr.writerow(row)
  
  # count += 1
  # if count % 430 == 0:
  #   print((count/430),'%', miss_count)


