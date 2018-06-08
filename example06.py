import pickle
import zlib
from datetime import datetime
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from hashlib import sha1
import pymongo

def main():
    client = pymongo.MongoClient(host='118.25.211.249',port=27017)
    db = client.zhihu
    page_cache = db.webpages
    page_cache.create_index([("expire", 1)], expireAfterSeconds=10)

    base_url = 'http://www.zhihu.com'
    url = urljoin(base_url,'explore')
    headers = {'user-agent':'baiduspaider'}
    reps = requests.get(url,headers=headers)
    soup = BeautifulSoup(reps.text,'lxml')

    hasher_proto = sha1()
    for elem in soup.find_all('a',{'href':re.compile(r'^/question')}):
        href = elem.attrs['href']
        full_url = urljoin(base_url,href)

        hasher = hasher_proto.copy()
        hasher.update(full_url.encode('utf-8'))
        key_url = hasher.hexdigest()

        if not page_cache.find_one({'url':key_url}):
            html_page = requests.get(full_url,headers=headers).text
            zhtml_page = zlib.compress(pickle.dumps(html_page))
            page_cache.insert_one({'url':key_url,'content':zhtml_page,'expire':datetime.utcnow()})
            print(page_cache.find().count(),full_url)


if __name__ == '__main__':
    main()