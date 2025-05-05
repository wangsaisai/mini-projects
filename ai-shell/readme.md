# AI Shell 命令生成工具

本项目提供一个命令行工具，帮助用户通过自然语言描述自动生成对应的 Shell 命令。工具使用 AI 模型解析用户输入，生成高效、安全且符合最佳实践的 Shell 指令。

## 功能特点

- **自然语言输入**：用户可使用日常语言描述所需的 Shell 命令。
- **AI 自动生成命令**：利用 AI 模型智能生成对应的 Shell 命令。
- **交互式执行**：生成命令后，用户可选择是否执行。
- **可配置代理**：支持自定义代理设置，方便网络环境受限的用户使用。

## 环境要求

- Python 3.8 或更高版本
- 依赖项见 `requirements.txt`

## 安装步骤

1. 克隆项目到本地：


2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 设置环境变量（需自行申请 Google API Key）：

```bash
export GOOGLE_API_KEY=你的谷歌API密钥
```

4. （可选）如需使用代理，设置代理环境变量：

```bash
export http_proxy=http://127.0.0.1:1087
export https_proxy=http://127.0.0.1:1087
```

## 使用方法

在命令行中运行工具，并输入自然语言描述：

```bash
alias ai='python ai.py'
ai "列出当前目录下所有文件"

# 或直接运行
python ai.py "列出当前目录下所有文件"
```

### 示例输出

工具将生成对应的 Shell 命令：

```
(AI Thinking): 列出当前目录下所有文件的命令是 `ls`。
(AI Answer): ls
```

随后提示用户是否执行：

```
Execute? Y/N:
```

输入 `Y` 确认后，工具将执行该命令。

## 文件结构说明

- `ai.py`：命令行工具主程序。
- `requirements.txt`：Python 依赖列表。

## 注意事项

- 请确保你的 `GOOGLE_API_KEY` 有效且具备相应权限。
- 工具生成的命令并非百分百准确，请务必在执行前仔细核对。

## 致谢

- 使用了 `pydantic-ai` 和 `httpx` 库。
- AI 模型由 Google GLA 提供支持。
