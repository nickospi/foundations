
# coding: utf-8

# In[55]:

# API_KEY = API keys from darksky and mailgun
#getting api info >> all temp units are in Celsius
import requests
url = 'https://api.darksky.net/forecast/API_KEY/40.7128,-74.0060?units=si'
response = requests.get(url)
data_shr = response.json()
temp = data_shr ["currently"]["temperature"]
summary = data_shr ["currently"]["summary"]
hightemp = data_shr["daily"]["data"][0]["temperatureHigh"] 
for feeling in data_shr ["daily"]["data"]:
    if hightemp >= 36:
        feeling = 'super-hot'
    elif 35 >= hightemp >= 20:
        feeling = 'warm' 
    elif 20 > hightemp >= 10:
        feeling = 'rather cold'
    elif 9 >= hightemp >= 0:
        feeling = 'cold'
    else:
        feeling = 'freezing'
lowtemp = data_shr["daily"]["data"][0]["temperatureLow"]
precip_prob = data_shr["daily"]["data"][0]["precipProbability"]
if precip_prob > 0:
    rain = "Take your umbrella!"
else:
    rain = "It's not going to rain or snow today." 
#print ("Right now it is", temp,"degrees out and", summary,".Today will be",feeling,"with a high of",hightemp,"and a low of",lowtemp,".",rain)
#putting mail text in a variable
mail_text = "Right now it is {} degrees out and {}.Today will be {} with a high of {} and a low of {}.{}".format(temp, summary,feeling,hightemp,lowtemp,rain)
#date for mail subject
import datetime
right_now = datetime.datetime.now()
date_string = right_now.strftime("%B %d, %Y")
#setting up mailgun
requests.post(
        "https://api.mailgun.net/v3/sandboxd37dc184d2cf48f4aada515cae6f4695.mailgun.org/messages",
        auth=("api", "API_KEY"),
        data={"from": "Excited User <mailgun@sandboxd37dc184d2cf48f4aada515cae6f4695.mailgun.org>",
              "to": ["n*******@gmail.com"],
              "subject": ("8AM Weather forecast:", date_string),
              "text":mail_text}) 

