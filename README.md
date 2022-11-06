# Project 3 Submission: Webscraping Ebay

This project was a result of the prompts listed [here](https://github.com/mikeizbicki/cmc-csci040/tree/2022fall/project_03).

**What the `ebay-dl.py` file does:** 

This file takes in a search term and (optionally) number of pages and scrapes ebay, returning the number of pages specified for the specific search term in JSON file format. The JSON file returns a dictionary with the name, price (in cents), status (brand new, refurbished, pre-ownedl, etc), shipping costs (in cents), whether free returns are possible, and the number of items sold. 


**How to run the `ebay-dl.py` file :** 
Firstly, enter in the item and the number of pages you wish to see from ebay after the ebay-dl.py. 


<pre><code>scrapingebay/ebay-dl.py" 'item query here'
</code></pre>

\

In this case, I've entered panini press for the item query and the number of pages as 10. If you want less than 10 pages, specify as necessary! This will return the `panini press.json` file that you can see linked in this repo. This file will have 10 pages worth of content regarding panini presses from ebay.


<pre><code>scrapingebay/ebay-dl.py" 'panini press' --num_pages=10
</code></pre>
