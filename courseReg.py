#! /usr/bin/env python2.7

# Course Registration Status Checker

#Designed for NEU Schedualing banner

# How To Use
#     python class2.py [CRN]

#Semester to lookup courses for 
#	In Format YYYYMM, where MM is the first month after the start of the semester
SEMESTER = '201710'

#Email To
#	Address to which you want alert emails sent
SEND_TO = "sent_to@email.com"

#Email From
#	Address and corresponding SMTP server to use for outgoing mail
SEND_FROM = "send_from@email.com" 
SMTP_SERVER = "smtp.email.com" # enter your real SMTP!
SMTP_PORT = 587
SMTP_CRED = "creds.txt" #File containing your password, encoded in base64





import urllib2
from io import StringIO
import sys
import datetime

def sendAlert(title,alert):
	import smtplib
	import base64

	sender = SEND_FROM
	receivers = [SEND_TO]

	message = """From: Course Info<"""+SEND_FROM+""">
To: You <"""+SEND_TO+""">
Subject: Class Registration Info
"""
	message = message + "The course you are interested in:\n"+title+"\n\nStatus: "+alert+"\n\nTo stop the CRON job enter \n\t\"crontab -e\" and delete the line including course2.py"

	try:
		smtpObj = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
		#smtpObj.set_debuglevel(1)
		smtpObj.ehlo()
		smtpObj.starttls()
                smtpObj.ehlo()
		smtpObj.login(SEND_FROM,base64.b64decode(open(SMTP_CRED).read()))
		smtpObj.sendmail(sender, receivers, message)         
		print "Successfully sent email"
	except smtplib.SMTPException:
		print "Error: unable to send email"

def strToItt(foo):
	stri = StringIO(foo)
	while True:
		nl = stri.readline()
		if nl == '': break
		yield nl.strip('\n')

def checkCourse(crn):
	url = 'https://wl11gp.neu.edu/udcprod8/NEUCLSS.p_class_search?sel_day=dummy&STU_TERM_IN='+SEMESTER+'&sel_subj=dummy&sel_attr=dummy&sel_schd=dummy&sel_camp=dummy&sel_insm=dummy&sel_ptrm=dummy&sel_levl=dummy&sel_instr=dummy&sel_seat=dummy&p_msg_code=UNSECURED&sel_crn='+crn+'&sel_subj=&sel_crse=&sel_title=&sel_attr=&sel_levl=&sel_schd=&sel_insm=&sel_from_cred=&sel_to_cred=&sel_camp=&sel_ptrm=&sel_instr=&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a'

	response =  urllib2.urlopen(url)
	html = response.read().decode('utf-8')
	try:
		table = (html.split("<CAPTION class=\"captiontext\">Scheduled Meeting Times</CAPTION>")[1]).split("</TABLE>")[0]
	except:
		print "Invalid CRN"
		return
	headers=(((table.split("<TR>")[1]).strip()).rstrip("</TR>")).strip()
	data = (((table.split("<TR>")[2]).strip()).rstrip("</TR>")).strip()

	title = ((html.split("ddtitle\" scope=\"colgroup\" >")[1]).split(">")[1]).split("<")[0]
	print (title)
	header_list = list()
	data_list = list()
	for i in strToItt(headers):
		header_list.append((i.split("</TH>")[0].split(">")[1]))
	for k in strToItt(data):
		data_list.append((k.split("<")[1].split(">")[1]))
	if len(header_list) != len (data_list):
		raise ValueError ("Mismatched row lengths")
	value_dict = dict(zip(header_list, data_list))
	#print (value_dict)
	#print (value_dict.get("Actual"),"/",value_dict.get("Capacity"))
	status="Null"
	
	if int(value_dict.get("Actual")) < int(value_dict.get("Capacity")):
		status="Seats Available! "
		verbose_status = status+" ("+value_dict.get("Actual")+"/"+value_dict.get("Capacity")+")"
		sendAlert(title,verbose_status)
	elif int(value_dict.get("Actual")) >= int(value_dict.get("Capacity")):
		status="Full"
		verbose_status = status+" ("+value_dict.get("Actual")+"/"+value_dict.get("Capacity")+")"
		#sendAlert(title,verbose_status)
	with open("/Users/Student/cpuglia/www/course.log", "a") as myfile:
		myfile.write('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())+" == "+title+" == "+verbose_status+"\n")
	print verbose_status

#print len(sys.argv)	
if len(sys.argv) < 2:
	print "Please run with CRN as an argument"
else:
	checkCourse(sys.argv[1])
