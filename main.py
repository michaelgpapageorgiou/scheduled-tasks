# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.

import datetime, pandas
import random,smtplib,os

my_email=os.environ.get('MY_EMAIL')
password=os.environ.get('MY_PASSWORD')

now=datetime.datetime.now()
today_month=now.month
today_day=now.day
today=(today_day,today_month)
data=pandas.read_csv('birthdays.csv')
#birthdays_dict={(row.day,row.month):(row['name'],row.email,row.year,row.month,row.day) for (index,row) in data.iterrows()}
birthdays_dict={(row.day,row.month):row for (index,row) in data.iterrows()}
if today in birthdays_dict:
    the_special_one = birthdays_dict[today]
    with open(f'letter_templates/letter_{random.randint(1,3)}.txt','r') as letter:
        letter=letter.read()
        letter_ready=letter.replace('[NAME]',the_special_one['name'])
        print(letter_ready)
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(password=password,user=my_email)
        connection.sendmail(from_addr=my_email,to_addrs=the_special_one['email'],
                            msg=f'subject:Happy Birthday\n\n{letter_ready}')
        )
