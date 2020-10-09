from bs4 import BeautifulSoup
import ssl
from urllib import request, parse
import json
import datetime as DT

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

today = DT.date.today()

venues = [
	# {'name': 'fine_yueliangwan', 'filename': '378.csv', 'partnerid': 378, 'shopid': '42'},
	# {'name': 'fine_changshoulu', 'filename': '379.csv', 'partnerid': 379, 'shopid': '36'},
	# {'name': 'fine_889', 'filename': '380.csv', 'partnerid': 380, 'shopid': '41'},
	# {'name': 'fine_xintiandi', 'filename': '381.csv', 'partnerid': 381, 'shopid': '39'},
	# {'name': 'fine_xinggeng', 'filename': '382.csv', 'partnerid': 382, 'shopid': '63'},
	# {'name': 'fine_caoyanglu', 'filename': '376.csv', 'partnerid': 376, 'shopid': '37'},
	# {'name': 'fine_shangchenglu', 'filename': '377.csv', 'partnerid': 377, 'shopid': '38'},
	{'name': 'fine_meiluocheng', 'filename': '388.csv', 'partnerid': 388, 'shopid': '34'}
]

url = 'https://api.fineyoga.com/hall/course/index/course-plan/list'

for index in range(len(venues)):
	filename = venues[index]['filename']
	f = open(filename, "w")
	headers = "title_en, title_cn, day_num, start_time, end_time, bookable\n"
	f.write(headers)

	for day_num in range(7):
		date = today + DT.timedelta(days=day_num)
		data = {
			"hall_id": venues[index]['shopid'],
			"date": f'{date}',
			"page": 1,
			"size": 20
		}
		data = parse.urlencode(data).encode()
		req =  request.Request(url, data=data)
		res = request.urlopen(req).read()
		activities = json.loads(res).get("pagination").get("data")
		for activity in activities:
			title_en = activity.get("course_name_en")
			title_cn = activity.get("course_name")
			start_time = activity.get("start_time")
			end_time = activity.get("end_time")
			booked_num = activity.get("has_order")
			total_num = activity.get("max_order")
			if (booked_num < total_num):
				bookable = True
			else:
				bookable = False
			f.write(str(title_en) + "," + str(title_cn) + "," + str(day_num) + "," + str(start_time) + "," + str(end_time) + "," + str(bookable) + "\n")

	f.close()