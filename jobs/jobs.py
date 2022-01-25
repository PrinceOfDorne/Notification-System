from blog.models import Query
from datetime import timedelta, datetime, time
import pickle
import os
import smtplib
import pytz
import sys
from dateutil.relativedelta import relativedelta

def checkifdeleted():
    folder = 'pickles/'
    if(len(os.listdir(folder)) == 0):
        return

    for file in os.listdir(folder):
    	i= file.split('_')[1]
    	i = int(i.split('.')[0])
    	if(len(Query.objects.filter(id = i)) == 0 or Query.objects.filter(id = i).first().approved == False):
        	os.remove(folder+file)
        	Query.objects.filter(id = i).first().schedule_created = 0
        	print(file,'removed')

def create_schedule():

    for query in Query.objects.all():
        #print(query.creator.email)              #Email of creator

        if(query.approved == True):
            if(query.schedule_created == 1):
                continue

            instances = []
            nextins = query.date_posted
            expiry = datetime.combine(query.expiry, time(0,0))
            while(nextins.replace(tzinfo=None) < expiry):
                if(query.frequency == 'hrs'):
                    nextins = nextins + timedelta(hours=int(query.nos))
                elif(query.frequency == 'days'):
                    delta = relativedelta(days=int(query.nos))
                    nextins = nextins + delta
                elif(query.frequency == 'months'):
                    delta = relativedelta(months=int(query.nos))
                    nextins = nextins + delta
                else:
                    delta = relativedelta(years=int(query.nos))
                    nextins = nextins + delta

                instances.append(nextins)
            query.schedule_created = 1
            query.save()
            print('query_schedule updated for',query.pk)


            dumping_site = 'pickles/instances_' + str(query.pk) + '.p'
            pickle.dump(instances, open(dumping_site,'wb'))
            print('DONE PICKLING!!! for Query:',str(query.pk))
  

def send_notification():
    folder = 'pickles/'
    files = os.listdir(folder)
        
    for file in files:
        infile = open(folder+file,'rb')
        schedule = pickle.load(infile)
        infile.close()

        #Add timezone to current time
        timezone = pytz.timezone("Asia/Kolkata")
        current_datetime = timezone.localize(datetime.now())

        if(schedule[0]>current_datetime):
            break

        for i in range(1,len(schedule)):
            if(schedule[i]>current_datetime):
                ID= file.split('_')[1]
                ID = int(ID.split('.')[0])
                print(ID, schedule[i])

                #Send the Mail
                query = Query.objects.filter(id=ID).first()
                email = query.creator.email
                App = query.Application
                Not = query.Notification
                created = query.created
                expiry = query.expiry

                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login("Mail", "Password")
                message = "REMINDER for " + Not + " of Application : " + App + " which is expiring on " + str(expiry)
                Subject = "LTI Notification System"
                message = 'Subject: {}\n\n{}'.format(Subject, message) 
                s.sendmail("Mail", email, message)
                s.quit()

                print("Email Notification has been sent successfully!!! for qeury:",str(query.pk))

                #Change the schedule
                schedule = schedule[i:]
                dumping_site = folder+file

                #Save the new schedule
                pickle.dump(schedule, open(dumping_site,'wb'))
                break

def schedule_api():

	checkifdeleted()
	create_schedule()    
	send_notification()