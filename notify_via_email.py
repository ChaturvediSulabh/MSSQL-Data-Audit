###### Notify #########
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_report():
    dir_path = "/tmp/"
    files = ["MOTOPOLL_EVENTS_PER_CUSTOMER_LAST24HOURS.csv", "ALL_NOC_EVENTS_PER_CUSTOMER_LAST24HOURS.csv", "SNMP_PROBE_OPERATING_STATUS.csv", "SYSLOG_PROBE_OPERATING_STATUS.csv"]

    msg = MIMEMultipart()
    msg['To'] = "sdonetcoolteam@extremenetworks.com"
    msg['From'] = "PRODUCTION NETCOOL"
    msg['Subject'] = "EVENT STATISTICS DATA SHEETS - Daily Audits"

    body = MIMEText('Please see attached Daily audit event management datasheets', 'html', 'utf-8')
    msg.attach(body)  # add message body (text or html)

    for f in files:  # add files to the message
        file_path = os.path.join(dir_path, f)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition','attachment', filename=f)
        msg.attach(attachment)

    s = smtplib.SMTP()
    s.connect(host='mailhost')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.close()
send_report()
