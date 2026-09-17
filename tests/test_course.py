import copy
import json
import tempfile
import unittest
from pathlib import Path

from education_agent.adapters.course_json import CourseLoadError, load_course
from education_agent.domain import CourseValidationError, validate_course


ROOT = Path(__file__).resolve().parents[1]
COURSE_PATH = ROOT / "courses" / "bayes-intro" / "course.json"


class CourseTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(COURSE_PATH.read_text(encoding="utf-8"))

    def test_real_course_preserves_concept_order_and_draft_status(self):
        course = load_course(COURSE_PATH)
        self.assertEqual(course.id, "bayes-intro")
        self.assertEqual(course.review_status, "draft")
        self.assertEqual([concept.id for concept in course.concepts],
                         ["prior", "likelihood", "posterior"])
        self.assertEqual(course.concepts[-1].prerequisites, ("prior", "likelihood"))

    def test_each_required_course_field_is_checked(self):
        for key in self.data:
            with self.subTest(key=key):
                data = copy.deepcopy(self.data)
                del data[key]
                with self.assertRaisesRegex(CourseValidationError, f"course.{key}"):
                    validate_course(data)

    def test_nested_fields_are_required(self):
        for collection, field in (("sources", "url"), ("concepts", "explanation")):
            with self.subTest(collection=collection, field=field):
                data = copy.deepcopy(self.data)
                del data[collection][0][field]
                with self.assertRaisesRegex(CourseValidationError, "缺少必填字段"):
                    validate_course(data)

    def test_wrong_types_and_empty_required_values_are_rejected(self):
        cases = (
            ("title", 123), ("audience", "  "), ("prerequisites", "百分比"),
            ("objectives", [False]), ("objectives", []), ("sources", []),
            ("sources", ["not an object"]), ("concepts", {}),
            ("schema_version", 1), ("schema_version", "2"),
            ("review_status", "approved"),
        )
        for key, value in cases:
            with self.subTest(key=key, value=value):
                data = copy.deepcopy(self.data)
                data[key] = value
                with self.assertRaises(CourseValidationError):
                    validate_course(data)
        with self.assertRaisesRegex(CourseValidationError, "必须是对象"):
            validate_course([])

    def test_concept_fields_are_typed(self):
        for field, value in (("prerequisites", [1]), ("source_ids", "mit-18-05"),
                             ("source_ids", []), ("misconceptions", [None])):
            with self.subTest(field=field, value=value):
                data = copy.deepcopy(self.data)
                data["concepts"][0][field] = value
                with self.assertRaises(CourseValidationError):
                    validate_course(data)

    def test_duplicate_ids_are_rejected(self):
        for collection in ("sources", "concepts"):
            with self.subTest(collection=collection):
                data = copy.deepcopy(self.data)
                data[collection].append(copy.deepcopy(data[collection][0]))
                with self.assertRaisesRegex(CourseValidationError, "重复 id"):
                    validate_course(data)

    def test_unknown_concept_and_source_references_are_rejected(self):
        for field in ("prerequisites", "source_ids"):
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data["concepts"][0][field] = ["missing-id"]
                with self.assertRaisesRegex(CourseValidationError, "missing-id"):
                    validate_course(data)

    def test_dependency_cycles_are_rejected(self):
        for dependency in ("prior", "posterior"):
            with self.subTest(dependency=dependency):
                data = copy.deepcopy(self.data)
                data["concepts"][0]["prerequisites"] = [dependency]
                with self.assertRaisesRegex(CourseValidationError, "前置依赖形成环"):
                    validate_course(data)

    def test_forward_references_are_valid_without_reordering_the_course(self):
        self.data["concepts"].reverse()
        course = validate_course(self.data)
        self.assertEqual(course.concepts[0].id, "posterior")

    def test_file_errors_are_clear(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "course.json"
            with self.assertRaisesRegex(CourseLoadError, "无法读取课程文件"):
                load_course(path)
            path.write_bytes(b"\xff")
            with self.assertRaisesRegex(CourseLoadError, "不是有效的 UTF-8"):
                load_course(path)
            path.write_text('{"title":\n}', encoding="utf-8")
            with self.assertRaisesRegex(CourseLoadError, "JSON 格式错误，第 2 行"):
                load_course(path)


if __name__ == "__main__":
    unittest.main()
