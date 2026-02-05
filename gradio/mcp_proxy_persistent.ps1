Write-Host "========================================" -ForegroundColor Cyan
Write-Host "MCP Proxy (Persistent PowerShell)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "This proxy will stay alive for Continue" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to exit" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

while ($true) {
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] Starting mcp-remote proxy..." -ForegroundColor Green
    
    try {
        # Start mcp-remote
        $process = Start-Process -FilePath "npx" `
            -ArgumentList @("-y", "mcp-remote@latest", "http://127.0.0.1:8000/mcp", "--transport", "sse-only", "--verbose") `
            -NoNewWindow -PassThru -RedirectStandardOutput "proxy_log.txt"
        
        # Wait for it to exit
        $process.WaitForExit()
        
        $timestamp = Get-Date -Format "HH:mm:ss"
        Write-Host "[$timestamp] Proxy stopped. Exit code: $($process.ExitCode)" -ForegroundColor Yellow
        
        if ($process.ExitCode -eq 0) {
            Write-Host "[$timestamp] Normal exit, not restarting." -ForegroundColor Green
            break
        }
        
        Write-Host "[$timestamp] Restarting in 3 seconds..." -ForegroundColor Yellow
        Start-Sleep -Seconds 3
        
    } catch {
        Write-Host "[ERROR] $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Restarting in 5 seconds..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
    }
}

Write-Host "Proxy stopped permanently." -ForegroundColor Cyan
Read-Host "Press Enter to close"