#!/bin/bash

source .venv/bin/activate

if [ $# -eq 0 ]; then
  python tests/test_pipeline.py > log.txt
  exit 0
fi

while getopts ":sc" opt; do
  case $opt in
    s)
      python tests/test_scoring.py
      ;;
    c)
      python tests/test_crawling.py
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done
