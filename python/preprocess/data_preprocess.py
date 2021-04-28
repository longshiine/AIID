import csv
import math
import matplotlib.pyplot as plt
import requests
import json

sil = []
f = open('data/data.csv', 'r', encoding='utf-8')
ff = open('data/new.csv', 'w', encoding='utf-8')
rdr = csv.reader(f)
ty = []
wdr = csv.writer(ff)
for idx,line in enumerate(rdr):
  if len(line[6].split()) > 2:
    row = []
    r = requests.get('http://apis.vworld.kr/new2coord.do?q='+line[6]+'&apiKey=767B7ADF-10BA-3D86-AB7E-02816B5B92E9&domain=http://map.vworld.kr/&output=json')
    result = dict(r.json())
    if len(result) == 1:
      r = requests.get('http://apis.vworld.kr/jibun2coord.do?q='+line[6]+'&apiKey=767B7ADF-10BA-3D86-AB7E-02816B5B92E9&domain=http://map.vworld.kr/&output=json')
      result = dict(r.json())
      if len(result) == 1:
        row = [0,0,0]
        print("fuck")
      else:
        row = [result['JUSO'], result['EPSG_4326_X'], result['EPSG_4326_Y']]
        print(row)
    else:
      row = [result['JUSO'], result['EPSG_4326_X'], result['EPSG_4326_Y']]
      print(row)
    # row = []
    # if idx == 0:
      #row = ['신고대상','발생월(sin)','발생월(cos)','발생시간(sin)','발생시간(cos)','발생지 주소','거주지 주소','발생동기','성별','실종나이','강수형태','하늘상태','기온','습도']
    #   row = ['Target', 'Month(sin)', 'Month(cos)', 'Time(sin)', 'Time(cos)', 'Location','Type', 'Sex', 'Age', 'Rain', 'Sky', 'Temperature', 'Humidity']
    # if idx != 0:
      # 1.신고대상
      # 아동: 1, 치매질환자: 2, 지적장애인(18세미만): 3, 지적장애인(18세이상): 4
      # if line[0] == "아동(18세미만)":
      #   row.append(1)
      # elif line[0] == "지적장애인(18세미만)":
      #   row.append(2)
      # elif line[0] == "지적장애인(18세이상)":
      #   row.append(3)
      # elif line[0] == "치매질환자":
      #   row.append(4)
  
      # 2.발생월_sin, 발생월_cos, 발생시간_sin, 발생시간_cos
      # date = line[1].split('-')
      # month_sin = math.sin(float(date[1])/12 * math.pi)
      # month_cos = math.cos(float(date[1])/12 * math.pi)
      # time_sin = math.sin(float(date[2].split()[1].split(':')[0])/24 * math.pi)
      # time_cos = math.cos(float(date[2].split()[1].split(':')[0])/24 * math.pi)
      # row.append(month_sin)
      # row.append(month_cos)
      # row.append(time_sin)
      # row.append(time_cos)

      # 3.발생지 주소, 거주지 주소
      #동선동 = 1, 삼선동 = 2, 성북동 = 3
      # if line[2] == "동선동":
      #   row.append(1)
      # elif line[2] == "삼선동":
      #   row.append(2)
      # elif line[2] == "성북동":
      #   row.append(3)
      
      # if line[3] == "동선동":
      #   row.append(1)
      # elif line[3] == "삼선동":
      #   row.append(2)
      # elif line[3] == "성북동":
      #   row.append(3)
      # ty.append(line[5])
      # 4.발생동기
      # if line[5] == "치매":
      #   row.append(1)
      # elif line[5] == "정신질환":
      #   row.append(2)
      # elif line[5] == "가정문제":
      #   row.append(3)
      # elif line[5] == "상습가출":
      #   row.append(4)
      # elif line[5] == "교우관계":
      #   row.append(5)
      # elif line[5] == "보호자이탈":
      #   row.append(6)
      # elif line[5] == "이성문제":
      #   row.append(7)
      # elif line[5] == "진학관계":
      #   row.append(8)
      # elif line[5] == "유기":
      #   row.append(9)
      # elif line[5] == "구직관계":
      #   row.append(10)
      # elif line[5] == "자살(의심)":
      #   row.append(11)
      # elif line[5] == "납치":
      #   row.append(12)
      # elif line[5] == "종교":
      #   row.append(13)
      # elif line[5] == "유인":
      #   row.append(14)
      # elif line[5] == "기타":
      #   row.append(15)
      # if line[5] == "치매":
      #   row.append([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
      # elif line[5] == "정신질환":
      #   row.append([0,1,0,0,0,0,0,0,0,0,0,0,0,0,0])
      # elif line[5] == "가정문제":
      #   row.append([0,0,1,0,0,0,0,0,0,0,0,0,0,0,0])
      # elif line[5] == "상습가출":
      #   row.append([0,0,0,1,0,0,0,0,0,0,0,0,0,0,0])
      # elif line[5] == "교우관계":
      #   row.append([0,0,0,0,1,0,0,0,0,0,0,0,0,0,0])
      # elif line[5] == "보호자이탈":
      #   row.append([0,0,0,0,0,1,0,0,0,0,0,0,0,0,0])
      # elif line[5] == "이성문제":
      #   row.append([0,0,0,0,0,0,1,0,0,0,0,0,0,0,0])
      # elif line[5] == "진학관계":
      #   row.append([0,0,0,0,0,0,0,1,0,0,0,0,0,0,0])
      # elif line[5] == "유기":
      #   row.append([0,0,0,0,0,0,0,0,1,0,0,0,0,0,0])
      # elif line[5] == "구직관계":
      #   row.append([0,0,0,0,0,0,0,0,0,1,0,0,0,0,0])
      # elif line[5] == "자살(의심)":
      #   row.append([0,0,0,0,0,0,0,0,0,0,1,0,0,0,0])
      # elif line[5] == "납치":
      #   row.append([0,0,0,0,0,0,0,0,0,0,0,1,0,0,0])
      # elif line[5] == "종교":
      #   row.append([0,0,0,0,0,0,0,0,0,0,0,0,1,0,0])
      # elif line[5] == "유인":
      #   row.append([0,0,0,0,0,0,0,0,0,0,0,0,0,1,0])
      # elif line[5] == "기타":
      #   row.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
    
      # 5.성별
      # if line[6] == "남자":
      #   row.append(0) 
      # elif line[6] == "여자":
      #   row.append(1)

      # 6.실종나이,'강수형태','하늘상태','기온','습도'
      # row += line[7:]

    wdr.writerow(row)
      # sil.append(location)
      # if len(location) > 1 and location[0] == "서울특별시":
      #   print(location)
# sil_set = set(sil)
# sil_list = list(sil_set)
# sil_counting = get_occurrence_count(sil)
# for sil in sil_counting:
#   if sil_counting[sil] > 200:
#     print("주소: ", sil)
#     print("실종발생건수: ", sil_counting[sil])

# def get_occurrence_count(my_list):
#   new_list = {}
#   for i in my_list:
#     try: new_list[i] += 1
#     except: new_list[i] = 1
#   return(new_list)
# gu_counting = get_occurrence_count(ty)
# print(gu_counting)