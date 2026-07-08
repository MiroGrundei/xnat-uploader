import tempfile
import unittest
import zipfile
from pathlib import Path

from xnat_upload import build_parser, require_file


class FileValidationTests(unittest.TestCase):
    def test_accepts_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "events.tsv"
            file_path.write_text("onset\tduration\n", encoding="utf-8")

            self.assertEqual(require_file(str(file_path)), file_path)

    def test_rejects_missing_file(self):
        with self.assertRaisesRegex(ValueError, "does not exist"):
            require_file("missing-file.tsv")

    def test_requires_valid_zip_for_scan(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "scan.zip"
            file_path.write_text("not a zip", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "valid ZIP"):
                require_file(str(file_path), zip_only=True)

    def test_accepts_valid_scan_zip(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "scan.zip"
            with zipfile.ZipFile(file_path, "w") as archive:
                archive.writestr("scan.dcm", "example")

            self.assertEqual(
                require_file(str(file_path), zip_only=True), file_path
            )


class ArgumentTests(unittest.TestCase):
    def test_parses_experiment_resource_upload(self):
        args = build_parser().parse_args(
            [
                "resource",
                "events.tsv",
                "--project",
                "DEMO",
                "--subject",
                "1001",
                "--experiment",
                "1001_01",
                "--resource",
                "beh",
            ]
        )

        self.assertEqual(args.command, "resource")
        self.assertEqual(args.resource, "beh")


if __name__ == "__main__":
    unittest.main()
