import json

import requests
import datetime
import time
from bs4 import BeautifulSoup

def get_html(url, data):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
    }
    response = requests.get(url,data,headers=headers)
    response.encoding = 'gbk'
    return response.text

# def get_info(html):
#     soup = BeautifulSoup(html, 'lxml')
#     table = soup.find('table', attrs = {'id': 'report'})
#     trs = table.find('tr').find_next_siblings()
#     for i in range(0,15):
#         print(trs[i].get_text())
#     return trs
    # table = soup.table
    # # print(table)
    # tr = table.find_all('tr')
    # for i in range(4, 19):
    #     for j in range(0, 9):
    #         td = tr[i].find_all('td')
    #         print(td[j].get_text())
def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find("table", attrs={"id": "report"})
    trs = table.find("tr").find_next_siblings()
    for tr in trs:
        tds = tr.find_all("td")
        yield [
            tds[0].text.strip(),
            tds[1].text.strip(),
            tds[2].text.strip(),
            tds[3].text.strip(),
            tds[4].text.strip(),
            tds[5].text.strip(),
            tds[6].text.strip(),
            tds[7].text.strip(),
            tds[8].text.strip(),
        ]

def get_page_nums(ktrqks, ktrqjs):
    '''
    :return:返回的是需要爬取的总页数
    '''
    base_url = "http://www.hshfy.sh.cn/shfy/web/ktgg_search_content.jsp"
    data = {
        "ktrqks": ktrqks,
        "ktrqjs": ktrqjs,
    }
    while True:
        html = get_html(base_url,data)
        soup = BeautifulSoup(html, 'lxml')
        if soup.body.text.strip() == "系统繁忙":
            print("系统繁忙，登录太频繁，ip被封锁")
            time.sleep(ERROR_SLEEP_TIME)
            continue
        else:
            break
    res = soup.find("div",attrs={"class":"meneame"})

    page_nums = res.find('strong').text
    #这里获得page_nums是一个爬取的总条数，每页是15条数据，通过下面方法获取总页数
    page_nums = int(page_nums)
    if page_nums %15 == 0:
        page_nums = page_nums//15
    else:
        page_nums = page_nums//15 + 1
    print("总页数：",page_nums)
    return page_nums

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')

def main():
    pages_num = 1
    ktrqks = '2021-06-12'
    ktrqjs = '2021-07-12'
    pages_nums = get_page_nums(ktrqks, ktrqjs)

    base_url = 'http://www.hshfy.sh.cn/shfy/web/ktgg_search_content.jsp'
    data = {
        'ktrqks': ktrqks,
        'ktrqjs': ktrqjs,
        'pagesnum': pages_num
    }

    while pages_num <= pages_nums:
        html = get_html(base_url,data)
        res = parse_html(html)
        for i in res:
            write_to_file(i)
        print('爬完第【%s】页，共【%s】页'%(pages_num,pages_nums))
        pages_num += 1
        data['pagesnum'] = pages_num
        time.sleep(1)
    # print(get_info(html))
    # while pages_num <= pages_nums:
    #     html = get_html(base_url,data)

    return 0

if __name__ == '__main__':
    main()