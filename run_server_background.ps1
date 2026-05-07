$env:PYTHONPATH = Join-Path $PSScriptRoot '.deps'
Set-Location $PSScriptRoot
& 'C:\Users\plato\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'main.py' *> 'server.log'

