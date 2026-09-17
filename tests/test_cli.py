import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSE_PATH = ROOT / "courses" / "bayes-intro" / "course.json"


class CliTests(unittest.TestCase):
    def run_cli(self, *arguments):
        environment = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
        return subprocess.run(
            [sys.executable, "-m", "education_agent", *map(str, arguments)],
            cwd=ROOT, env=environment, capture_output=True, text=True,
            encoding="utf-8", timeout=10,
        )

    def test_commands_show_draft_status_without_claiming_teaching_approval(self):
        for command in ("inspect-course", "validate-course"):
            with self.subTest(command=command):
                result = self.run_cli(command, COURSE_PATH)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("bayes-intro", result.stdout)
                self.assertIn("review_status: draft", result.stdout)
                self.assertIn("教学内容尚未审核", result.stdout)
                self.assertEqual(result.stderr, "")
                if command == "inspect-course":
                    self.assertIn("[posterior]", result.stdout)
                    self.assertIn("https://ocw.mit.edu", result.stdout)
                else:
                    self.assertIn("结构校验通过", result.stdout)

    def test_invalid_course_exits_nonzero_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text("{}", encoding="utf-8")
            result = self.run_cli("validate-course", path)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, "")
            self.assertIn("缺少必填字段", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_missing_file_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_cli("inspect-course", Path(directory) / "missing.json")
            self.assertEqual(result.returncode, 1)
            self.assertIn("无法读取课程文件", result.stderr)

    def test_command_requires_an_explicit_path(self):
        result = self.run_cli("validate-course")
        self.assertEqual(result.returncode, 2)
        self.assertIn("PATH", result.stderr)


if __name__ == "__main__":
    unittest.main()
