from bs4 import BeautifulSoup
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time
import pandas as pd
import pymongo


mars_data = {}

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    news_url = 'https://mars.nasa.gov/news/'
    response = requests.get(news_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.findAll('div', class_="features")
    for result in results:
        slides = result.findAll('div', class_="slide")
        for slide in slides:
            news_title = slide.find('div', class_="content_title")
            news_p = slide.find('div', class_="rollover_description_inner")
            # Error handling
            try:
                # Identify and return title of listing        
                title = news_title.a.text
        #         # Identify and return price of listing
                snippet = news_p.text
        #         # Identify and return link to listing

        #         # Print results only if title, price, and link are available
                if (title and snippet):
                    print('-------------')
                    print(title)
                    print(snippet)
            except AttributeError as e:
                print(e)
                news_title = news_title.a.text
                news_snippet = news_p.text
                mars_data['news_title'] = news_title
                mars_data['news_snipper'] = news_snippet
    time.sleep(1)
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    base_url = 'https://www.jpl.nasa.gov'
    time.sleep(1)
    for x in range(1):
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find('footer')
        browser.find_by_id('full_image').click()
        browser.is_element_present_by_text('more info', wait_time=4)
        button = 'more info'
        browser.find_link_by_partial_text(button).click()
        html = browser.html
        soup1 = BeautifulSoup(html, 'html.parser')
        figure = soup1.find('figure', class_="lede")
        hires_img_url = figure.find('a')['href']
        featured_img_url = base_url + hires_img_url
        print(featured_img_url)
        # browser.visit(featured_img_url)
        jpl_img = featured_img_url
        mars_data['jpl_img'] = jpl_img
    time.sleep(1)
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(weather_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find('div', class_="js-tweet-text-container")
    latest_tweet = results.p
    mars_weather = latest_tweet.text.strip()
    print(mars_weather)
    mars_data['weather'] = mars_weather
    time.sleep(1)
    facts_url = 'https://space-facts.com/mars/'
    facts = pd.read_html(facts_url)
    facts
    type(facts)
    df = facts[0]
    df.head()
    html_table = df.to_html()
    html_table.replace('\n', '')
    mars_facts = html_table.replace('\n', '')
    mars_data['mars_facts'] = mars_facts
    time.sleep(1)
    hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response = requests.get(hemis_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', class_="itemLink product-item")
    hemispheres = []
    titles = []
    desc = soup.find_all('div', class_="description")
    names = desc[0].text
    names = names.rsplit(' ', 1)[0]
    for result in results:
        hemispheres.append(result['href'])
    for x in range(4):
        titles.append(desc[x].text.rsplit(' ', 1)[0])
    print(hemispheres)
    print(titles)
    for y in range(0,4):
        enhanced_img = []
        full_url = []
        base_url = "https://astrogeology.usgs.gov"
        enhanced_url = base_url + hemispheres[y]
        enhanced_img.append(enhanced_url)
    print(enhanced_img)
    for z in range(len(enhanced_img)):
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(enhanced_img[z])
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        result = soup.find('ul')
        list = result.find('li')
        full_img = list.find('a')['href']
        full_url.append(full_img)
        hemisphere_dict = {}
        for a in range(4):
            hemisphere_dict[titles[a]] = full_url[a]
            mars_data['hemispheres'] = hemisphere_dict
            browser.quit()
            print(mars_data)
            browser.quit()
            return mars_data
