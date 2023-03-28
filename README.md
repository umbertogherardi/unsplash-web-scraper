# unsplash_webscraper
A webscraper for Unsplash images. 

Current bugs/ minor issues: 
 - Although the scraper reportedly finds 60 images from a given search, only 20 are unique (we have 3 sets of the same images). 
 - Unsplash only displays 20 images per page using this static-scraping method.
 
 Future fixes/ TODO list:
 - Prevent the scraper from grabbing duplicate image urls (could probably be implemented by simply using a set).
 - Research the unsplash API/ Selenium documentation to scrape the entire collection of iamge urls returend from a search query. 
