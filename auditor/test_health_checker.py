import unittest
import os
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from health_checker import HealthChecker

class TestHealthChecker(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    def test_readme_detection(self):
        checker = HealthChecker(self.test_dir)
        self.assertFalse(checker.has_readme())
        (Path(self.test_dir) / 'README.md').touch()
        self.assertTrue(checker.has_readme())
        os.remove(Path(self.test_dir) / 'README.md')
        (Path(self.test_dir) / 'readme.rst').touch()
        self.assertTrue(checker.has_readme())
    def test_tests_detection_directories(self):
        checker = HealthChecker(self.test_dir)
        self.assertFalse(checker.has_tests())
        (Path(self.test_dir) / 'tests').mkdir()
        self.assertTrue(checker.has_tests())
    def test_tests_detection_files(self):
        checker = HealthChecker(self.test_dir)
        (Path(self.test_dir) / 'main_test.go').touch()
        self.assertTrue(checker.has_tests())
        os.remove(Path(self.test_dir) / 'main_test.go')
        (Path(self.test_dir) / 'test_app.py').touch()
        self.assertTrue(checker.has_tests())
        os.remove(Path(self.test_dir) / 'test_app.py')
        (Path(self.test_dir) / 'app.test.js').touch()
        self.assertTrue(checker.has_tests())
        os.remove(Path(self.test_dir) / 'app.test.js')
        (Path(self.test_dir) / 'app.spec.ts').touch()
        self.assertTrue(checker.has_tests())
    def test_ci_github_workflows(self):
        checker = HealthChecker(self.test_dir)
        self.assertFalse(checker.has_ci()['exists'])
        wf_dir = Path(self.test_dir) / '.github' / 'workflows'
        wf_dir.mkdir(parents=True)
        wf_file = wf_dir / 'ci.yml'
        wf_file.write_text('name: CI')
        result = checker.has_ci()
        self.assertTrue(result['exists'])
        self.assertIn('github', result['details'])
    def test_ci_gitlab(self):
        checker = HealthChecker(self.test_dir)
        (Path(self.test_dir) / '.gitlab-ci.yml').touch()
        result = checker.has_ci()
        self.assertTrue(result['exists'])
        self.assertIn('gitlab', result['details'])
    def test_ci_circleci(self):
        checker = HealthChecker(self.test_dir)
        cc_dir = Path(self.test_dir) / '.circleci'
        cc_dir.mkdir()
        (cc_dir / 'config.yml').touch()
        result = checker.has_ci()
        self.assertTrue(result['exists'])
        self.assertIn('circleci', result['details'])
    def test_metadata_detection(self):
        checker = HealthChecker(self.test_dir)
        meta = checker.get_metadata()
        self.assertFalse(meta['package.json'])
        self.assertFalse(meta['go.mod'])
        (Path(self.test_dir) / 'package.json').touch()
        meta = checker.get_metadata()
        self.assertTrue(meta['package.json'])
    def test_ecosystem_detection(self):
        checker = HealthChecker(self.test_dir)
        meta = {'package.json': True, 'go.mod': False, 'setup.py': False, 'pyproject.toml': False, 'Cargo.toml': False, 'pom.xml': False}
        eco = checker.get_ecosystems(meta)
        self.assertIn('Node.js', eco)
        meta = {'package.json': False, 'go.mod': True, 'setup.py': False, 'pyproject.toml': False, 'Cargo.toml': False, 'pom.xml': False}
        eco = checker.get_ecosystems(meta)
        self.assertIn('Go', eco)
        meta_all_false = {k: False for k in meta.keys()}
        eco = checker.get_ecosystems(meta_all_false)
        self.assertEqual(['unidentified'], eco)
    def test_full_check_healthy_repo(self):
        (Path(self.test_dir) / 'README.md').touch()
        (Path(self.test_dir) / 'tests').mkdir()
        wf_dir = Path(self.test_dir) / '.github' / 'workflows'
        wf_dir.mkdir(parents=True)
        (wf_dir / 'test.yml').write_text('name: test')
        (Path(self.test_dir) / 'package.json').touch()
        checker = HealthChecker(self.test_dir)
        result = checker.check_all()
        self.assertTrue(result['readme'])
        self.assertTrue(result['tests'])
        self.assertTrue(result['ci'])
        self.assertFalse(result['no_metadata'])
        self.assertIn('Node.js', result['ecosystems'])
        self.assertEqual('4/4', result['score'])
    def test_full_check_unhealthy_repo(self):
        checker = HealthChecker(self.test_dir)
        result = checker.check_all()
        self.assertFalse(result['readme'])
        self.assertFalse(result['tests'])
        self.assertFalse(result['ci'])
        self.assertTrue(result['no_metadata'])
        self.assertEqual(['unidentified'], result['ecosystems'])
        self.assertEqual('0/4', result['score'])
    def test_partial_health(self):
        (Path(self.test_dir) / 'README.md').touch()
        (Path(self.test_dir) / 'go.mod').touch()
        checker = HealthChecker(self.test_dir)
        result = checker.check_all()
        self.assertTrue(result['readme'])
        self.assertFalse(result['tests'])
        self.assertFalse(result['ci'])
        self.assertFalse(result['no_metadata'])
        self.assertIn('Go', result['ecosystems'])
        self.assertEqual('2/4', result['score'])

if __name__ == '__main__':
    unittest.main()
