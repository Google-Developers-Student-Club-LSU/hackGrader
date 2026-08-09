#!/bin/bash
 
source .venv/bin/activate
while getopts ":sc:" opt; do
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
    :)
      python tests/test_pipeline.py
      ;;
  esac
done

