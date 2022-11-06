import argparse
import requests
from bs4 import BeautifulSoup
import json 

def parse_itemssold(text):
    '''
    Takes as input a string and returns the number of items sold, as specified in the string 

    >>> parse_itemssold('38 sold')
    38
    >>> parse_itemssold('14 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text.lower():
        return int(numbers)
    else:
        return 0

def parse_price(text):
    price = ''
    if 'see price' in text.lower():
        return None
    else:
        for char in text:
            if char in '1234567890':
                price += char
        return int(price)

def parse_shipping(text):
    shipping = ''
    if 'free' in text.lower():
        shipping = 0
    else:
        for char in text:
            if char in '1234567890':
                shipping += char
    
    return int(shipping)

# this if statement only runs the code below when python file is run normally (not in the doctests)
if __name__ == '__main__':

    #get command line args
    parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default = 10)
    args = parser.parse_args()
    print('args.search_term=', args.search_term)

    # list of all items found in all ebay webpages
    items = []

    # loop over the ebay webpages
    for page_number in range(1,int(args.num_pages)+1):
        #make the url 
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='
        url += args.search_term 
        url += '&_sacat=0&_pgn='
        url += str(page_number)
        url += '&rt=nc'    
        print('url=', url)

        #download the html
        r = requests.get(url)
        status = r.status_code #status = 200; which means success
        print('status=', status)
        html = r.text  #gets the text

        #process the html
        soup = BeautifulSoup(html, 'html.parser')

        #loop over the items in each page
        tags_items = soup.select('.s-item')
        for tag_item in tags_items:

            #extract the name
            name = None
            tags_name = tag_item.select('.s-item__title')
            for tag in tags_name:
                name = tag.text

            #extract the price
            price = None
            tags_price = tag_item.select('.s-item__price')
            for tag in tags_price:
                price = parse_price(tag.text)
            
            #extract the status: "Brand New', 'Refurbished', 'Pre-owned'
            status = None
            tags_status = tag_item.select('.SECONDARY_INFO')
            for tag in tags_status:
                status = tag.text

            #extract status of shipping; price of shipping the item in cents, stored as an int. if free, value is 0
            shipping = 0
            tags_shipping = tag_item.select('.s-item__shipping, .s-item__freeXDays')
            for tag in tags_shipping:
                shipping = parse_shipping(tag.text)
            
            #extract the free_returns
            free_returns = False
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns:
                free_returns = True

            #extract the # of items sold
            items_sold = 0
            tags_itemssold = tag_item.select('.s-item__hotness')
            for tag in tags_itemssold:
                items_sold = parse_itemssold(tag.text)
            #create a dictionary with the keys/values
            item = {
                'name': name,
                'price': price,
                'status': status,
                'shipping': shipping,
                'free_returns': free_returns,
                'items_sold': items_sold,
            }
            items.append(item)

    #write the json to a file
    filename = args.search_term+'.json'
    with open(filename, 'w', encoding='ascii') as f:
        f.write(json.dumps(items))