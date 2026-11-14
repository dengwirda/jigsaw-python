import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

import setuptools


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(
    int(setuptools.__version__.split(".")[0]) >= 77,
    "source distribution metadata requires setuptools 77 or newer")
class SourceDistributionTests(unittest.TestCase):
    def test_archive_and_legacy_build_helper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "source"
            root.mkdir()
            for name in ("MANIFEST.in", "README.md", "LICENSE.md",
                         "build.py", "example.py", "pyproject.toml",
                         "setup.cfg", "setup.py"):
                shutil.copyfile(str(ROOT / name), str(root / name))

            for name in ("jigsawpy/__init__.py",
                         "external/jigsaw/CMakeLists.txt",
                         "external/jigsaw/bin/jigsaw",
                         "external/jigsaw/lib/libjigsaw.so",
                         "jigsawpy/_bin/jigsaw",
                         "jigsawpy/_lib/libjigsaw.so"):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("")

            result = subprocess.run(
                [sys.executable, "setup.py", "sdist"], cwd=str(root),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True)
            self.assertEqual(result.returncode, 0, result.stderr)

            archive = next((root / "dist").glob("*.tar.gz"))
            with tarfile.open(str(archive)) as tar:
                names = tar.getnames()
                prefix = names[0].split("/")[0] + "/"
                files = {name[len(prefix):] for name in names
                         if name.startswith(prefix)}
                self.assertIn("build.py", files)
                self.assertIn("external/jigsaw/CMakeLists.txt", files)
                for name in ("external/jigsaw/bin/jigsaw",
                             "external/jigsaw/lib/libjigsaw.so",
                             "jigsawpy/_bin/jigsaw",
                             "jigsawpy/_lib/libjigsaw.so"):
                    self.assertNotIn(name, files)
                unpacked = Path(tmp) / "unpacked"
                unpacked.mkdir()
                for name in ("setup.py", "pyproject.toml", "README.md",
                             "LICENSE.md", "build.py"):
                    (unpacked / name).write_bytes(
                        tar.extractfile(prefix + name).read())

            (unpacked / "build.py").write_text(
                "def build_external():\n"
                "    print('local build helper invoked')\n")
            script = (
                "import runpy, sys, types; "
                "sys.modules['build'] = types.ModuleType('build'); "
                "sys.argv = ['setup.py', 'build_external']; "
                "runpy.run_path('setup.py', run_name='__main__')"
            )
            result = subprocess.run(
                [sys.executable, "-c", script], cwd=str(unpacked),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("local build helper invoked", result.stdout)


if __name__ == "__main__":
    unittest.main()
