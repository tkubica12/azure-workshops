# Demonstrating Browser Use
Showcase computer use agent on example of Browser Use project.

```powershell
# Install uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

uv venv --python 3.11
.venv\Scripts\activate
uv pip install browser-use
uv run playwright install