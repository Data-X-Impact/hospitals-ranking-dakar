# -*- coding: utf-8 -*-

#%% load packages and set options
from selenium import webdriver
#from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support.expected_conditions import presence_of_element_located
#from selenium.common.exceptions import NoSuchElementException
import time
#import string
#import openpyxl
#import os
import pandas as pd

#options to store long strings in pandas dataframe
pd.options.display.max_colwidth=100000

#%% lauch driver 
print("Hello World")
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 5)

#%% opening google maps
# Opening Google maps
driver.get("https://www.google.com/maps")
time.sleep(3)

#%% closing cookies button
# Closing the google consent form
#widget = driver.find_element_by_tag_name("iframe")
#driver.switch_to_frame(widget)
#div_button = driver.find_element_by_class_name("VfPpkd-dgl2Hf-ppHlrf-sM5MNb")
button_xpath='//button[contains(@aria-label,"Accepter l\'utilisation de cookies")]'
button = driver.find_element_by_xpath(button_xpath)
button.click()

#%% search hospitals on google maps
# Finding the search box
#driver.switch_to_default_content()
searchinput_xpath='//input[@id="searchboxinput"]'
searchbox = driver.find_element_by_xpath(searchinput_xpath)
location = "Dakar"
searchbox.send_keys(location)
searchbox.send_keys(Keys.ENTER)
time.sleep(2)
cancelsearch_xpath='//a[@class="gsst_a"]'
cancelbut = driver.find_element_by_xpath(cancelsearch_xpath)
cancelbut.click()
searchbox.send_keys("Hopitaux dakar") # or search hôpitaux dakar instead
searchbox.send_keys(Keys.ENTER)
time.sleep(3)

#%% search & collect strategy
#list all the hospitals found with the google search and store their info
#then search hospital by hospital and directly go through the reviews and the ratings


#%% useful functions
def next_page():
    #move onto the next page
    #nextpage_xpath='//button[contains(@aria-label,"Page suivante")]'
    nextpage_xpath='//button[@jsaction="pane.paginationSection.nextPage"]'
    button = driver.find_element_by_xpath(nextpage_xpath)
    button.click()
    
def scroll_pages_to_collect():
    #collect pages by scrolling to display all hospitals links
    #identify scroll button
    #siAUzd-neVct section-scrollbox cYB2Ge-oHo7ed cYB2Ge-ti6hGc siAUzd-neVct-Q3DXx-BvBYQ
    #siAUzd-neVct section-scrollbox cYB2Ge-oHo7ed cYB2Ge-ti6hGc siAUzd-neVct-Q3DXx-BvBYQ siAUzd-neVct-YbohUe-bnBfGc
    scrollable_div=driver.find_element_by_xpath('//div[(contains(@class,"siAUzd-neVct section-scrollbox cYB2Ge-oHo7ed cYB2Ge-ti6hGc siAUzd-neVct-Q3DXx-BvBYQ") and contains(@aria-label,"Résultats pour "))]')
    #scrollable_div=driver.find_element_by_css_selector('div.siAUzd-neVct.section-scrollbox.cYB2Ge-oHo7ed.cYB2Ge-ti6hGc.siAUzd-neVct-Q3DXx-BvBYQ')
    #scrollable_div.send_keys(Keys.PAGE_DOWN)
    #apply the scrolling as much times to read all
    i=10 # adjustable depending on the number of links found
    while(i>0):
        #driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        scrollable_div.send_keys(Keys.PAGE_DOWN)
        time.sleep(3) #adjustable depending on your network speed
        i-=1
    
#%% useful functions

def collect_pages():
    # collect the hospitals displayed
    #☺results_div='//div[@class="MVVflb-haAclf V0h1Ob-haAclf-d6wfac MVVflb-haAclf-uxVfW-hSRGPd"]'
    results_a='//a[@class="a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd"]'
    entries = driver.find_elements_by_xpath(results_a)
    print("pages collected: ",len(entries))
    
    hospitals_master = pd.DataFrame(data=entries,columns=['entry'])
    hospitals_master['hospital'] = hospitals_master['entry'].map(lambda x: x.get_attribute("aria-label"))
    hospitals_master['link'] = hospitals_master['entry'].map(lambda x: x.get_attribute("href"))
    hospitals_master=hospitals_master.drop(columns=['entry'])
    
    return hospitals_master

#%% collect all the pages (or the first 10 result panel) from the search results
hospitals_links=pd.DataFrame(data=[],columns=['hospital','link'])
nb_pages=10
while nb_pages>0:
    #collect pages by scrolling to display all hospitals links
    scroll_pages_to_collect()
    hospitals_links=hospitals_links.append(collect_pages(),ignore_index=True)
    #go the next page and repeat the process
    nb_pages-=1
    if nb_pages != 0:
        try:
            next_page()
        except:
            print("no more pages available")
            break
print("total pages collected: ", hospitals_links.shape[0])

#%% export hospitals links if needed
hospitals_links.to_csv("hospitals_links.csv",
                sep=";",
                encoding="utf-8",
                index=False)

#%% load hospitals links if needed
#hospitals_links=pd.read_csv('hospitals_links.csv',sep=";") 

