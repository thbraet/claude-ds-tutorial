#!/bin/bash
# Hook: PreToolUse — Validate data file access
# This hook runs before any Read tool that accesses data files.
# It warns about reading very large files and blocks access to restricted paths.

# Read the JSON input from stdin
INPUT=$(cat)

# Extract the tool name and file path
TOOL=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; inp=json.load(sys.stdin); print(inp.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

# Only check Read operations on data files
if [ "$TOOL" != "Read" ] || [ -z "$FILE_PATH" ]; then
    echo '{"decision": "approve"}'
    exit 0
fi

# Check if this is a data file
case "$FILE_PATH" in
    *data/raw/*|*data/processed/*|*data/external/*)
        # Check file size (warn if > 100MB)
        if [ -f "$FILE_PATH" ]; then
            FILE_SIZE=$(stat -f%z "$FILE_PATH" 2>/dev/null || stat -c%s "$FILE_PATH" 2>/dev/null || echo "0")
            if [ "$FILE_SIZE" -gt 104857600 ]; then
                echo "{\"decision\": \"approve\", \"message\": \"WARNING: File is $(( FILE_SIZE / 1048576 ))MB. Consider using DuckDB MCP or pandas to read specific columns/rows instead of loading the entire file.\"}"
                exit 0
            fi
        fi
        ;;
    *.env|*credentials*|*secret*|*password*)
        # Block access to sensitive files
        echo '{"decision": "deny", "reason": "Access to sensitive files (.env, credentials) is blocked by the validate-data-load hook."}'
        exit 0
        ;;
esac

# Default: approve
echo '{"decision": "approve"}'
