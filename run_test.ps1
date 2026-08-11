param (
  [switch]$c,
  [switch]$s
)

. .venv/bin/activate.ps1

if (-not $c -and -not $s) {
  python tests/test_pipeline.py 
  exit
}

if ($c) {
  python tests/test_crawling.py 
} 

if ($s) {
  python tests/test_scoring.py 
}
