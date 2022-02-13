#!/bin/bash
target=$1
isort $target
black $target
mypy --strict $target
flake8 $target
