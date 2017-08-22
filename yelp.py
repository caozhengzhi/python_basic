from bs4 import BeautifulSoup
import requests

headers = {
    'Connection': 'keep-alive',
    'Access-Control-Request-Headers': 'content-type',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

response = requests.get('https://www.yelp.com/biz/founding-farmers-d-c-washington-2', headers=headers).text
soup = BeautifulSoup(response, 'html.parser')
import re
num_reviews = soup.find('span', attrs={'class': 'review-count rating-qualifier'}).text
num_reviews = int(re.search('\d+', num_reviews).group())
print(num_reviews)
url_list = []
for i in range(0, num_reviews//20 * 20, 20):
    url_list.append('https://www.yelp.com/biz/founding-farmers-d-c-washington-2?start='+str(i))
print(url_list)
reviews = soup.find_all('div', attrs={'class':'review review--with-sidebar'})
print(len(reviews))
review = reviews[0]
# Username
username = review.find('a', attrs={'class': 'user-display-name js-analytics-click'}).text
print(username)
# Location
location = review.find('li', attrs={'class': 'user-location responsive-hidden-small'}).text
print(location)
# Rating
rating = review.find('img', attrs={'class': 'offscreen'}).get('alt')
rating = float(re.search('\d+', rating).group())
print(rating)
# Date
date = review.find('span', attrs={'class': 'rating-qualifier'}).text
print(date)
# Content
content = review.find('p').text
print(content)

import csv
with open('reviews.csv', 'w') as csvfile:
    review_writer = csv.writer(csvfile)
    for review in reviews:
        dic = {}
        username = review.find('a', attrs={'class': 'user-display-name js-analytics-click'}).text
        location = review.find('li', attrs={'class': 'user-location responsive-hidden-small'}).text.strip()
        date = review.find('span', attrs={'class': 'rating-qualifier'}).text.strip()
        rating = review.find('img', attrs={'class': 'offscreen'}).get('alt')
        rating = float(re.search('\d+', rating).group())
        content = review.find('p').text
        dic['username'] = username
        dic['location'] = location
        dic['date'] = date
        dic['rating'] = rating
        dic['content'] = content
        review_writer.writerow(dic.values())
import time
import random


def scrape_reviews(reviews, csvwriter):
    for review in reviews:
        dic = {}
        username = review.find('a', attrs={'class': 'user-display-name js-analytics-click'}).text
        location = review.find('li', attrs={'class': 'user-location responsive-hidden-small'}).text.strip()
        date = review.find('span', attrs={'class': 'rating-qualifier'}).text.strip()
        rating = review.find('img', attrs={'class': 'offscreen'}).get('alt')
        rating = float(re.search('\d+', rating).group())
        content = review.find('p').text
        dic['username'] = username
        dic['location'] = location
        dic['date'] = date
        dic['rating'] = rating
        dic['content'] = content
        csvwriter.writerow(dic.values())


with open('reviews.csv', 'w') as csvfile:
    review_writer = csv.writer(csvfile)
    for index, url in enumerate(url_list):
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, 'html.parser')
        reviews = soup.find_all('div', attrs={'class': 'review review--with-sidebar'})
        scrape_reviews(reviews, review_writer)
        time.sleep(random.randint(1, 3))
        # Log the progress
        print('Finished page ' + str(index + 1))