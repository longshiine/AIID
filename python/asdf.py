import csv
import requests

read_f = open('data/real_data.csv', 'r', encoding='utf-8')
write_f = open('data/new.csv', 'w', encoding='utf-8')
rdr = csv.reader(read_f)
wdr = csv.writer(write_f)
apiKey = '767B7ADF-10BA-3D86-AB7E-02816B5B92E9'

count = 0 # 진행상황 보기
percentage = 0 # 퍼센테이지

for idx,line in enumerate(rdr):
  # line의 구성: 대상구분, 성별, 나이, 관할관서, 접수관서, 접수일자, 주소, 실종(가출)경력, 주로 다니는 장소
  row = [line[1], line[5]]# 새로운 csv의 한줄
  if idx == 0: # 첫줄 입력
    row += ['주소'] + line[10:]
    wdr.writerow(row)
    continue
  # 주소 -> 좌표 변환코드(Geocoder사용)
  # 지번, 도로명 주소 둘다 제대로 있기만 하면 변환 가능
  # line[6] -> line[6] 주소, line[7] x좌표, line[8] y좌표
  # 주소에 대한 정보 없는 경우에는 -> 주소, 0, 0 --> 우선은 포함안시키겠음!
  if len(line[6].split()) > 3:
      JUSO = ""
      print(line[6])
      # 동/읍/면으로 필터링
      for idx, juso in enumerate(line[6].split()):
        if '도' in juso or '시' in juso or '군' in juso or '구' in juso or '동' in juso or '읍' in juso or '면' in  juso:
          if '(' in juso:
            JUSO += juso[1:-1] + " "
          else:
            JUSO += juso + " "
        else:
          continue
      row += [JUSO] + line[10:]
      print(row)
      wdr.writerow(row)
  # else:
  #   row += [line[6],0,0]
  count += 1
  if count % 200 == 0:
    percentage += 1
    print(percentage/10, "%")