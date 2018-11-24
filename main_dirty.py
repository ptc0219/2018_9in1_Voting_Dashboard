import os, time, requests
from bs4 import BeautifulSoup

url = "http://vote.2018.nat.gov.tw/mobile/zh_TW/TC/63000000000000000.html"

last_count = 0
last_count_diff = 0

while(True):
    os.system('clear')
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    data = []
    div = soup.find('div', attrs={'class': 'table-content'})
    table = div.find('table')
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    ding = [data[1][1], data[1][3].replace(',', '')]
    kp  =  [data[3][1], data[3][3].replace(',', '')]

    print(': '.join(ding))
    print(': '.join(kp))
    diff = int(kp[1]) - int(ding[1])
    if(diff != last_count):
        last_count_diff = diff - last_count
        last_count = diff
    sign = '+' if diff > 0 else '-'
    diff_per = abs(int(kp[1]) - int(ding[1])) / (int(kp[1]) + int(ding[1])) * 100
    print('柯文哲 VS 丁守中:', sign + str(diff) + '(' + str(last_count_diff) + ')', '(' + str(round(diff_per, 2)) + '%)')

    footer = soup.find('div', attrs={'class': 'table-footer-right'})
    info_raw = footer.text.strip().replace(u'\xa0', ' ').split()[1:]
    send = info_raw[1].split('/')
    info = [' '.join(info_raw[0:2]) + ' (' + str(int(send[1]) - int(send[0])) + ')', ' '.join(info_raw[2:])]
    [print(x) for x in info]
    time.sleep(10)