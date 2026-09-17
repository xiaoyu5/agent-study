"""与文件和命令行无关的课程模型及结构校验。"""

from dataclasses import dataclass
from graphlib import CycleError, TopologicalSorter


class CourseValidationError(ValueError):
    """课程不符合当前数据契约；不代表教学质量评价。"""


@dataclass(frozen=True)
class Source:
    id: str
    title: str
    url: str


@dataclass(frozen=True)
class Concept:
    id: str
    title: str
    prerequisites: tuple[str, ...]
    explanation: str
    source_ids: tuple[str, ...]
    misconceptions: tuple[str, ...]


@dataclass(frozen=True)
class Course:
    schema_version: str
    id: str
    version: str
    title: str
    audience: str
    prerequisites: tuple[str, ...]
    objectives: tuple[str, ...]
    sources: tuple[Source, ...]
    concepts: tuple[Concept, ...]
    review_status: str


def _object(value: object, path: str) -> dict:
    if not isinstance(value, dict):
        raise CourseValidationError(f"{path}: 必须是对象")
    return value


def _required(data: dict, key: str, path: str) -> object:
    if key not in data:
        raise CourseValidationError(f"{path}.{key}: 缺少必填字段")
    return data[key]


def _text(value: object, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CourseValidationError(f"{path}: 必须是非空字符串")
    return value


def _field_text(data: dict, key: str, path: str) -> str:
    return _text(_required(data, key, path), f"{path}.{key}")


def _list(data: dict, key: str, path: str, *, nonempty: bool = False) -> list:
    value = _required(data, key, path)
    if not isinstance(value, list):
        raise CourseValidationError(f"{path}.{key}: 必须是列表")
    if nonempty and not value:
        raise CourseValidationError(f"{path}.{key}: 列表不能为空")
    return value


def _texts(data: dict, key: str, path: str, *, nonempty: bool = False) -> tuple[str, ...]:
    values = _list(data, key, path, nonempty=nonempty)
    return tuple(_text(value, f"{path}.{key}[{index}]")
                 for index, value in enumerate(values))


def _unique_ids(items: tuple[Source, ...] | tuple[Concept, ...], path: str) -> set[str]:
    seen: set[str] = set()
    for item in items:
        if item.id in seen:
            raise CourseValidationError(f"{path}: 重复 id {item.id!r}")
        seen.add(item.id)
    return seen


def validate_course(value: object) -> Course:
    """解析并校验 schema v1，返回课程；不审核讲解正确性或教学效果。"""
    data = _object(value, "course")
    schema_version = _field_text(data, "schema_version", "course")
    if schema_version != "1":
        raise CourseValidationError("course.schema_version: 当前仅支持字符串 '1'")
    review_status = _field_text(data, "review_status", "course")
    if review_status != "draft":
        raise CourseValidationError("course.review_status: M0 仅支持 'draft'（待教学审核）")

    sources: list[Source] = []
    for index, value in enumerate(_list(data, "sources", "course", nonempty=True)):
        path = f"course.sources[{index}]"
        item = _object(value, path)
        sources.append(Source(
            id=_field_text(item, "id", path),
            title=_field_text(item, "title", path),
            url=_field_text(item, "url", path),
        ))

    concepts: list[Concept] = []
    for index, value in enumerate(_list(data, "concepts", "course", nonempty=True)):
        path = f"course.concepts[{index}]"
        item = _object(value, path)
        concepts.append(Concept(
            id=_field_text(item, "id", path),
            title=_field_text(item, "title", path),
            prerequisites=_texts(item, "prerequisites", path),
            explanation=_field_text(item, "explanation", path),
            source_ids=_texts(item, "source_ids", path, nonempty=True),
            misconceptions=_texts(item, "misconceptions", path),
        ))

    course = Course(
        schema_version=schema_version,
        id=_field_text(data, "id", "course"),
        version=_field_text(data, "version", "course"),
        title=_field_text(data, "title", "course"),
        audience=_field_text(data, "audience", "course"),
        prerequisites=_texts(data, "prerequisites", "course"),
        objectives=_texts(data, "objectives", "course", nonempty=True),
        sources=tuple(sources),
        concepts=tuple(concepts),
        review_status=review_status,
    )
    source_ids = _unique_ids(course.sources, "course.sources")
    concept_ids = _unique_ids(course.concepts, "course.concepts")
    for concept in course.concepts:
        for prerequisite in concept.prerequisites:
            if prerequisite not in concept_ids:
                raise CourseValidationError(
                    f"concept {concept.id!r}.prerequisites: 未知概念 {prerequisite!r}")
        for source_id in concept.source_ids:
            if source_id not in source_ids:
                raise CourseValidationError(
                    f"concept {concept.id!r}.source_ids: 未知来源 {source_id!r}")
    try:
        tuple(TopologicalSorter({concept.id: concept.prerequisites
                                 for concept in course.concepts}).static_order())
    except CycleError as error:
        cycle = " -> ".join(error.args[1])
        raise CourseValidationError(f"course.concepts: 前置依赖形成环：{cycle}") from error
    return course
