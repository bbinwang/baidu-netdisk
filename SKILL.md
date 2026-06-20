---
name: baidu-netdisk
description: 百度网盘文件下载和上传。当用户提到"百度网盘"、"网盘下载"、"网盘上传"、"pan download"、"pan upload"、"从网盘下载"、"上传到网盘"时触发。下载通过 Python 脚本实现，上传优先使用上传脚本（从 MCP server 的 BAIDU_NETDISK_ACCESS_TOKEN 读取 token）。
---

# 百度网盘 Skill

百度网盘文件操作：下载和上传。

## 下载文件

使用下载脚本（bash 调用）：

```bash
python3 ~/.claude/skills/baidu-netdisk/scripts/baidu_netdisk_download.py "<网盘路径>" [本地保存路径]
```

示例：下载网盘文件到本地
```bash
python3 ~/.claude/skills/baidu-netdisk/scripts/baidu_netdisk_download.py "/00.王斌/04.照片/IMG_3300.JPG" ./IMG_3300.JPG
```

参数：
- 第一个参数（必填）：网盘文件路径，如 `/文件夹/文件名.jpg`
- 第二个参数（可选）：本地保存路径，默认保存到当前目录

## 上传文件

### 方式一：使用上传脚本（推荐）

```bash
python3 ~/.claude/skills/baidu-netdisk/scripts/baidu_netdisk_upload.py <本地路径> <云盘路径>
```

示例：上传文件
```bash
python3 ~/.claude/skills/baidu-netdisk/scripts/baidu_netdisk_upload.py \
  /home/user/document.pdf \
  "/00.王斌/04.工作/docs"
```

参数：
- 第一个参数（必填）：本地文件路径
- 第二个参数（必填）：云盘路径（必须以 `/` 开头）

说明：脚本会自动从 `baidu-netdisk-local-uploader` MCP 服务器配置的 `BAIDU_NETDISK_ACCESS_TOKEN` 环境变量读取 token，无需手动传入。

### 方式二：使用 MCP server

使用 MCP server `baidu-netdisk-local-uploader` 的 `upload_file` 工具：
- `local_file_path`：必填，本地文件路径
- `remote_path`：可选，云盘路径（默认保存到根目录）

## 注意事项

- `BAIDU_NETDISK_ACCESS_TOKEN` 有效期为 30 天，过期后需重新授权并更新配置
- 大于 4MB 的文件上传时会自动分片
