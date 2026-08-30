import os
import sys
import json
import argparse
from pathlib import Path

METADATA_MAP = {
    'package.json': 'Node.js',
    'pyproject.toml': 'Python',
    'setup.py': 'Python',
    'go.mod': 'Go',
    'Cargo.toml': 'Rust',
    'pom.xml': 'Java'
}

class HealthChecker:
    def __init__(self, path):
        self.path = Path(path).resolve()
        if not self.path.is_dir():
            raise ValueError("Not a directory")
    
    def has_readme(self):
        for f in self.path.iterdir():
            if f.is_file():
                name = f.name.lower()
                if name in ['readme', 'readme.md', 'readme.rst', 'readme.txt']:
                    return True
        return False
    
    def has_tests(self):
        test_dirs = ['test', 'tests', '__tests__']
        for td in test_dirs:
            if (self.path / td).is_dir():
                return True
        
        for root, dirs, files in os.walk(self.path):
            for f in files:
                fl = f.lower()
                if fl.endswith('_test.go'):
                    return True
                if fl.startswith('test_') and fl.endswith('.py'):
                    return True
                if '.test.' in fl or '.spec.' in fl:
                    return True
        return False
    
    def has_ci(self):
        found = False
        details = {}
        
        wf = self.path / '.github' / 'workflows'
        if wf.is_dir():
            ymls = [x for x in wf.iterdir() if x.is_file() and x.suffix in ['.yml', '.yaml'] and x.stat().st_size > 0]
            if ymls:
                found = True
                details['github'] = [x.name for x in ymls]
        
        others = [
            ('.gitlab-ci.yml', 'gitlab'),
            ('.circleci/config.yml', 'circleci'),
            ('Jenkinsfile', 'jenkins')
        ]
        for fpath, key in others:
            if (self.path / fpath).is_file():
                found = True
                details[key] = fpath
        
        return {'exists': found, 'details': details}
    
    def get_metadata(self):
        result = {}
        for mf in METADATA_MAP.keys():
            result[mf] = (self.path / mf).is_file()
        return result
    
    def get_ecosystems(self, metadata):
        eco = []
        for f, exists in metadata.items():
            if exists and f in METADATA_MAP:
                e = METADATA_MAP[f]
                if e not in eco:
                    eco.append(e)
        return eco if eco else ['unidentified']
    
    def check_all(self):
        readme = self.has_readme()
        tests = self.has_tests()
        ci = self.has_ci()
        meta = self.get_metadata()
        eco = self.get_ecosystems(meta)
        
        no_meta = not any(meta.values())
        passed = sum([readme, tests, ci['exists'], not no_meta])
        
        return {
            'path': str(self.path),
            'readme': readme,
            'tests': tests,
            'ci': ci['exists'],
            'ci_details': ci['details'],
            'metadata': meta,
            'no_metadata': no_meta,
            'ecosystems': eco,
            'score': f"{passed}/4"
        }

def to_json(data):
    return json.dumps(data, indent=2)

def to_text(data):
    out = []
    out.append("=" * 60)
    out.append("Repository Health Report")
    out.append("=" * 60)
    out.append(f"Path: {data['path']}")
    out.append("")
    out.append(f"README: {'YES' if data['readme'] else 'NO'}")
    out.append(f"Tests: {'YES' if data['tests'] else 'NO'}")
    out.append(f"CI Config: {'YES' if data['ci'] else 'NO'}")
    
    if data['ci'] and data['ci_details']:
        for k, v in data['ci_details'].items():
            if isinstance(v, list):
                out.append(f"  {k}: {', '.join(v)}")
            else:
                out.append(f"  {k}: {v}")
    
    out.append(f"Metadata: {'MISSING' if data['no_metadata'] else 'FOUND'}")
    if not data['no_metadata']:
        for f, exists in data['metadata'].items():
            if exists:
                out.append(f"  {f}")
    
    out.append(f"Ecosystems: {', '.join(data['ecosystems'])}")
    out.append("")
    out.append(f"Health Score: {data['score']}")
    out.append("=" * 60)
    return "

def to_markdown(data):
    out = []
    out.append("# Repository Health Report")
    out.append("")
    out.append(f"**Path:** `{data['path']}`")
    out.append("")
    out.append("## Checks")
    out.append("")
    out.append(f"- README: {'✅' if data['readme'] else '❌'}")
    out.append(f"- Tests: {'✅' if data['tests'] else '❌'}")
    out.append(f"- CI Config: {'✅' if data['ci'] else '❌'}")
    
    if data['ci'] and data['ci_details']:
        for k, v in data['ci_details'].items():
            if isinstance(v, list):
                out.append(f"  - {k}: {', '.join(v)}")
            else:
                out.append(f"  - {k}: {v}")
    
    out.append(f"- Metadata: {'✅' if not data['no_metadata'] else '❌'}")
    if not data['no_metadata']:
        for f, exists in data['metadata'].items():
            if exists:
                out.append(f"  - `{f}`")
    
    out.append("")
    out.append("## Ecosystems")
    out.append("")
    for e in data['ecosystems']:
        out.append(f"- {e}")
    
    out.append("")
    out.append(f"**Health Score:** {data['score']}")
    return "

def run():
    parser = argparse.ArgumentParser(description='Check repository health')
    parser.add_argument('repo_path', help='Repository directory path')
    parser.add_argument('-f', '--format', choices=['json', 'text', 'markdown'], default='text', help='Output format')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    
    args = parser.parse_args()
    
    try:
        checker = HealthChecker(args.repo_path)
        result = checker.check_all()
        
        if args.format == 'json':
            output = to_json(result)
        elif args.format == 'markdown':
            output = to_markdown(result)
        else:
            output = to_text(result)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Written to: {args.output}")
        else:
            print(output)
        
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(run())
