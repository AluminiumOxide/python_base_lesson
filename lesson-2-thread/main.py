import json
import os.path
import random
import sys
import threading

import requests
import urllib3
from bs4 import  BeautifulSoup
import re
import m3u8
from urllib.parse import urljoin
import subprocess


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def random_header():
    user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36',
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3_old.0.30729; .NET CLR 3_old.5.30729; InfoPath.3_old; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (Linux; U; Android 2.3_old.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3_old.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Opera/9.80 (Android 2.3_old.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        "Mozilla/5.0 (Linux; U; Android 3_old.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3_old.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
        "UCWEB7.0.2.37/28/999",
        "NOKIA5700/ UCWEB7.0.2.37/28/999",
        "Openwave/ UCWEB7.0.2.37/28/999",
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    ]
    headers = {
        "User-Agent": random.choice(user_agent)
    }
    return headers


ts_head = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Origin": "https://jx.18988.net",
    "Priority": "u=1, i",
    "Sec-CH-UA": '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
}


def get_m3u8_url(url):
    # head = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"
    # }
    res = requests.get(url, headers=random_header())
    res_cont = res.content.decode('utf-8')
    print(res.content.decode('utf-8'))
    # sys.exit()
    soup = BeautifulSoup(res_cont,"html.parser")
    head_name = soup.find("a", class_="text-overflow").string
    script_tag = soup.find("div", class_="embed-responsive").find("script",attrs={"type":"text/javascript"}).string
    # print(head_name, script_tag)

    match = re.search(r"var player_aaaa\s*=\s*(\{.*\})",script_tag, re.DOTALL)
    # print(match)
    json_info = json.loads(match.group(1))
    # print(json_info)
    m3u8_url = json_info.get("url")
    print(m3u8_url)
    print(head_name)
    return m3u8_url,head_name


def get_ts_list(m3u8_url):
    ts_list = []
    queue = [m3u8_url]
    while queue:
        now = queue.pop(0)
        resp = requests.get(now, verify=False)
        # resp.raise_for_status()
        m3u8_obj = m3u8.loads(resp.text)

        if m3u8_obj.is_variant:
            # 遍历多级m3u8
            for now_list in m3u8_obj.playlists:
                now_uri = now_list.uri
                if not now_uri.startswith("http"):
                    now_uri = urljoin(now, now_uri)
                queue.append(now_uri)
                print(f"add: {now_uri}")
        else:
            # 遍历ts
            for now_list in m3u8_obj.segments:
                now_uri = now_list.uri
                if not now_uri.startswith("http"):
                    now_uri = urljoin(now, now_uri)
                ts_list.append(now_uri)
                print(f"find: {now_uri}")
    return ts_list


def download_one_ts(i,one_ts,save_dir,local_file,lock):
    one_path = os.path.join(save_dir, f"{i:05d}.ts")
    if os.path.exists(one_path):
        print(f"{one_path} already exist, pass")
        with lock:
            local_file[i] = one_path
        return
    try:
        res = requests.get(one_ts, headers=ts_head, verify=False)
        res.raise_for_status()
        with open(one_path, "wb") as f:
            f.write(res.content)
        print(f"download {one_path} {i} success")
        with lock:
            local_file[i] = one_path
    except Exception as e:
        print(f"download {one_path} {i} failed")
        with lock:
            local_file[i] = None


def get_ts_file(ts_list):
    thread_num = 6
    save_dir = "cache_ts"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    local_file = [None] * len(ts_list)
    thread_list = []
    lock = threading.Lock()
    # for i,one_ts in enumerate(ts_list):
    for i in range(0,len(ts_list),thread_num):
        ts_batch = ts_list[i:i+thread_num]

        thread_list.clear()
        for j,one_ts in enumerate(ts_batch, start=i):
            t = threading.Thread(target=download_one_ts, args=(j,one_ts,save_dir,local_file,lock))
            t.start()
            thread_list.append(t)

        # join
        for t in thread_list:
            t.join()

    # print(local_file)
    return local_file


def get_video(file_list, head_name):
    with open("cache_ts_list.txt", "w", encoding="utf-8") as f:
        for one_file in file_list:
            f.write(f"file '{os.path.abspath(one_file)}'\n")

    cmd = [
        "ffmpeg",
        "-f", "concat", "-safe", "0", "-i", "cache_ts_list.txt", "-c", "copy", head_name
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    os.remove("cache_ts_list.txt")

    if res.returncode != 0:
        print("ffmpeg run failed")


if __name__ == '__main__':

    url = "https://www.dongmandaquan.vip/vodplay/19847-6-1.html"

    m3u8_url,head_name = get_m3u8_url(url)

    ts_list = get_ts_list(m3u8_url)

    file_list = get_ts_file(ts_list)

    get_video(file_list, head_name+".mp4")


















