# install.ps1 - Smart PyTorch installation script for Windows

if ($env:PYTORCH_VARIANT -eq "gpu" -or (Get-Command nvidia-smi -ErrorAction SilentlyContinue)) {
    Write-Host "Installing GPU version..."
    uv sync --extra gpu-cuda128
} else {
    Write-Host "Installing CPU version..."
    uv sync --extra cpu
}
