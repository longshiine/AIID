import csv
import math
import matplotlib.pyplot as plt
import requests
import json
import datetime

f = open('data/one_location.csv', 'r', encoding='utf-8')
ff = open('data/new.csv', 'w', encoding='utf-8')
rdr = csv.reader(f)
wdr = csv.writer(ff)

count = 0
miss_count = 0
weather_data= {}
index = 0
locations = []
for idx,line in enumerate(rdr):
  if idx == 0: # 첫줄 입력
    continue
  else:
    if line[1].split()[1] in (weather_data).keys():
      if line[0] == '1':
        weather_data[line[1].split()[1]] += 1
    else:
      if line[0] == '1':
        weather_data[line[1].split()[1]] = 1
      else:
        weather_data[line[1].split()[1]] = 0

print(weather_data)