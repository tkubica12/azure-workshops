#!/bin/bash
# install.sh - Smart PyTorch installation script

if [[ "$PYTORCH_VARIANT" == "gpu" ]] || command -v nvidia-smi &> /dev/null; then
    echo "Installing GPU version..."
    uv sync --extra gpu-cuda128
else
    echo "Installing CPU version..."
    uv sync --extra cpu
fi
