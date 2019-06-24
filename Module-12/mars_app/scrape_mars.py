#Unit 12 Assigment - Mission to Mars
#Step 2 MongoDB and Flask Application
#@version 1.0
#@author Martha Meses

import pandas as pd
import requests
from splinter import Browser
# For parsing HTML
from bs4 import BeautifulSoup as bs

# For automating browser actions
def init_browser():
        executable_path = {'executable_path': 'chromedriver.exe'}
        # Defining the path for CHROM driver
        return Browser("chrome", **executable_path, headless=False)

def scrape_data():
### NASA Mars News
        # Website to scrap
        url = 'https://mars.nasa.gov/news/'
        # Creating a new Browser instance for CHROM driver
        browser = init_browser()
        # Visiting the url in CHROM browser
        browser.visit(url)
        # Getting the html content
        html = browser.html
        # Parser html to beutifulsoup with lxml
        soup = bs(html,'lxml')
        # Print all html
        # print(soup.prettify())
        # Getting the latest news title
        arrayNewsTitle = []
        scrapeNewsTitle = soup.find_all('div', class_="bottom_gradient")
        for data in scrapeNewsTitle:
                h3 = data.find('h3')
                arrayNewsTitle.append((h3.text))
        latestNewsTitle = arrayNewsTitle[0]
        # print(latestNewsTitle)
        # Getting the lastes news paragraph
        arrayNewsParaText = []
        scrapeNewsParaText = soup.find_all('div', class_="image_and_description_container")
        for data in scrapeNewsParaText:
                div = data.find('div', class_="rollover_description_inner" )
                arrayNewsParaText.append((div.text))
        latestNewsParaText = arrayNewsParaText[0]
        # print(latestNewsParaText)
        # Close the browser after scraping
        browser.quit()
### END NASA Mars News
### JPL Mars Space Images - Featured Image
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        # Creating a new Browser instance for CHROM driver
        browser = init_browser()
        # Visiting the url in CHROM browser
        browser.visit(url)
        # Getting the html content
        browser.html
        # Getting the Featured image
        arrayHrefImage = []
        scrapeFeaturedImage = browser.find_by_tag('a')
        for a in scrapeFeaturedImage:
                hrefImage = a._element.get_attribute('data-fancybox-href')
                if hrefImage != None:
                        arrayHrefImage.append((hrefImage))
        featuredImageUrl = "https://www.jpl.nasa.gov" + arrayHrefImage[1]
        # print(featuredImageUrl)
        # Close the browser after scraping
        browser.quit()
### END JPL Mars Space Images - Featured Image
### Mars Weather
        url = 'https://twitter.com/marswxreport?lang=en'
        # Creating a new Browser instance for CHROM driver
        browser = init_browser()
        # Visiting the url in CHROM browser
        browser.visit(url)
        # Getting the html content
        html = browser.html
        # Parser html to beutifulsoup with lxml
        soup = bs(html,'lxml')
        # Print all html
        # print(soup.prettify())
        # Getting the latest Mars weather tweet
        arrayTweetText = []
        scrapeMarsWeatherTweet = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
        for tweet in scrapeMarsWeatherTweet:
                tweetText = tweet.text
                arrayTweetText.append((tweetText))
        mars_weather = arrayTweetText[0]
        # print(mars_weather)
        # Close the browser after scraping
        browser.quit()
###END Mars Weather
### Mars Facts
        url = 'https://space-facts.com/mars/'
        # Scrape the table of the url with pandas
        tableScrape = pd.read_html(url)
        df = tableScrape[0]
        df.columns = ['Description','Value']
        df.set_index('Description', inplace=True)
        htmlTable = df.to_html()
        htmlTable = htmlTable.replace('\n','')
        # htmlTable
### END Mars Facts
### Mars Hemispheres
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        # Creating a new Browser instance for CHROM driver
        # browser = Browser('chrome', **executable_path, headless=False)
        browser = init_browser()
        # Visiting the url in CHROM browser
        browser.visit(url)
        # Getting the html content
        html = browser.html
        # Parser html to beutifulsoup with lxml
        soup = bs(html,'lxml')
        # Print all html
        # print(soup.prettify())
        # Getting the high resolution images for each Mar's hemispheres
        arrayHemisphereTitle = []
        arrayNextUrl = []
        scrapeMarsHemispheres = soup.find_all('div', class_='item')
        for hemisphere in scrapeMarsHemispheres:
                hemisphereTitle = hemisphere.h3.text
                arrayHemisphereTitle.append((hemisphereTitle))
                imageUrl = hemisphere.find('a', class_="itemLink product-item")
                imageHref = imageUrl['href']
                arrayNextUrl.append((imageHref))
        # arrayHemisphereTitle
        # arrayNextUrl
        arrayImageUrl=[]
        for nextUrl in arrayNextUrl: 
                url = 'https://astrogeology.usgs.gov' + nextUrl
                response = requests.get(url)
                result = response.text
                soup = bs(result,'lxml')
                scrapeImage = soup.find_all('ul')
                for image in scrapeImage:
                        imageUrl = image.a['href']
                        arrayImageUrl.append((imageUrl))
        # Getting just the url that I need
        arrayImageUrl2 = [arrayImageUrl[0],arrayImageUrl[2],arrayImageUrl[4],arrayImageUrl[6]]
        # arrayImageUrl2
        # Creating a list 
        dictImageUrl = {}
        for x in range(4):
                t = arrayHemisphereTitle[x]
                v = arrayImageUrl2[x]
                dictImageUrl[x] = {'title':t, 'img_url': v}
        hemisphere_image_url = [dictImageUrl.get(0),dictImageUrl.get(1),dictImageUrl.get(2),dictImageUrl.get(3)]
        # hemisphere_image_url
        # Close the browser after scraping
        browser.quit()
###END Mars Hemispheres

        # Store data scraped in a dictionary
        scraped_data = {
                'newsTitle':latestNewsTitle,
                'newsPara':latestNewsParaText,
                'featuredImage':featuredImageUrl,
                'weatherTweet':mars_weather,
                'facts':htmlTable,
                'marsHemisphere':hemisphere_image_url
        }

        return(scraped_data)

