import smtplib

# source : http://www.nixtutor.com/linux/send-mail-through-gmail-with-python/

fromaddr = 'fromuser@gmail.com'
toaddrs  = 'touser@gmail.com' #if more than one user use list  
msg = 'There was a terrible error that occured and I wanted you to know!'


# Credentials (if needed)
username = 'username'
password = 'password'

# The actual mail send
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
