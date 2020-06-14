#!/usr/bin/env python
# coding: utf-8


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def scrape_all():
    listings=scrape()
    image_data= image_scrape()
    facts= mars_facts()
    images_dict= images_scrape()
    data= {'news_title':listings['headline'],'news_paragraph':listings['para'],'featured_image':image_data,
    'facts': facts, 'hemisphere_images':images_dict}
    return data

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/Users/veronicavalencia/Desktop/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)



# Create BeautifulSoup object; parse with 'html.parser'
def scrape():
    browser = init_browser()
    listings = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    slide_element = soup.select_one('ul.item_list li.slide')
    listings["headline"] = slide_element.find("div",class_='content_title').get_text()
    listings["para"] = slide_element.find("div",class_='article_teaser_body').get_text()
    return listings





# Scrape page into Soup
def image_scrape():
   browser = init_browser()
   url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
   browser.visit(url)
   browser.is_element_present_by_css("img", wait_time=1)
   html = browser.html
   soup = BeautifulSoup(html, "html.parser")


# Find the src for the featured space image
   relative_image_path = soup.find_all('img')[2]["src"]
   featured_image_url = url + relative_image_path

   # Store data in a dictionary
   image_data = {
       "featured_image_url": featured_image_url
   }

   # Close the browser after scraping
   browser.quit()

   # Return results
   return image_data
   


def mars_facts():
#Mars Facts 
    url = 'https://space-facts.com/mars/)'
    facts = ['Equatorial Diameter', 'Polar Diameter', 'Mass', 'Moons', 'Orbit Distance', 'Orbit Period','Surface Temperature','First Record','Recorded By']

    # Use Panda's `read_html` to parse the url
    ### BEGIN SOLUTION
    tables = pd.read_html(url)
    tables
    ### END SOLUTION
    # Find the medical abbreviations DataFrame in the list of DataFrames as assign it to `df`
    # Assign the columns `['facts', 'fact']`
    ### BEGIN SOLUTION
    df = tables[2]
    df.columns = ['facts', 'fact']
    df.head(10)
    ### END SOLUTION

    html = df.to_html()
    return html 



def images_scrape():
    image_url = []
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    browser.is_element_present_by_css("a.product-item", wait_time=1)
    hemisphere_url = {}
    # Find all hemisphere images
    page = browser.find_by_css("a.product-item h3")
    
    for i in range(len(page)):
 # Find the src for the featured space image and title
        browser.find_by_css("a.product-item h3")[i].click()
        img_url= browser.find_link_by_text('Sample').first
        hemisphere_url['img_url']= img_url['href']
        hemisphere_url['title']= browser.find_by_css('h2.title').text
        image_url.append(hemisphere_url)
        browser.back()
    return image_url
    






