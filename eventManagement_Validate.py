#!/usr/bin/python3
######## Python Logging ######################################################################
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s',filename='/var/log/ds3_ds3_FortinetArchiveCleanup.log',filemode='w')
##############################################################################################

####### Python MS SQL Server Connection ######################################################
import pymssql
conn = pymssql.connect(server='', user='', password='', database='')
cursor = conn.cursor()
##############################################################################################

###### Python Get Date Time now and 24 Hours Before #########################################
import time
year = (time.strftime('%Y'))
month = (time.strftime('%m'))
today = (time.strftime('%d'))
yesterday = int(today) - 1
if(yesterday < 10):
        yesterday = '0' + str(yesterday)
else:
        yesterday = str(yesterday)
from_date_time = year+month+yesterday
to_date_time = year+month+today

##### Other Python Modules needed for this program ###################################################################
import re
import os
############################################################################################

##### Python CSV Module #####################################################################
import csv
def genReport(row,fileName):
    with open(fileName,'a+') as csv_file:
        csv_file.write('\n'+row.strip("()"))
##############################################################################################

##### Get Data and write to CSV #############################################################
os.system(r'touch MOTOPOLL_EVENTS_PER_CUSTOMER_LAST24HOURS.csv ALL_NOC_EVENTS_PER_CUSTOMER_LAST24HOURS.csv SNMP_PROBE_OPERATING_STATUS.csv SYSLOG_PROBE_OPERATING_STATUS.csv')
with open('MOTOPOLL_EVENTS_PER_CUSTOMER_LAST24HOURS.csv','w') as file:
        defs = 'Number of MOTOPOLL OK EVENTS, Customer'
        file.write(defs)

with open('ALL_NOC_EVENTS_PER_CUSTOMER_LAST24HOURS.csv','w') as file:
	defs = 'Number of WLAN Events, Customer'
	file.write(defs)

with open('SNMP_PROBE_OPERATING_STATUS.csv','w') as file:
	defs = 'Number of Events processed between SNMP Probe and NCO Bridge, Probe Name'
	file.write(defs)

with open('SYSLOG_PROBE_OPERATING_STATUS.csv','w') as file:
	defs = 'Number of Events processed between SYSLOG Probe and NCO Bridge, Probe Name'
	file.write(defs)

cursor.execute("SELECT COUNT(*), Customer from REPORTER_STATUS where Summary in ('MOTOPOLL is OK') and FirstOccurrence between '"+from_date_time+"' and '"+to_date_time+"' GROUP BY Customer")
motopollEvs = cursor.fetchall()
for i in range(len(motopollEvs)):
    fileName = 'MOTOPOLL_EVENTS_PER_CUSTOMER_LAST24HOURS.csv'
    genReport(str(motopollEvs[i]),fileName)

cursor.execute("SELECT COUNT(*), Customer from REPORTER_STATUS where MSI_ServiceType = 'WLAN' and MSI_Displayed = 1 and FirstOccurrence between '"+from_date_time+"' and '"+to_date_time+"' GROUP BY Customer")
wlanEvs = cursor.fetchall()
for i in range(len(wlanEvs)):
    fileName = 'ALL_NOC_EVENTS_PER_CUSTOMER_LAST24HOURS.csv'
    genReport(str(wlanEvs[i]), fileName)

cursor.execute("SELECT COUNT(*), MSI_EvSource from REPORTER_STATUS where MSI_ServiceType = 'WLAN' and FirstOccurrence between '"+from_date_time+"' and '"+to_date_time+"' GROUP BY MSI_EvSource")
snmpEvs = cursor.fetchall()
for i in range(len(snmpEvs)):
    fileName = 'SNMP_PROBE_OPERATING_STATUS.csv'
    genReport(str(snmpEvs[i]), fileName)

cursor.execute("SELECT COUNT(*), MSI_EvSource from REPORTER_STATUS where MSI_ServiceType = 'SECURITY' and FirstOccurrence between '"+from_date_time+"' and '"+to_date_time+"' GROUP BY MSI_EvSource")
syslogEvs = cursor.fetchall()
for i in range(len(syslogEvs)):
    fileName = 'SYSLOG_PROBE_OPERATING_STATUS.csv'
    genReport(str(syslogEvs[i]), fileName)

conn.close()
