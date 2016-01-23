import requests
from requests.auth import HTTPBasicAuth
def getLoad(host):
	pattern_load_avg = re.compile(r'load average: (.*), (.*), (.*)')
	try:
		r = requests.get("http://monitoring.example.com/nagios/cgi-bin/status-json.cgi?host=" + host, auth=HTTPBasicAuth(username,password))
		data = re.search(pattern_load_avg,r.content)
		load = data.group().split(":")[1].split(",")[0]
		load = round(float(load))
		return load
	except:
		load = 0
		return load
