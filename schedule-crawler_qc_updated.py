from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen
import json
import datetime as DT

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

today = DT.date.today()
day_num = 0

venues = [
	{'name': 'mysoul', 'filename': '19.csv', 'partnerid': 19},
	{'name': 'justyoga_xuhui', 'filename': '63.csv', 'partnerid': 63},
	{'name': 'thebarre', 'filename': '101.csv', 'partnerid': 101},
	{'name': 'freesoul', 'filename': '62.csv', 'partnerid': 62},
	{'name': 'infinitymotion', 'filename': '347.csv', 'partnerid': 347}
]

for index in range(len(venues)):
	filename = venues[index]['filename']
	f = open(filename, "w")
	headers = "title_en, title_cn, day_num, start_time, end_time, bookable\n"
	f.write(headers)

	for day_num in range(7):
		date = today + DT.timedelta(days=day_num)
		if (venues[index]['partnerid'] == 19):
			url = f'https://yun.qingchengfit.cn/api/mobile/schedules/group/?shop_id=49220&date={date}'
		elif (venues[index]['partnerid'] == 63):
			url = f'https://yun.qingchengfit.cn/api/mobile/schedules/group/?shop_id=38149&date={date}'
		elif (venues[index]['partnerid'] == 101):
			url = f'https://yun.qingchengfit.cn/api/mobile/schedules/group/?shop_id=28444&date={date}'
		elif (venues[index]['partnerid'] == 62):
			url = f'https://yun.qingchengfit.cn/api/mobile/schedules/group/?shop_id=39431&date={date}'
		elif (venues[index]['partnerid'] == 347):
			url = f'https://yun.qingchengfit.cn/api/mobile/schedules/group/?shop_id=64898&date={date}'

		res = urlopen(url).read()
		contents = json.loads(res).get("data").get("schedules")

		for content in contents:
			title_en = content.get("course").get("name").lstrip('*')
			title_cn = title_en
			start_time = content.get("start").split('T')[1]
			end_time = content.get("end").split('T')[1]
			if (content.get("current_max_capacity") == 0):
				bookable = False
			else:
				bookable = True
			f.write(title_en + "," + title_cn + "," + str(day_num) + "," + start_time + "," + end_time + "," + str(bookable) + "\n")

	f.close()
