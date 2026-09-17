"""M0 的课程检查命令；只读取本地课程。"""

import argparse
import sys
from collections.abc import Sequence

from education_agent.adapters.course_json import CourseLoadError, load_course
from education_agent.domain import Course, CourseValidationError


def _show_review_status(course: Course) -> None:
    print(f"review_status: {course.review_status}（教学内容尚未审核）")


def _inspect(course: Course) -> None:
    print(f"课程：{course.title}")
    print(f"id: {course.id} | version: {course.version} | schema_version: {course.schema_version}")
    _show_review_status(course)
    print(f"适用人群：{course.audience}")
    print("先修知识：" + ("；".join(course.prerequisites) or "无"))
    print("学习目标：")
    for objective in course.objectives:
        print(f"  - {objective}")
    print("概念（按课程文件顺序）：")
    for concept in course.concepts:
        dependencies = ", ".join(concept.prerequisites) or "无"
        print(f"  [{concept.id}] {concept.title} | 前置概念：{dependencies}")
        print(f"    {concept.explanation}")
        print(f"    参考来源：{', '.join(concept.source_ids)}")
        for misconception in concept.misconceptions:
            print(f"    常见误解：{misconception}")
    print("参考资料（链接仅供查阅，结构校验不验证外部内容）：")
    for source in course.sources:
        print(f"  [{source.id}] {source.title}\n    {source.url}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="教育 Agent M0：本地课程结构检查")
    commands = parser.add_subparsers(dest="command", required=True)
    for name, description in (
        ("inspect-course", "展示课程、概念依赖与教学审核状态"),
        ("validate-course", "校验课程结构；不代表教学审核通过"),
    ):
        command = commands.add_parser(name, help=description, description=description)
        command.add_argument("path", metavar="PATH", help="本地 UTF-8 课程 JSON 路径")
    args = parser.parse_args(argv)
    try:
        course = load_course(args.path)
    except (CourseLoadError, CourseValidationError) as error:
        print(f"错误：{error}", file=sys.stderr)
        return 1
    if args.command == "inspect-course":
        _inspect(course)
    else:
        print(f"结构校验通过：{course.id} v{course.version}")
        print(f"概念：{len(course.concepts)} | 参考资料：{len(course.sources)}")
        _show_review_status(course)
    return 0
