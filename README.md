A [pre-commit](http://pre-commit.com) hook to check your Python dependencies against [safety-db](//github.com/pyupio/safety-db).

It checks all files in your current venv or a requirements file if you supply it.

## Usage
```
-   repo: https://github.com/Galdanwing/pre-commit-hooks-safety
    sha: v1.0.0
    hooks:
    -   id: python-safety-dependencies-check
        args: [exclude, bleach]
```


## Alternative local hook
You'll need to `pip install safety` beforehand:
```
-   repo: local
    hooks:
    -   id: python-safety-dependencies-check
        entry: safety
        args: [check, --full-report]
        language: system
        files: requirements
```