#%%collect reviews page by page

#%% function to open hospitals pages
def open_page(this_page,metadata=True):
    #♥ now given a open page of a hospital how to get the reviews.
    driver.get(this_page)
    time.sleep(3)
    #collect adress
    temp='//button[contains(@data-item-id,"address")]'
    location=driver.find_element_by_xpath(temp).get_attribute('aria-label')
    
    #button to click to display all the reviews
    #button_xpath='//button[(@class="widget-pane-link" and @jsaction="pane.rating.moreReviews")]'
    try:
        button_xpath='//button[@jsaction="pane.rating.moreReviews"]'
        button = driver.find_element_by_xpath(button_xpath)
        button.click()
    except:
        print("no extended search")
        
    ratings=driver.find_element_by_xpath('//div[@class="gm2-display-2"]').text
    total_reviews=driver.find_element_by_xpath('//div[@class="gm2-caption"]').text
    print("ratings: ",ratings,"\ntotal reviews: ", total_reviews, "\n location :",location)
    
    if metadata:
        return pd.DataFrame(data={'link':[this_page],
                                  'ratings':[ratings],
                                  'total_reviews':[total_reviews],
                                  'location':[location]})

#this_page=hospitals_links["link"][3]
#metadata=open_page(this_page)

#%% function to scroll down to display all reviews
def scroll_reviews_to_collect(max_iteration=10):
    #scroll to display all the reviews
    try:
        xpath1='//div[@class="siAUzd-neVct section-scrollbox cYB2Ge-oHo7ed cYB2Ge-ti6hGc"]'
        scrollable_div=driver.find_element_by_xpath(xpath1)
    except:
        xpath2='//div[@jsan="t-dgE5uNmzjiE,7.siAUzd-neVct,7.section-scrollbox,7.cYB2Ge-oHo7ed,7.cYB2Ge-ti6hGc,0.tabindex"]'
        scrollable_div=driver.find_element_by_xpath(xpath2)
    scrollable_div.send_keys(Keys.PAGE_DOWN)
    #apply the scrolling as much times to read all
    i=max_iteration
    while(i>0):
        #driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        scrollable_div.send_keys(Keys.PAGE_DOWN)
        time.sleep(3) # waiting time to adjust depending on yr network speed
        i-=1
        
#max_iteration=int(metadata['total_reviews'][0].split()[0])


#%% reviews collection function
def collect_reviews_n_ratings():
    #expand shortened reviews
    button_xpath='//button[(@class="ODSEW-KoToPc-ShBeI gXqMYb-hSRGPd" and @jsaction="pane.review.expandReview")]'
    buttons = driver.find_elements_by_xpath(button_xpath)
    for button in buttons:
        button.click()
        time.sleep(1)
    
    #collect reviews and ratings
    reviews_xpath='//span[@class="ODSEW-ShBeI-text"]'
    ratings=driver.find_elements_by_xpath('//span[(@class="ODSEW-ShBeI-H1e3jb" and @role="img")]')
    reviews=driver.find_elements_by_xpath(reviews_xpath)
    
    df = pd.DataFrame(data=ratings,columns=['ratings'])
    df['reviews']=reviews
    df['rating'] = df['ratings'].map(lambda x: x.get_attribute("aria-label"))
    df['review'] = df['reviews'].map(lambda x: x.text)
    df=df.drop(columns=['ratings','reviews'])
    
    print("reviews collected: ",len(reviews),"\nratings collected: ",len(ratings))
    
    return df

#%% collect reviews page by page

final_df=pd.DataFrame(data=[],columns=['hospital','link',
                                       'ratings','total_reviews','location',
                                       'rating','review'])
for page in hospitals_links['link']: #[hospitals_links['link'][3]]:
    
    try:
        metadata = open_page(page)
    except:
        print("failed to identify reviews")
    
    try:
        max_iteration=int(metadata['total_reviews'][0].split()[0])
    except:
        max_iteration=50
    
    try:
        scroll_reviews_to_collect(max_iteration=max_iteration)
    except:
        print("scrollable div not found, default to initial display")
    
    try:
        df=collect_reviews_n_ratings()
    
        #adding others columns
        df['ratings']=metadata['ratings'][0]
        df['total_reviews']=metadata['total_reviews'][0]
        df['location']=metadata['location'][0]
        df['link']=page
        selection=hospitals_links[hospitals_links['link']==page].reset_index()
        df['hospital']=selection['hospital'][0]
        df=df[['hospital','link','ratings','total_reviews','location',
               'rating','review']]
        
        final_df=final_df.append(df,ignore_index=True)
    except:
        print("unable to collect reviews")
        selection=hospitals_links[hospitals_links['link']==page].reset_index()
        df=pd.DataFrame(data=[selection['hospital'][0],page,'','','','','']).transpose()
        df.columns=['hospital','link','ratings','total_reviews','location','rating','review']
        final_df=final_df.append(df,ignore_index=True)
        
    

#%% export the result
final_df.to_csv("hospitals_reviews.csv",
                sep=";",
                encoding="utf-8",
                index=False)
   


#%% end