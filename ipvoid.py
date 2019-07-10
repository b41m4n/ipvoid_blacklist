import requests
import csv
from bs4 import BeautifulSoup
import time
import re
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
def ipvoid(blacklist_ip):
    url = "https://www.ipvoid.com/ip-blacklist-check/"
    session = requests.Session()
    data = {'ip' : blacklist_ip}
    ip_details = session.post(url, data = data, headers = headers)
    soup = BeautifulSoup(ip_details.content, 'html.parser')
    ip_addr_info = soup.find(id = "ip-address-information")
    ip_info = [tag.find_all("td")[1].text for tag in ip_addr_info.find_next_sibling().find_all("tr")]
    host_name = 'N/A' if ip_info[4] == 'Unknown' else ip_info[4]
    blacklist_ip_address = re.search(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})',ip_info[3]).group()
    try:
        country = re.search(r'((?=\s\().*?(?=\s))\s([\w.-]+\s[\w.-]+)', ip_info[9]).group(2)
    except AttributeError:
        country = re.search(r'((?=\s\().*(?=\s))\s([\w.-]+)',ip_info[9]).group(2)
    blacklist_ip_info = [blacklist_ip_address, host_name, ip_info[7], country, ip_info[2]]
    return blacklist_ip_info

def main():
    file_name = "Desktop\\ip_list.txt"
    blacklist_sheet = "Desktop\\blacklist.csv"
    blacklist_ips = [line.rstrip('\n') for line in open(file_name)]
    with open(blacklist_sheet, 'wb') as csvfile:
        fields = ['IP', 'Hostname', 'ISP', 'Location', 'Blacklist Status']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        for ip in blacklist_ips:
            csvwriter.writerow(ipvoid(ip))
            time.sleep(3)

if __name__ == "__main__":
    main()