#!/usr/bin/env python3
"""百度网盘文件下载脚本
参数：access_token, 网盘路径，本地路径
access_token 从 baidu-netdisk-local-uploader MCP 配置的 BAIDU_NETDISK_ACCESS_TOKEN 读取
"""

import requests
import os
import sys
import argparse


def download(remote_path: str, local_path: str = None, access_token: str = None):
    """从百度网盘下载文件

    参数:
    - remote_path: 网盘文件路径，如 /00.王斌/04.照片/IMG_3300.JPG
    - local_path: 本地保存路径，默认为当前目录下的文件名
    - access_token: 百度网盘 access_token
    """
    filename = os.path.basename(remote_path)
    parent_dir = os.path.dirname(remote_path)
    if not local_path:
        local_path = filename

    # Step 1: 列出目录文件，获取 fs_id
    r = requests.get(
        "https://pan.baidu.com/rest/2.0/xpan/file",
        params={
            "method": "list",
            "access_token": access_token,
            "dir": parent_dir + "/",
            "start": 0,
            "limit": 100,
        },
    )
    if r.status_code != 200:
        print(f"列出目录失败：HTTP {r.status_code}")
        return False

    fs_id = None
    for f in r.json().get("list", []):
        if f.get("server_filename") == filename or f.get("path") == remote_path:
            fs_id = f["fs_id"]
            print(f"找到文件：fs_id={fs_id}, size={f['size']/1024/1024:.1f}MB")
            break

    if not fs_id:
        print(f"文件未找到：{remote_path}")
        return False

    # Step 2: 获取下载链接
    r2 = requests.get(
        "https://pan.baidu.com/rest/2.0/xpan/multimedia",
        params={
            "method": "filemetas",
            "access_token": access_token,
            "fsids": f"[{fs_id}]",
            "dlink": 1,
        },
    )
    dlink = r2.json()["list"][0]["dlink"]
    dlink += "&access_token=" + access_token

    # Step 3: 下载文件
    print(f"正在下载到：{local_path}")
    r3 = requests.get(dlink, headers={"User-Agent": "netdisk"}, stream=True)
    if r3.status_code != 200:
        print(f"下载失败：HTTP {r3.status_code}")
        return False

    total = int(r3.headers.get("Content-Length", 0))
    downloaded = 0
    with open(local_path, "wb") as f:
        for chunk in r3.iter_content(8192):
            f.write(chunk)
            downloaded += len(chunk)
            if total:
                pct = downloaded / total * 100
                print(f"\r  进度：{pct:.0f}% ({downloaded/1024/1024:.1f}/{total/1024/1024:.1f}MB)", end="", flush=True)
    print()

    print(f"下载完成：{local_path} ({os.path.getsize(local_path)/1024/1024:.1f}MB)")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="百度网盘下载脚本")
    parser.add_argument("remote_path", help="网盘文件路径，如 /00.王斌/04.照片/IMG_3300.JPG")
    parser.add_argument("local_path", nargs="?", help="本地保存路径，默认保存到当前目录")

    args = parser.parse_args()

    # 从 MCP 配置的 BAIDU_NETDISK_ACCESS_TOKEN 读取 token
    access_token = os.environ.get("BAIDU_NETDISK_ACCESS_TOKEN")
    if not access_token:
        print("error: BAIDU_NETDISK_ACCESS_TOKEN not set, please configure baidu-netdisk-local-uploader MCP server")
        sys.exit(1)

    remote = args.remote_path
    local = args.local_path
    download(remote, local, access_token)
