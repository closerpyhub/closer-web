param(
    [ValidateRange(1024, 65535)]
    [int]$Port = 8765
)

$ErrorActionPreference = 'Stop'
$siteRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$previewUrl = "http://127.0.0.1:$Port/"
$listener = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($listener) {
    throw "El puerto $Port ya esta ocupado (PID $($listener.OwningProcess -join ', ')). No se ha interrumpido ese proceso."
}

$pythonPath = (& python -c 'import sys; print(sys.executable)').Trim()
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $pythonPath)) {
    throw 'No se encontro un interprete Python disponible.'
}
$outputLog = Join-Path $env:TEMP "closer-web-preview-$Port.stdout.log"
$errorLog = Join-Path $env:TEMP "closer-web-preview-$Port.stderr.log"
$serverArgs = @('-u', '-m', 'http.server', "$Port", '--bind', '127.0.0.1', '--directory', "`"$siteRoot`"")

# File-backed streams keep the server independent of a temporary agent terminal.
$server = Start-Process -FilePath $pythonPath -ArgumentList $serverArgs -WorkingDirectory $siteRoot -WindowStyle Hidden -RedirectStandardOutput $outputLog -RedirectStandardError $errorLog -PassThru
for ($attempt = 0; $attempt -lt 10; $attempt++) {
    if ($server.HasExited) {
        throw "El servidor se cerro. Revisar $errorLog"
    }
    try {
        $response = Invoke-WebRequest -Uri $previewUrl -UseBasicParsing -TimeoutSec 2
        if ($response.StatusCode -eq 200) {
            Write-Output "Vista previa: $previewUrl"
            Write-Output "PID: $($server.Id)"
            Write-Output "Registro: $errorLog"
            return
        }
    } catch {
        Start-Sleep -Milliseconds 200
    }
}
throw "El servidor no respondio. Revisar el PID $($server.Id) y $errorLog"
