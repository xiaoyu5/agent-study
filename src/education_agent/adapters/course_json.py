"""从本地 UTF-8 JSON 文件读取并校验课程。"""

import json
from pathlib import Path

from education_agent.domain import Course, validate_course


class CourseLoadError(ValueError):
    """课程文件无法读取或不是有效的 UTF-8 JSON。"""


def load_course(path: str | Path) -> Course:
    path = Path(path)
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise CourseLoadError(f"{path}: 不是有效的 UTF-8 文件") from error
    except OSError as error:
        raise CourseLoadError(f"{path}: 无法读取课程文件（{error.strerror}）") from error
    try:
        data = json.loads(content)
    except json.JSONDecodeError as error:
        raise CourseLoadError(
            f"{path}: JSON 格式错误，第 {error.lineno} 行第 {error.colno} 列"
        ) from error
    return validate_course(data)
