import argparse
import json
from pathlib import Path

DATA_FILE = Path("tasks.json")


def load_tasks() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_tasks(tasks: list[dict]) -> None:
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def add_task(title: str) -> None:
    tasks = load_tasks()
    next_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({"id": next_id, "title": title, "done": False})
    save_tasks(tasks)
    print(f"已添加任务 #{next_id}: {title}")


def list_tasks() -> None:
    tasks = load_tasks()
    if not tasks:
        print("暂无任务")
        return
    for task in tasks:
        status = "✅" if task["done"] else "⬜"
        print(f"{task['id']:>3}. {status} {task['title']}")


def mark_done(task_id: int) -> None:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"任务 #{task_id} 已完成")
            return
    print(f"未找到任务 #{task_id}")


def delete_task(task_id: int) -> None:
    tasks = load_tasks()
    filtered = [t for t in tasks if t["id"] != task_id]
    if len(filtered) == len(tasks):
        print(f"未找到任务 #{task_id}")
        return
    save_tasks(filtered)
    print(f"任务 #{task_id} 已删除")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TaskFlow CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="添加任务")
    p_add.add_argument("title", help="任务标题")

    sub.add_parser("list", help="列出任务")

    p_done = sub.add_parser("done", help="标记完成")
    p_done.add_argument("task_id", type=int, help="任务 ID")

    p_delete = sub.add_parser("delete", help="删除任务")
    p_delete.add_argument("task_id", type=int, help="任务 ID")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        mark_done(args.task_id)
    elif args.command == "delete":
        delete_task(args.task_id)


if __name__ == "__main__":
    main()
