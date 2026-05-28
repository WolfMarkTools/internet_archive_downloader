# Build a flat extension folder for "Load unpacked" on Windows (ZIP / no symlinks).
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Source = if ($args.Count -ge 1) { $args[0] } else { "isrc" }
$SourcePath = Join-Path $RepoRoot $Source
if (-not (Test-Path $SourcePath -PathType Container)) {
    Write-Error "Source not found: $SourcePath"
}
$Out = Join-Path $RepoRoot "build" "$Source-unpacked"
if (Test-Path $Out) { Remove-Item $Out -Recurse -Force }
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $py) {
    Write-Error "Python 3 is required. Install Python or run: py scripts/prepare_unpacked.py"
}
& $py.Source (Join-Path $RepoRoot "scripts" "prepare_unpacked.py") $Source -o $Out
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
