# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
#asking at the same time if there is any list_text as tag on the webpage
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

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

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

#---------
# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)
html = browser.html
img_soup = soup(html,'html.parser')
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

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
    
    #print(f'{titulo} {imagen_url}')
    
    hemisphere_image_urls.append(Mars_temp)
    
    browser.back()

browser.quit()