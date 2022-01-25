import pickle
from datetime import datetime
import pytz

s = pickle.load(open('G:/HIMYM/django_project101 - Copy/pickles/instances_26.p','rb'))
x = s[0]
print(s[:5])
