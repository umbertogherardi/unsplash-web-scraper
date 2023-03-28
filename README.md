# unsplash_webscraper
A webscraper for Unsplash images, with resolution selection. Resolution options for a given search range from a width of ~100 pixels to ~2000 pixels.

Current bugs/ minor issues: 
 - Although the scraper reportedly finds 60 images from a given search, only 20 are unique (we have 3 sets of the same images). 
 - Unsplash only displays 20 images per page using this static-scraping method.
 
 Future fixes/ TODO list:
 - Prevent the scraper from grabbing duplicate image urls (could probably be implemented by simply using a set).
 - Determine how to request images directly from the Unsplash API, or use Selenium to dynamically scrape the entire collection of image urls returned from a search query. 
