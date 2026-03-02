#!/bin/bash
# Hook: PostToolUse — Lint and validate after notebook modifications
# This hook runs after Write/Edit operations on .ipynb files.
# It checks for common notebook issues.

# Read the JSON input from stdin
INPUT=$(cat)

# Extract tool name and file path
TOOL=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; inp=json.load(sys.stdin); print(inp.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

# Only check Write/Edit operations on notebooks
if [[ "$TOOL" != "Write" && "$TOOL" != "Edit" && "$TOOL" != "NotebookEdit" ]]; then
    exit 0
fi

case "$FILE_PATH" in
    *.ipynb)
        # Validate JSON structure
        if [ -f "$FILE_PATH" ]; then
            python3 -c "
import json, sys

with open('$FILE_PATH', 'r') as f:
    try:
        nb = json.load(f)
    except json.JSONDecodeError:
        print('ERROR: Notebook is not valid JSON after edit')
        sys.exit(1)

# Check for cells without source
issues = []
for i, cell in enumerate(nb.get('cells', [])):
    if 'source' not in cell:
        issues.append(f'Cell {i} has no source field')
    if cell.get('cell_type') == 'code':
        source = ''.join(cell.get('source', []))
        # Warn about common issues
        if 'import *' in source:
            issues.append(f'Cell {i}: Avoid wildcard imports (import *)')
        if 'password' in source.lower() or 'secret' in source.lower():
            issues.append(f'Cell {i}: Possible sensitive data in code')

if issues:
    print('Notebook lint warnings:')
    for issue in issues:
        print(f'  - {issue}')
else:
    print('Notebook validation passed.')
" 2>&1
        fi
        ;;
esac
