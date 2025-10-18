
param([ValidateSet("start","stop","restart","reindex")]$cmd="start")
$ROOT="C:\Agent"
$VENV="$ROOT\venv\Scripts\Activate.ps1"
$PIDFILE="$ROOT\logs\agent.pid"
if (!(Test-Path "$ROOT\logs")){ New-Item -ItemType Directory "$ROOT\logs" | Out-Null }
function Start-Agent {
  & $VENV
  $env:AGENT_CONFIG="$ROOT\config\config.example.json"
  $env:AGENT_LOG_DIR="$ROOT\logs"
  $env:AGENT_AUDIT_DIR="$ROOT\audit"
  Start-Process -FilePath "uvicorn" -ArgumentList "src.api.main:app --host 127.0.0.1 --port 8088 --log-level warning" -PassThru | % { $_.Id } | Out-File -Encoding ascii $PIDFILE
  Start-Process -FilePath "python" -ArgumentList "$ROOT\bin\hotkeys.py"
  Write-Host "Agent API on http://127.0.0.1:8088"
}
function Stop-Agent {
  if (Test-Path $PIDFILE){ Get-Content $PIDFILE | % { Stop-Process -Id $_ -ErrorAction SilentlyContinue }; Remove-Item $PIDFILE -Force }
  Get-Process -Name "python","uvicorn" -ErrorAction SilentlyContinue | ? {$_.Path -like "*\Agent\*"} | Stop-Process -Force -ErrorAction SilentlyContinue
}
if ($cmd -eq "start"){ Start-Agent }
elseif ($cmd -eq "stop"){ Stop-Agent }
elseif ($cmd -eq "restart"){ Stop-Agent; Start-Agent }
elseif ($cmd -eq "reindex"){ & $VENV; python "$ROOT\bin\reindex.py" }
