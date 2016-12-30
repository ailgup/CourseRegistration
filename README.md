# Course Registration
Python script that checks the seat availability of courses at Northeastern University, can be run as a CRON to send an email alert user to when a seat in a class becomes available.

This script runs best on a Linux server, or an other always-on environment. University servers (eg. COE Linux) are a great place to run it, if you have the permissions. Otherwise a service such as Heroku would work.

### Usage

The script runs on Python 2.x using the following syntax

```python
python courseReg.py [CRN]
```
eg. If you wanted to know the status of Course# 15647
```python
$ python courseReg.py 15647
Professional Issues in Engineering - 15647 - EECE 3000 - 04- (Boston) - Credits 1
Full (19/19)
```
This shows you that the course is currently full, as the output is in the format (Students Registered,Total Seats)

**Note:** The program requires a file named by default ```certs.txt``` which contains your STMP password obviscurated with base64 encoding.

#### Setting up a CRON
Since you will likely want this script to run over the course of months while you wait for an opening to occour, we need to automate this process by creating a cron job.
- Navigate to the directory containing the script.
- Open the CRON editor
```bash
crontab -e
```
Then append the following to the top of the document.
This will run the script every other hour.
```
MAILTO=""
0 */2 * * * python /full/path/to/file/courseReg.py 12345
```
##### Killing the CRON
Well eventually you will want to kill this CRON since you either got into the class or don't care about it any more. In this case you will re-enter the crontab editor
```
crontab -e
```
Then delete the lines you added above and you will no longer be running the script!

### Modification

To use the program to it's fullest modify the following variables to work for you. They are located at the top of the program.

#### Semester
``` 
#	In Format YYYYMM, where MM is the first month after the start of the semester
SEMESTER = '201710'
```

#### Email To Address
```
#	Address to which you want alert emails sent
SEND_TO = "send_to@email.com"
```

#### Email From Address
```
#	Address and corresponding SMTP server to use for outgoing mail
SEND_FROM = "send_from@email.com"
SMTP_SERVER = "smtp.email.com"
SMTP_PORT = 587
SMTP_CRED = "creds.txt" #File containing your password, encoded in base64
```
##### SMTP_CRED
This file should be a single line only containing your password in base64.
To generate this file you can run the following simple command.
 ```
 $ echo mySuperSecretPassword | base64 >> creds.txt
 ```
 Where here your password would be : mySuperSecretPassword
