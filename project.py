import requests
from bs4 import BeautifulSoup

def crawl_nate():
    url = "https://pann.nate.com"
    talk_url = "https://pann.nate.com/talk"
    resp = requests.get(talk_url)
    html = BeautifulSoup(resp.content, 'html.parser')
    f = open('./data/test.txt', 'w',  encoding='utf-8')
    
    s_talk = html.find('ul', {'id':  'categoryArea', 'class': 'odd'})
    categories = s_talk.findAll('a')
    
    for category in categories:
        f.write("category: {}\n".format(category.getText()))
        href = category['href']
        url_category = url + href
        cat_resp = requests.get(url_category)
        cat_html = BeautifulSoup(cat_resp.content, 'html.parser')

        post_list = cat_html.find('ul', {'class': 'post_list'})
        if(post_list):
            post_lists = post_list.findAll('a')
        
            for p in post_lists:
                href = p['href']
                if(href[6].isalpha()):
                    continue
                resp = requests.get(url+p['href'])
                html = BeautifulSoup(resp.content, 'html.parser')
                post = html.find('div', {'class': 'posting'})
                posts = post.find('div', {'id': 'contentArea'})
                txt = posts.getText().strip()
                if(txt):
                    f.write("post: {}\n".format(txt.strip()))

                f.write('comments: ')
                comments = html.findAll('dd', {'class': 'usertxt'})
                for comment in comments:
                    txt = comment.find('span').getText()
                    if(txt):
                        f.write("{}, ".format(txt.strip()))
    f.close()

if __name__ == '__main__':
    crawl_nate()
