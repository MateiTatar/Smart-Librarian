# Prompt for OpenAI API key and save to a local .env (gitignored)
param()

$pwd = Get-Location
$envPath = Join-Path $pwd '.env'
if (Test-Path $envPath) {
    Write-Host ".env already exists at $envPath. Overwrite? (y/N)" -NoNewline
    $ans = Read-Host
    if ($ans -ne 'y' -and $ans -ne 'Y') {
        Write-Host "Aborted. No changes made."
        exit 0
    }
}

$key = Read-Host -AsSecureString "Introduceți OPENAI API KEY (va fi salvat în .env)"
$keyPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($key))

"OPENAI_API_KEY=$keyPlain" | Out-File -Encoding utf8 -FilePath $envPath -Force
Write-Host ".env creat la: $envPath (contine OPENAI_API_KEY)."
Write-Host ".env este in .gitignore - nu va fi comis accidental."

