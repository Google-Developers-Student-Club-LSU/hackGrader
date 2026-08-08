param (
  [switch]$c = $false
  [switch]$l = $false
  [switch]$a = $true
)

source .venv/source/Activate.ps1
if ($c) {
  python tests/test_crawling.py 
} elseif ($l) {
  python tests/test_scoring.py 
} elseif ($a)
  python tests/test_pipeline.py 
}
