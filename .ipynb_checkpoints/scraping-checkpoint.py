# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    browser_2 = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemispheres": hemisphere_images(browser_2)
    }
    
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    #asking at the same time if there is any list_text as tag on the webpage
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')
    
    # Add try/except for error handling
    try:
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        #news_p
    except AttributeError:
        return None, None
    
    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    #The instruction from the development mode is :
    #<button class="btn btn-outline-light"> FULL IMMAGE</button>
    #this command was execute directly from "browser" property
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel
    except AttributeError:
        return None
        
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    #img_url

    browser.quit()
    
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

def hemisphere_images(browser):
    
    url = 'https://marshemispheres.com'
    browser.visit(url)
    
    html = browser.html
    img_soup = soup(html,'html.parser')
    
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    try:
        
        #3. Write code to retrieve the image urls and titles for each hemisphere.
        i=0
        sections = img_soup.find_all('div',class_='item')
        for i in range(4):
    
            html = browser.html
            img_soup = soup(html,'html.parser')
    
            #click based on h3 tag 
            url = browser.find_by_tag('h3')[i]
            url.click()
    
            #visit section of the webpage
            html = browser.html
            img_soup = soup(html,'html.parser')
    
            #extract title
            titulo = img_soup.find('h2', class_='title').text
            image = img_soup.find("div",class_="downloads")
            imagen = image.a['href']
            imagen_url = f'https://marshemispheres.com/{imagen}'
    
            Mars_temp = {
                      'img_url':imagen_url,
                      'title':titulo
                    }

            hemisphere_image_urls.append(Mars_temp)
    
            browser.back()
        
    except AttributeError:
        return None
    
    browser.quit()
    return hemisphere_image_urls