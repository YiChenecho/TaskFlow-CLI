# TaskFlow CLI

这是一个极简的 Python 命令行待办事项项目，支持：

- 添加任务
- 列出任务
- 标记任务完成
- 删除任务

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
python app.py list
```

## 使用方式

```bash
python app.py add "学习 Git"
python app.py list
python app.py done 1
python app.py delete 1
```

数据会保存在当前目录的 `tasks.json` 文件中。
