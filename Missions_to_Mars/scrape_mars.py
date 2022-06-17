from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # # NASA Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find('div', class_="content_title").text

    news_paragraph = soup.find('div', class_ = "article_teaser_body").text

    #print(title)
    #print(paragraph)

    # # JPL Mars Space Images - Featured Image

    images_url = 'https://spaceimages-mars.com'
    browser.visit(images_url)

    images_html = browser.html
    images_soup = bs(images_html, "html.parser")

    browser.links.find_by_partial_text('FULL IMAGE').click()
    time.sleep(3)
    images_html = browser.html
    images_soup = bs(images_html, 'html.parser')

    featured_image = images_soup.find('img', class_='fancybox-image')
    featured_image_url = 'https://spaceimages-mars.com/'+ featured_image['src']
    #print(featured_image_url)


    # # Mars Facts

    mars_facts_url = 'https://galaxyfacts-mars.com'
    browser.visit(mars_facts_url)

    tables = pd.read_html(mars_facts_url)
    df = tables[0]
    df.rename(columns={0:'Facts',1:'Mars'}, inplace=True)
    
    df = df.iloc[1: , :]
    df = df.drop([2], axis=1)
    df = df.reset_index(drop=True)
    df.set_index('Facts', inplace=True)
    #df

    html_table = df.to_html()
    #html_table

    # # Mars Hemisphere

    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    titles = []
    urls = []
    mars_data = {}

    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html, "html.parser")
    hemispheres = hemispheres_soup.find_all('div', class_="description")
    for hemisphere in hemispheres:
        titles.append(hemisphere.find('a').text.strip())
        browser.links.find_by_partial_text(hemisphere.find('a').text.strip()).click()
        time.sleep(1)
        hemisphere_html = browser.html
        hemisphere_soup = bs(hemisphere_html, 'html.parser')
        hemisphere_image = hemisphere_soup.find('img', class_='wide-image')
        hemisphere_image_url = hemispheres_url + hemisphere_image['src']
        urls.append(hemisphere_image_url)
        browser.links.find_by_partial_text('Back').click()
        time.sleep(1)
    #print(title)
    #print(urls)
    
    hemisphere_list = []
    i = 0
    for title in titles:
        img_url = urls[i]
        hemisphere_dictionary = {'title': title, 'img_url': img_url}
        hemisphere_list.append(hemisphere_dictionary)
        i += 1
    #hemisphere_list

    browser.quit()

    mars_data = {
            'news_title': news_title, 
            'news_paragraph': news_paragraph, 
            'featured_image': featured_image_url,
            'mars_facts': html_table,
            'mars_hemisphere_images': hemisphere_list
            }

    return mars_data




