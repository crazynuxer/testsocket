#!/usr/bin/python
import requests,os,smtplib,sys,multiprocessing,time,subprocess
from datetime import date, timedelta
from email.mime.text import MIMEText

def sendAlert(error):
   s = smtplib.SMTP('smtp.example.com')
   msg = MIMEText(""" %s  """ % error)
   sender = 'crazynuxer@example.com'
   recipients = ['crazynuxer@example.com']
   msg['Subject'] = "Error Masalah Download Log"
   msg['From'] = sender
   msg['To'] = ", ".join(recipients)
   s.sendmail(sender, recipients, msg.as_string())

def parseconf(logconf):
	ln = 0
	yesterday = date.today() - timedelta(1)      
	for line in open(logconf):
		ln += 1
		
		# exclude comment
		if line.lstrip().startswith('#'):
			continue
		cols = line.split('|')
		
		# check number of columns
		if len(cols) != 3:
			sys.stdout.write('Error at line ' + str(ln) + ' : Number of columns is not 4')
			sys.stdout.flush()
			continue
                url = 'http://log' + cols[0].strip(' ') + '/' + cols[1].strip(' ') + '/' + cols[0].strip(' ') + '.' + cols[2].strip('\n').strip(' ') + '-' + yesterday.strftime('%Y%m%d')
                urllist.append(url)
        			
	return

def check_size(url,filename):
    r = requests.head(url)
    size = r.headers['content-length']
    statinfo = os.stat(filename)
    if int(size) == int(statinfo.st_size) :
        print 'OK'
    else:
        print 'Masalah send email'
        error = 'File sudah berhasil didownload tapi file sizenya berbeda ada kemungkinan koneksi timeout ' + url
        sendAlert(error)
    return

def download_file(url):
    filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    try:
        r = requests.get(url, stream=True, timeout=3)
        p1 = subprocess.Popen(['/usr/bin/wget', url], stdout=subprocess.PIPE)
	# Run the command
	output = p1.communicate()[0]
        check_size(url,filename)
    except :
        print 'Error File Not Found '
        error = 'Gagal download file karena ga bisa konek ke server ' + url
        sendAlert(error)
        pass

    return 

def handle_queue(queue):
    while not queue.empty():
        url = queue.get()
        download_file(url)
    return

urllist = []
jobs = []
parseconf(sys.argv[2])
queue = multiprocessing.Queue()
max_proc = int(sys.argv[1])

for url in urllist:
    print url
    queue.put(url)


for i in xrange(max_proc):
    print i
    p = multiprocessing.Process(target=handle_queue, args=(queue,))
    jobs.append(p)
    p.start()

for j in jobs:
        j.join()
        print '%s.exitcode = %s' % (j.name, j.exitcode)
'''
## ## hostname | direktori | nama file 
server1 | log | file.logs
'''
