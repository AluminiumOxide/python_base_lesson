import json
import os.path

import requests
import urllib3
from bs4 import  BeautifulSoup
import re
import m3u8
from urllib.parse import urljoin
import subprocess


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_m3u8_url(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"
    }
    res = requests.get(url, headers=head)
    res_cont = res.content.decode('utf-8')
    # print(res.content.decode('utf-8'))

    soup = BeautifulSoup(res_cont,"html.parser")
    head_name = soup.find("h1", class_="name nowrap").string
    script_tag = soup.find("div", class_="player").find("script",attrs={"type":"text/javascript"}).string
    # print(head_name, script_tag)

    match = re.search(r"var player_aaaa\s*=\s*(\{.*\})",script_tag, re.DOTALL)
    # print(match)
    json_info = json.loads(match.group(1))
    # print(json_info)
    m3u8_url = json_info.get("url")
    # print(m3u8_url)
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


def get_ts_file(ts_list):
    save_dir = "cache_ts"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    local_file = []
    for i,one_ts in enumerate(ts_list):
        one_path = os.path.join(save_dir, f"{i:05d}.ts")
        if not os.path.exists(one_path):
            try:
                res = requests.get(one_ts,verify=False)
                res.raise_for_status()
                with open(one_path,"wb") as f:
                    f.write(res.content)
                print(f"download {one_path} {i} success")
            except Exception as e:
                print(f"download {one_path} {i} failed")
                continue
        local_file.append(one_path)
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

    url = "https://fcdm004.cc/bf/7036-1-1.html"
    url = "https://www.yhdm1111.cc/bofang/7036-1-1.html"

    m3u8_url,head_name = get_m3u8_url(url)

    ts_list = get_ts_list(m3u8_url)

    file_list = get_ts_file(ts_list)

    get_video(file_list, head_name+".mp4")


















