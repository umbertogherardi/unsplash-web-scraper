# unsplash_webscraper
A webscraper for Unsplash images with resolution selection. Resolution ranges vary from ~100 pixels to ~2000 pixels in width. Can be used to find high-quality images for computer vision/ ML training sets. 

Current bugs/ minor issues: 
 - Although the scraper reportedly finds 60 images from a given search, only 20 are unique (we have 3 sets of the same images). 
 - Unsplash only displays 20 images per page using this static-scraping method.
 
 Future fixes/ TODO list:
 - Prevent the scraper from grabbing duplicate image urls (could probably be implemented by using a set).
 - Determine how to request images directly from the Unsplash API, or use Selenium to dynamically scrape a webpage so we are not limited to 20 images per search.
