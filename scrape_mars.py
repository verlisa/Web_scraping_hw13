from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "./chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
  # Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # Define database and collection
    db = client.mars_db
    collection = db.items

    # Create empty dictionary for storing data

    mars_facts = {}

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')
    # NASA Mars News - title
    news_title = soup.find('div', class_='content_title').text.strip()
    mars_facts["title"] = news_title
    
    # NASA Mars News - paragraph
    news_p = soup.find('div', class_='rollover_description').text.strip()
    mars_facts["paragraph"] = news_p
    
    # JPL Mars Space Images - Featured Image - Use Splinter to find image 

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://www.jpl.nasa.gov/spaceimages/index.php?category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # image = soup.find_all('article', class_='carousel_item')
 
    time.sleep(2)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    browser.click_link_by_partial_text('.jpg')

    #Retrieve image url
    html=browser.html
    JPL_soup=BeautifulSoup(html,'html.parser')
    featured_mars_image = JPL_soup.find('img').get('src')

    # feat_img = (i["style"])
        
    mars_facts["featured_mars_image"] =  featured_mars_image
    

    # # Mars Weather -  latest Mars weather tweet
    # #Use Splinter to find tweet text 
   
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('div', class_="js-tweet-text-container").text.split()
    mars_facts["weather"] = mars_weather

    # Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    tables
    df = tables[0]
    df
    html_table = df.to_html()
    
    mars_facts["mars_facts"] = html_table

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_image_urls =[]
    titles = []

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    soup.find_all("h3")
    hemisphere_image_urls=[]
    hemisphere_titles=[]
    hemi_dict={'title':[],'img_url':[]}
    titles =soup.find_all('h3')
    for title in titles:
        y=title.get_text()
        val1=y.strip('Enhanced')
        browser.click_link_by_partial_text(y)
        val2=browser.find_link_by_partial_href('download')['href']
        hemi_dict={'title':val1,'img_url':val2}
        hemisphere_image_urls.append(hemi_dict)
        browser.visit(url)

        mars_facts["mars_hemispheres"] = hemisphere_image_urls

        mars_facts["hemisphere_titles"] = hemisphere_titles

    return mars_facts

if __name__ == '__main__':
    scraper = scrape()
    print(scraper)