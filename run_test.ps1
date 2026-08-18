param (
  [switch]$c,
  [switch]$s
)

$hasUv = [bool](Get-Command "uv" -ErrorAction SilentlyContinue)

if (-not $c -and -not $s) {
  if ($hasUv) {
    uv run pytest -sv tests/test_pipeline.py > log.txt
  } else {
    python tests/test_pipeline.py > log.txt
  }
  exit
}

if ($c) {
  if ($hasUv) {
    uv run pytest -sv tests/test_crawling.py
  } else {
    python tests/test_crawling.py
  }
} 

if ($s) {
  if ($hasUv) {
    uv run pytest -sv tests/test_scoring.py
  } else {
    python tests/test_scoring.py
  }
}