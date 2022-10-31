#!/usr/bin/env python
# coding: utf-8

import time
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": featured_image(browser),
        "facts_table": mars_facts(),
        "hemisphere": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


# # NASA Mars News
def mars_news(browser):
    nasaURL = 'https://redplanetscience.com/'
    browser.visit(nasaURL)

    time.sleep(1)

    html = browser.html

    nasaSoup = bs(html, 'html.parser')
    try:
        newsTitle = nasaSoup.find('div', class_='content_title').get_text()
        newsP = nasaSoup.find('div', class_='article_teaser_body').text
    except AttributeError:
        return None, None
    return newsTitle, newsP



# # JPL Mars Space Images—Featured Image
# use splinter module to visit Nasa's JPL Mars Space url
def featured_image(browser):
    jplNasaURL = 'https://spaceimages-mars.com/'
    browser.visit(jplNasaURL)

    html = browser.html
    soup = bs(html, "html.parser")

    try:
        img = [i.get("src") for i in soup.find_all("img", class_="headerimage fade-in")]
    except AttributeError:
        return None
    return img

    # featured_image_url = jplNasaURL + img[0]
    # featured_image_url

    # featured_image_url='https://spaceimages-mars.com//image/featured/mars1.jpg'


# # Mars Facts
# URL link for mars facts
def mars_facts():
    marsURL = 'https://galaxyfacts-mars.com/'

    try:
        # locate the table from the mars facts
        facts_table = pd.read_html(marsURL)[0]
    except AttributeError:
        return None
    
    #set table header and index
    facts_table.columns = facts_table.iloc[0]
    facts_table = facts_table.iloc[1: , :]
    facts_table.set_index('Mars - Earth Comparison',inplace=True)
    
    # facts_table_html=facts_table.to_html()

    return facts_table.to_html(classes="table table-striped")


# # Mars Hemispheres
def hemispheres(browser):
    url = "https://marshemispheres.com/"
    browser.visit(url)

    hemisphere_image_urls = []

    for i in range(4):
        html = browser.html
        soup = bs(html, "html.parser")
        
        title = soup.find_all("h3")[i].get_text()
        browser.find_by_tag('h3')[i].click()
        
        html = browser.html
        soup = bs(html, "html.parser")
        
        img_url = soup.find("img", class_="wide-image")["src"]
        
        hemisphere_image_urls.append({
            "title": title,
            "img_url": "https://marshemispheres.com/" + img_url
        })
        browser.back()

    return hemisphere_image_urls


# marsData = [{
#         'news_title': newsTitle,
#         'news_p': newsP,
#         'featured_image_url': featured_image_url,
#         'facts_table': facts_table_html,
#         'hemisphere_image_urls' : hemisphere_image_urls
#     }]


# # In[17]:


# marsData

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
