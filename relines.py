#!/usr/bin/python
from os import remove
from shutil import copy
def reline(filename,filename2,spstring,string1,string2):
    f = open(filename2)
    fw = open(filename,'w+')
    for line in f.readlines():
        if line.startswith(string1):
            listf = line.split(spstring)
            listf[1] = string2
            print listf[0] + ' ' + spstring + ' ' + listf[1]
            fw.write(listf[0] + ' ' + spstring + ' ' + listf[1]+'\n')
        else:
            fw.write(line)

reline("/tmp/config2.php","/var/www/example/application/config/config.php","=","$config['base_url']","'http://127.0.0.1';")
reline("/tmp/config.php","/tmp/config2.php","=","$config['cookie_domain']","'';")
reline("/tmp/constants2.php","/var/www/example/application/config/constants.php",",","define('CDN_URL'","'http://127.0.0.1');")
reline("/tmp/constants1.php","/tmp/constants2.php",",","define('DOC_ROOT'","'/var/www/example/');")
reline("/tmp/constants.php","/tmp/constants1.php",",","define('IMAGICK_LIBRARY_PATH'","'/usr/bin/');")
reline("/tmp/database.php","/var/www/example/application/config/database.php","=>","	'password'","'ehya',")


rmlist = ["/tmp/config2.php","/tmp/constants2.php","/tmp/constants1.php"]
for rfile in rmlist:
    try:
        remove(rfile)
    except:
       pass


flist = ["/tmp/config.php","/tmp/constants.php","/tmp/database.php"]
for f in flist:
    try:
       copy(f,"/var/www/example/application/config/")
    except:
       pass

