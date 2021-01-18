# gu = []
# f = open('data.csv', 'r', encoding='utf-8')
# rdr = csv.reader(f)
# for idx,line in enumerate(rdr):
#     if idx != 0:
#       location = line[6].split()[:2]
#       if len(location) > 1 and location[0] == "서울특별시":
#         gu.append(location[1])
      
# f.close()

# gu_set = set(gu)
# gu_list = list(gu_set)
def get_occurrence_count(my_list):
  new_list = {}
  for i in my_list:
    try: new_list[i] += 1
    except: new_list[i] = 1
  return(new_list)
# gu_counting = get_occurrence_count(gu)

# colorInfo = {}
# for l in gu_counting:
#   if gu_counting[l] > 1500:
#     colorInfo[l] = '#753B39'
#   elif gu_counting[l] > 1200:
#     colorInfo[l] = '#E03F3C'
#   elif gu_counting[l] > 900:
#     colorInfo[l] = '#F7A49B'
#   elif gu_counting[l] > 600:
#     colorInfo[l] = '#E3C4BD'
#   else:
#     colorInfo[l] = '#fff'

# print(gu_counting)
# print(colorInfo)
