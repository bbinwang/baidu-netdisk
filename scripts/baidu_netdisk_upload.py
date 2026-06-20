#!/usr/bin/env python3
"""
百度网盘上传脚本
参数：本地路径，云盘路径
复用 netdisk.py 中的上传能力，从 baidu-netdisk-local-uploader MCP 配置的 BAIDU_NETDISK_ACCESS_TOKEN 读取 token
"""
import os
import sys
import argparse

# 添加 netdisk-mcp-server-stdio 目录到路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NETDISK_DIR = os.path.join(BASE_DIR, "netdisk-mcp-server-stdio")
sys.path.append(NETDISK_DIR)

from netdisk import upload_file


def main():
    parser = argparse.ArgumentParser(description="百度网盘上传脚本")
    parser.add_argument("local_path", help="本地文件路径")
    parser.add_argument("remote_path", help="云盘路径（必须以/开头）")

    args = parser.parse_args()

    # 从 MCP 配置的 BAIDU_NETDISK_ACCESS_TOKEN 读取 token
    token = os.environ.get("BAIDU_NETDISK_ACCESS_TOKEN")
    if not token:
        print("error: BAIDU_NETDISK_ACCESS_TOKEN not set, please configure baidu-netdisk-local-uploader MCP server")
        return 1

    # 调用 upload_file
    result = upload_file(args.local_path, args.remote_path)

    # 输出结果
    print(result)

    # 返回状态码
    return 0 if result.get("status") == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
