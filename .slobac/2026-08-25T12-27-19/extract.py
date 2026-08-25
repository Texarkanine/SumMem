import ast
from pathlib import Path

files = [
    "tests/test_nap.py",
    "tests/test_scopes.py",
    "tests/test_wake.py",
    "tests/test_store.py",
    "tests/test_version.py",
    "tests/test_proof_conflict.py",
    "tests/test_view.py",
    "tests/test_gitutil.py"
]

out = []
for f in files:
    p = Path("/home/mobaxterm/git/SumMem") / f
    tree = ast.parse(p.read_text())
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            doc = ast.get_docstring(node) or ""
            out.append({
                "file": f,
                "line": node.lineno,
                "name": node.name,
                "doc": doc
            })

import json
Path("/home/mobaxterm/git/SumMem/.slobac/2026-08-25T12-27-19/tests.json").write_text(json.dumps(out, indent=2))
