import os, time, requests
from bs4 import BeautifulSoup

url = "http://vote.2018.nat.gov.tw/mobile/zh_TW/TC/63000000000000000.html"
sleep = 10

last_count = 0
last_count_diff = 0

try:
    while(True):
        data = []

        html = requests.get(url).text

        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div', attrs={'class': 'table-content'})
        table = div.find('table')
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            cols = [col.text for col in cols]
            data.append([col for col in cols])

        ding = [data[1][2], data[1][4].replace(',', '')]
        kp  =  [data[3][2], data[3][4].replace(',', '')]

        diff = int(kp[1]) - int(ding[1])
        sign = '+' if diff > 0 else '-'
        rate = round(abs(int(kp[1]) - int(ding[1])) / (int(kp[1]) + int(ding[1])) * 100, 2)

        if(diff != last_count):
            last_count_diff = diff - last_count
            last_count = diff

        footer = soup.find('div', attrs={'class': 'table-footer-right'})
        info_raw = footer.text.replace(u'\xa0', ' ').split()[1:]
        send = info_raw[1].split('/')
        send_diff = int(send[1]) - int(send[0])
        info = [' '.join(info_raw[0:2]) + ' (' + str(send_diff) + ')', ' '.join(info_raw[2:])]

        os.system('clear')
        print(': '.join(ding))
        print(': '.join(kp))
        print('柯文哲 VS 丁守中:', sign + str(diff) + '(' + str(last_count_diff) + ')', '(' + str(rate) + '%)')
        [print(x) for x in info]

        time.sleep(sleep)
except KeyboardInterrupt:
    print("Exit...")
