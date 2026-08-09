param (
  [switch]$c = $false
  [switch]$s = $false
  [switch]$a = $true
)

source .venv/bin/activate.ps1
if ($c) {
  python tests/test_crawling.py 
} elseif ($s) {
  python tests/test_scoring.py 
} elseif ($a)
  python tests/test_pipeline.py 
}

