# pyproject.toml  (at project root)
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "my_plecs_project"
version = "0.1.0"

[tool.setuptools.packages.find]
where = ["."]
include = ["Script*"]