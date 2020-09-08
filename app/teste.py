import calendar
import datetime

mydate = datetime.datetime.now()
print(mydate.month)

c = calendar.Calendar()

for i in c.monthdatescalendar(2020,4):
    for i in i:
        print(i.day, i.month, i.year, i.weekday())