from selenium import webdriver
driver = webdriver.Chrome('./chromedriver')
driver.get('https://sync.readcube.com/collections/ff394a98-20f7-4882-871c-840e9f73d65b/items');
html = driver.page_source
f = open("bibtex.bib", "wt")
f.write(html)
f.close()

