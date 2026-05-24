---
name: baidu-netdisk
description: 百度网盘文件下载和上传。当用户提到"百度网盘"、"网盘下载"、"网盘上传"、"pan download"、"pan upload"、"从网盘下载"、"上传到网盘"时触发。下载通过 Python 脚本实现，上传通过 MCP server baidu-netdisk-local-uploader 实现。
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

查找 MCP server `baidu-netdisk-local-uploader`：
- **如果存在**：直接使用 MCP tool `upload_file`，参数为 `local_file_path` 和可选的 `remote_path`
- **如果不存在**：按以下流程创建

### 创建 MCP Server 流程

1. 引导用户授权：
   > 请打开这个链接，登录网盘后点击授权按钮，将授权通过的完整 URL 发给我：
   > https://openapi.baidu.com/oauth/2.0/authorize?response_type=token&client_id=QHOuRXiepJBMjtk0esLhrPoNlQyYd0mF&redirect_uri=oob&scope=basic,netdisk

2. 从用户返回的 URL 中提取 `access_token` 参数值（URL 格式为 `https://openapi.baidu.com/oauth/2.0/login_success#access_token=xxx&...`，取 `access_token=` 后面的值，到 `&` 为止）

3. 获取 uv 绝对路径：
   ```bash
   which uv
   ```

4. 将以下配置添加到全局 MCP 配置文件 `~/.claude/.mcp.json`（与已有配置合并，不要覆盖）：
   ```json
   {
     "baidu-netdisk-local-uploader": {
       "type": "stdio",
       "command": "<uv绝对路径>",
       "args": [
         "--directory",
         "<HOME>/.claude/skills/baidu-netdisk/scripts/netdisk-mcp-server-stdio",
         "run",
         "netdisk.py"
       ],
       "env": {
         "BAIDU_NETDISK_ACCESS_TOKEN": "<用户的access_token>"
       }
     }
   }
   ```

5. 提示用户重启 Claude Code 使 MCP server 生效

## 注意事项

- 下载脚本中的 access token 有效期为 30 天，过期后需重新授权
- 上传 MCP server 同样使用该 token，过期后需更新 `~/.claude/.mcp.json` 中的 `BAIDU_NETDISK_ACCESS_TOKEN`
- 大于 4MB 的文件上传时会自动分片
