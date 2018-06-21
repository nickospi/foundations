
# coding: utf-8

# In[837]:


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


# In[838]:


#for server use only
from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(800, 600))
display.start()

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(chrome_options=options)


# In[839]:


driver.get("https://www.bloomberg.com")


# In[840]:


Bloomberg_Now = []
#getting the main story panel and appending it on a dict
stories = driver.find_elements_by_class_name ("hub-main")
for story in stories:
    headlines = {}
    headline = story.find_element_by_class_name ("single-story-module__headline-link")
    headlines ['Headline'] = headline.text
    timestamp = story.find_element_by_class_name ("hub-timestamp")
    headlines['Timestamp'] = timestamp.text
    category = story.find_element_by_class_name ("single-story-module__eyebrow")
    headlines['Category'] = category.text   
    url = story.find_element_by_tag_name("a").get_attribute('href')
    headlines['Url'] = url
    try: 
        related = story.find_element_by_class_name ("single-story-module__related-stories")
        headlines ['Related'] = related.text
    except:
        pass
#getting the more stories panel and appending it on a dict
    Bloomberg_Now.append(headlines)
    more = {}
    more_stories = story.find_elements_by_tag_name('h3')
    summary = story.find_elements_by_class_name ('story-package-module__story__summary') 
    more['Story_Two'] = more_stories[0].text
    more['Summary'] = summary[0].text
    more['Story_Three'] = more_stories[1].text
    more['Summary'] = summary[1].text
    more['Story_Four'] = more_stories[2].text
    more['Summary'] = summary[2].text
    more['Story_Five'] = more_stories[3].text  
    more['Summary'] = summary[3].text
    markets = driver.find_element_by_class_name("navi-markets-bar")
    Bloomberg_Now.append(more)
#getting the markets panel and appending it on a separate dict
    finance = {}
    finance['Markets'] = markets.text
    Bloomberg_Now.append(finance)
Bloomberg_Now  


# In[848]:


#date for mail subject
import datetime
right_now = datetime.datetime.now()
date_string_attchmnt = right_now.strftime("%Y-%m-%d-%-I%p")
date_string = right_now.strftime("%-I%p")


# In[849]:


#saving to csv
import pandas as pd
import requests
df = pd.DataFrame(Bloomberg_Now)
df.to_csv("Bloomberg_Now.csv", index=False)


# In[850]:


requests.post(
        "https://api.mailgun.net/v3/sandboxd37dc184d2cf48f4aada515cae6f4695.mailgun.org/messages",
        auth=("api", "*****************************"),
        files=[("Bloomberg_Now {}".format(date_string_attchmnt), open("Bloomberg_Now.csv"))],
        data={"from": "NP <mailgun@sandboxd37dc184d2cf48f4aada515cae6f4695.mailgun.org>",
              "to": ["n******@gmail.com"],
              "subject": "Here is your {} briefing".format(date_string),
              "text": "Here is your briefing from Bloomberg"}) 

