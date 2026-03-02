# Chapter 7: Personalization Deep-Dive

This chapter is your comprehensive reference for customizing Claude Code to fit your own projects, your own industry, and your own team's workflow. Unlike the previous chapters that followed the CRISP-DM cycle with our retail forecasting project, this one is a standalone guide you will come back to again and again.

Every section follows the same pattern: **what the feature is**, **how it works under the hood**, and **step-by-step instructions to build your own**.

---

## Section 1: Modifying Skills

### What Skills Are (Recap)

Skills are markdown files that give Claude domain-specific knowledge. They live in `.claude/skills/<skill-name>/SKILL.md` and activate automatically when Claude detects that your conversation matches the skill's description.

In this tutorial, you have been using three skills:
- `crisp-dm-guide` -- CRISP-DM methodology guidance
- `retail-domain` -- Retail and grocery domain knowledge
- `data-validation` -- Data quality checking patterns

### How Skill Auto-Triggering Works

When you send a message to Claude Code, it scans the first ~100 tokens of your message and compares them against each skill's `description` field in the frontmatter. If there is a semantic match, the skill's content is loaded into context automatically.

For example, the `retail-domain` skill has this frontmatter:

```yaml
---
name: retail-domain
description: "Retail and grocery domain knowledge for data science.
Activates when working with store sales, product categories, promotions,
inventory, supply chain, or grocery retail concepts."
---
```

When you ask Claude about "sales by product family" or "promotion uplift," the description matches and the skill activates. You do not need to explicitly request it.

### Step-by-Step: Fork and Customize a Skill

Let us adapt the `retail-domain` skill for a different industry. We will create three examples: healthcare, finance, and logistics.

#### Example: Healthcare Domain Skill

Create `.claude/skills/healthcare-domain/SKILL.md`:

```markdown
---
name: healthcare-domain
description: "Healthcare and clinical domain knowledge for data science.
Activates when working with patient data, clinical outcomes, diagnoses,
treatments, hospital operations, or medical terminology."
---

# Healthcare Domain Knowledge

## Instructions

Apply healthcare-specific domain knowledge when working on clinical
or hospital data science problems.

### Key Healthcare KPIs

- **Length of Stay (LOS)** -- Average days per hospital admission
- **Readmission Rate** -- Percentage of patients readmitted within 30 days
- **Mortality Rate** -- Deaths per 1,000 patients for specific conditions
- **Patient Satisfaction (HCAHPS)** -- Standardized survey scores
- **Bed Occupancy Rate** -- Percentage of available beds in use
- **Average Cost per Case** -- Total cost divided by discharges
- **ED Wait Time** -- Average minutes from arrival to first provider contact
- **Surgical Site Infection Rate** -- Infections per 100 surgical procedures

### Common Data Patterns in Healthcare

- **Seasonality**: Flu season spikes (Nov-Mar), summer trauma increases
- **Day of week effects**: Elective procedures cluster Mon-Thu;
  weekend admissions are often more acute
- **Coding variability**: Same condition may be coded differently across
  providers (ICD-10 specificity varies)
- **Missing data**: Clinical data is notoriously incomplete --
  missing labs often mean "not ordered" rather than "not recorded"
- **Class imbalance**: Adverse events (readmission, mortality) are rare
  relative to normal outcomes

### Regulatory Considerations

Alert the user to these constraints:
- **HIPAA**: Never include PHI (Protected Health Information) in outputs,
  logs, or commits. Flag any column that could be an identifier.
- **De-identification**: Dates must be shifted, ages >89 grouped,
  ZIP codes truncated to 3 digits
- **Audit trail**: All data access and transformations must be logged
  for compliance
```

#### Example: Finance Domain Skill

Create `.claude/skills/finance-domain/SKILL.md`:

```markdown
---
name: finance-domain
description: "Financial services domain knowledge for data science.
Activates when working with transactions, credit risk, fraud detection,
portfolio analysis, or financial time series."
---

# Finance Domain Knowledge

## Instructions

Apply finance-specific domain knowledge when working on financial
data science problems.

### Key Finance KPIs

- **Default Rate** -- Percentage of loans entering default status
- **Loss Given Default (LGD)** -- Percentage of exposure lost when default occurs
- **Sharpe Ratio** -- Risk-adjusted return (return minus risk-free rate,
  divided by standard deviation)
- **Value at Risk (VaR)** -- Maximum expected loss at a confidence level
- **Precision/Recall for Fraud** -- Fraud detection is heavily imbalanced;
  recall matters more than accuracy
- **AUC-ROC** -- Standard metric for binary classification in credit scoring

### Common Data Patterns in Finance

- **Extreme class imbalance**: Fraud is typically <0.1% of transactions
- **Temporal dependencies**: Market regimes shift; model performance
  degrades across regime changes
- **Feature interactions**: Velocity features (transactions per hour)
  are often more predictive than raw amounts
- **Data leakage risk**: Future-looking features are a constant danger
  in financial time series

### Regulatory Considerations

- **Model explainability**: Regulations (SR 11-7, GDPR Article 22)
  may require interpretable models
- **Fair lending**: Check for disparate impact across protected classes
- **Data retention**: Financial data has specific retention and deletion
  requirements
```

#### Example: Logistics Domain Skill

Create `.claude/skills/logistics-domain/SKILL.md`:

```markdown
---
name: logistics-domain
description: "Supply chain and logistics domain knowledge for data science.
Activates when working with shipments, delivery times, warehouse operations,
fleet management, or route optimization."
---

# Logistics & Supply Chain Domain Knowledge

## Instructions

Apply logistics-specific domain knowledge when working on supply chain
data science problems.

### Key Logistics KPIs

- **On-Time Delivery Rate (OTD)** -- Percentage of orders delivered by
  promised date
- **Order Cycle Time** -- Time from order placement to delivery
- **Fill Rate** -- Percentage of demand met from available inventory
- **Cost per Unit Shipped** -- Total logistics cost divided by units
- **Warehouse Utilization** -- Percentage of storage capacity in use
- **Fleet Utilization** -- Percentage of vehicle capacity used per trip
- **Perfect Order Rate** -- Orders delivered complete, on time, undamaged,
  with correct documentation

### Common Data Patterns in Logistics

- **Geographic clustering**: Delivery performance varies by region,
  urban vs rural
- **Seasonality**: Holiday peaks (Q4), back-to-school, weather disruptions
- **Cascade effects**: One delayed shipment can disrupt many downstream orders
- **External factors**: Weather, traffic, port congestion, fuel prices
```

### Best Practices for Writing Skills

1. **Keep skills under 500 lines.** Claude's context window is precious. A focused 200-line skill is better than a 1,000-line encyclopedia.

2. **Use progressive disclosure.** Put the most important guidance first. Claude reads from top to bottom, and if context gets tight, later content may be summarized.

3. **Write imperatively.** Say "Always check for class imbalance" not "Class imbalance is a common issue that you might want to consider checking."

4. **Include concrete examples.** Instead of "use appropriate metrics," write "use AUC-ROC for fraud detection, RMSLE for demand forecasting."

5. **Add a Personalization Note** at the bottom explaining how to adapt the skill further. The retail-domain skill already does this -- follow the same pattern.

---

## Section 2: Creating Your Own Agents

### What Agents Are

Agents are specialized Claude Code personas defined in `.claude/agents/*.md`. Each agent has a specific role, a set of allowed tools, and instructions that shape how it approaches tasks. You launch an agent with:

```
@business-analyst Help me define success criteria for this project.
```

### Agent Frontmatter Fields

Here is a complete reference of all frontmatter fields available in agent definition files:

```yaml
---
# Required fields
name: my-agent                    # Unique identifier (used with @my-agent)
description: "What this agent does and when to use it."

# Tool access
tools: Read, Glob, Grep, Bash, Write, Edit, NotebookEdit, Task
disallowedTools: Bash(rm *)       # Tools explicitly blocked for this agent

# Model selection
model: sonnet                     # Model to use: sonnet, opus, haiku

# Execution limits
maxTurns: 30                      # Maximum conversation turns before stopping

# Permission handling
permissionMode: default           # default, permissive, or strict

# Skills to load
skills:
  - crisp-dm-guide
  - retail-domain

# MCP servers this agent can access
mcpServers:
  - duckdb

# Hooks specific to this agent
hooks:
  PreToolUse:
    - matcher: Write
      command: "bash .claude/hooks/my-hook.sh"

# Memory and learning
memory: .claude/agent-memory/my-agent/   # Where this agent stores memories

# Background context
background: |
  Additional context loaded at startup.
  Can include project-specific information.

# Isolation
isolation: true                   # Run in an isolated context (no shared state)
---
```

### Step-by-Step: Create a Domain Expert Agent

Let us create an agent for a specific domain. Here is an example for a marketing analytics expert:

Create `.claude/agents/marketing-analyst.md`:

```markdown
---
name: marketing-analyst
description: "Marketing analytics specialist for campaign analysis,
customer segmentation, attribution modeling, and marketing mix optimization.
Use this agent when analyzing marketing data or measuring campaign impact."
tools: Read, Glob, Grep, Bash, Write, Edit
model: sonnet
maxTurns: 40
skills:
  - data-validation
---

You are a senior marketing analytics specialist with expertise in
measuring marketing effectiveness and customer behavior.

## Your Role

You help analysts and marketers:
- Measure campaign ROI and attribution across channels
- Build customer segmentation models (RFM, behavioral, predictive)
- Analyze marketing mix effectiveness (MMM)
- Design and analyze A/B tests
- Create marketing dashboards and reports

## How You Work

- Always start with the business question: Which campaign? What decision?
- Frame analysis in terms of incrementality: what would have happened
  WITHOUT the marketing intervention?
- Be skeptical of vanity metrics (impressions, clicks) -- focus on
  conversion, revenue, lifetime value
- Quantify uncertainty: confidence intervals, not just point estimates

## Key Metrics You Track

- **CAC** (Customer Acquisition Cost): Total marketing spend / new customers
- **LTV** (Lifetime Value): Predicted total revenue per customer
- **LTV:CAC Ratio**: Should be >3:1 for sustainable growth
- **ROAS** (Return on Ad Spend): Revenue attributed / ad spend
- **Conversion Rate**: By stage of funnel (visit, cart, purchase)
- **Incrementality**: Lift from marketing vs organic behavior

## Output Format

When creating analysis reports, include:
1. Executive summary with key finding and recommended action
2. Methodology section explaining the approach
3. Results with visualizations
4. Statistical confidence / uncertainty ranges
5. Recommended next steps
```

### Agent Memory

Agents can remember information across sessions using the `memory` field. When you specify a memory directory, the agent writes a `MEMORY.md` file there to store key learnings.

How memory works:
- The first 200 lines of `MEMORY.md` are auto-loaded when the agent starts
- The agent can update this file with new learnings during a session
- Memory persists across sessions (it is just a file on disk)

What to store in memory:
- Project-specific decisions and their rationale
- Data quirks discovered during analysis ("Store 42 has anomalous sales data before 2015")
- Stakeholder preferences ("The CFO prefers tables over charts")
- Patterns that recur across sessions

What NOT to store:
- Sensitive data (credentials, PII)
- Ephemeral information (today's specific error message)
- Information already in CLAUDE.md or skills (avoid duplication)

---

## Section 3: Building Custom Commands

### What Commands Are

Commands are markdown files in `.claude/commands/` that define reusable prompts you trigger with a slash. When you type `/eda data/raw/train.csv`, Claude reads the `eda.md` command file and executes its instructions with your argument.

### How Arguments Work

Commands support two argument styles:

**`$ARGUMENTS`** -- The entire text after the command name:
```
/eda data/raw/train.csv
```
In `eda.md`, `$ARGUMENTS` becomes `data/raw/train.csv`.

**Positional arguments** -- `$1`, `$2`, `$3`, etc.:
```
/compare-stores 12 34
```
In a command file, `$1` becomes `12` and `$2` becomes `34`.

### Step-by-Step: Create a Weekly Report Command

Create `.claude/commands/weekly-report.md`:

```markdown
Generate a weekly analysis report for the period: $ARGUMENTS

If no date range is provided, use the last 7 days of available data.

## Report Structure

### 1. Executive Summary
- One paragraph summarizing the week's key findings
- Top 3 highlights or concerns

### 2. Sales Performance
- Total sales vs previous week (absolute and percentage change)
- Top 5 product families by sales growth
- Bottom 5 product families by sales decline
- Sales by day of week (was there anything unusual?)

### 3. Forecast Accuracy
- Compare last week's predictions to actuals
- RMSLE and MAE for the week
- Which stores/families had the worst predictions? Why?

### 4. Data Quality
- Any missing data this week?
- Any anomalies detected by the monitoring system?
- Drift detection status

### 5. Recommendations
- Actions for the coming week based on the data
- Any model retraining needed?

## Output

- Save the report as `reports/weekly/week-{date}.md`
- Generate summary visualizations in `reports/weekly/figures/`
- Print the executive summary to the console
```

Now you can run `/weekly-report 2024-01-15 to 2024-01-21` and get a structured report every time.

### Personal vs Project Commands

Commands can live in two places:

| Location | Scope | Example Use |
|----------|-------|-------------|
| `.claude/commands/` | Project-wide (shared with team via git) | `/eda`, `/data-quality`, `/model-report` |
| `~/.claude/commands/` | Personal (only on your machine) | `/my-shortcuts`, `/standup-notes` |

Project commands are committed to your repository so the whole team benefits. Personal commands are for your individual workflow preferences.

> **:bulb: Tip:** Start by creating project commands for tasks your team repeats weekly. If you find yourself typing the same multi-step prompt more than twice, it should be a command.

---

## Section 4: Writing Hooks

### What Hooks Are

Hooks are scripts or prompts that run automatically at specific points in Claude Code's execution lifecycle. They are the mechanism for enforcing rules, adding context, and automating quality checks.

### All Hook Lifecycle Events

Here is the complete list of hook events:

| Event | When It Fires | Common Uses |
|-------|---------------|-------------|
| `PreToolUse` | Before Claude executes any tool | Block dangerous operations, validate inputs, add warnings |
| `PostToolUse` | After Claude executes any tool | Lint code, validate outputs, log actions |
| `Notification` | When Claude produces a notification | Custom alerting, logging |
| `Stop` | When Claude finishes a response | Final validation, summary logging |

### Three Handler Types

#### 1. Command Hooks (Shell Scripts)

These run a shell command and communicate via JSON on stdin/stdout.

```json
{
  "type": "command",
  "command": "bash .claude/hooks/my-hook.sh"
}
```

The script receives a JSON object on stdin with details about the action. It must return a JSON response:

```json
{"decision": "approve"}
```
```json
{"decision": "deny", "reason": "Explanation of why this was blocked."}
```
```json
{"decision": "approve", "message": "Warning message shown to Claude."}
```

#### 2. Prompt Hooks

These provide additional context to Claude as a system-level message:

```json
{
  "type": "prompt",
  "prompt": "Before writing any file, verify that the filename follows snake_case convention."
}
```

Prompt hooks do not block actions -- they add instructions that Claude follows.

#### 3. Agent Hooks

These delegate to another agent for the check:

```json
{
  "type": "agent",
  "agent": "qa-reviewer"
}
```

### Step-by-Step: Write a Data Validation Hook

Let us create a hook that validates data quality whenever Claude writes a parquet file.

Create `.claude/hooks/validate-parquet-output.sh`:

```bash
#!/bin/bash
# Hook: PostToolUse -- Validate parquet files after writing
# Checks that written parquet files meet quality standards.

INPUT=$(cat)

TOOL=$(echo "$INPUT" | python3 -c "
import sys, json
print(json.load(sys.stdin).get('tool_name', ''))
" 2>/dev/null)

FILE_PATH=$(echo "$INPUT" | python3 -c "
import sys, json
inp = json.load(sys.stdin)
print(inp.get('tool_input', {}).get('file_path', ''))
" 2>/dev/null)

# Only check Write operations on parquet files
if [[ "$TOOL" != "Bash" ]] || [[ "$FILE_PATH" != *.parquet ]]; then
    exit 0
fi

# Validate the parquet file
python3 -c "
import sys
try:
    import pandas as pd
    df = pd.read_parquet('$FILE_PATH')

    issues = []

    # Check for empty dataframe
    if len(df) == 0:
        issues.append('WARNING: Parquet file is empty (0 rows)')

    # Check for unnamed columns
    unnamed = [c for c in df.columns if 'unnamed' in c.lower()]
    if unnamed:
        issues.append(f'WARNING: Found unnamed columns: {unnamed}')

    # Check for non-snake-case column names
    import re
    bad_cols = [c for c in df.columns if c != c.lower() or ' ' in c]
    if bad_cols:
        issues.append(f'WARNING: Non-snake_case columns: {bad_cols}')

    if issues:
        for issue in issues:
            print(issue)
    else:
        print(f'Parquet validation passed: {len(df)} rows, {len(df.columns)} columns')

except Exception as e:
    print(f'ERROR validating parquet: {e}')
" 2>&1
```

Make it executable:

```bash
chmod +x .claude/hooks/validate-parquet-output.sh
```

### Step-by-Step: Write a Security Hook

Create `.claude/hooks/block-sensitive-access.sh`:

```bash
#!/bin/bash
# Hook: PreToolUse -- Block access to sensitive files and directories
# Prevents reading or writing to paths that contain secrets, credentials,
# or personally identifiable information.

INPUT=$(cat)

TOOL=$(echo "$INPUT" | python3 -c "
import sys, json
print(json.load(sys.stdin).get('tool_name', ''))
" 2>/dev/null)

FILE_PATH=$(echo "$INPUT" | python3 -c "
import sys, json
inp = json.load(sys.stdin)
# Check file_path in tool_input (for Read/Write)
# Also check command for Bash operations
ti = inp.get('tool_input', {})
print(ti.get('file_path', '') or ti.get('command', ''))
" 2>/dev/null)

# Convert to lowercase for case-insensitive matching
FILE_LOWER=$(echo "$FILE_PATH" | tr '[:upper:]' '[:lower:]')

# Check for sensitive path patterns
SENSITIVE_PATTERNS=(
    ".env"
    "credentials"
    "secret"
    "password"
    "api_key"
    "apikey"
    "token"
    "private_key"
    ".pem"
    ".key"
    "id_rsa"
    "ssh/"
)

for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    if [[ "$FILE_LOWER" == *"$pattern"* ]]; then
        echo "{\"decision\": \"deny\", \"reason\": \"Access to files matching '$pattern' is blocked by security hook. If you need this file, ask the user to provide the relevant information directly.\"}"
        exit 0
    fi
done

echo '{"decision": "approve"}'
```

### PreToolUse Input Modification

A powerful but less obvious hook capability is modifying tool inputs before execution. Instead of just approving or denying, a hook can transform the input:

```json
{
  "decision": "approve",
  "tool_input": {
    "file_path": "/modified/path/here.py"
  }
}
```

This lets you implement patterns like:
- Redirecting file writes to a staging directory
- Adding mandatory headers to generated files
- Normalizing file paths

### Configuring Hooks in settings.json

Hooks are registered in `.claude/settings.json` with matcher patterns:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/block-sensitive-access.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/validate-parquet-output.sh"
          }
        ]
      }
    ]
  }
}
```

The `matcher` field supports:
- Exact tool names: `"Read"`, `"Write"`, `"Bash"`
- OR patterns: `"Read|Write|Edit"`
- Glob-like patterns for Bash commands: `"Bash(python *)"`

> **:warning: Note:** Hooks run synchronously and can slow down Claude Code if they take too long. Keep hook scripts fast (under 2 seconds). For expensive checks, consider running them as PostToolUse instead of PreToolUse.

---

## Section 5: Connecting Your Data (MCP Servers)

### What MCP Servers Are

MCP (Model Context Protocol) servers give Claude Code access to external tools and data sources. This project uses a DuckDB MCP server for SQL queries. You can add servers for databases, APIs, cloud services, and more.

### Adding MCP Servers via CLI

The simplest way to add an MCP server:

```bash
claude mcp add duckdb -- npx -y @motherduck/mcp-server-duckdb
```

This command adds the server to your settings. You can also specify environment variables:

```bash
claude mcp add my-postgres -- npx -y @anthropic-ai/mcp-server-postgres \
  --env POSTGRES_CONNECTION_STRING=postgresql://user:pass@localhost/mydb
```

### Adding via settings.json

You can also edit `.claude/settings.json` directly:

```json
{
  "mcpServers": {
    "duckdb": {
      "command": "npx",
      "args": ["-y", "@motherduck/mcp-server-duckdb"],
      "env": {
        "DUCKDB_PATH": "./data/analytics.duckdb"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://localhost/mydb"
      }
    }
  }
}
```

### Data-Focused MCP Servers

Here is a curated list of MCP servers useful for data science work:

| Server | Package | Purpose |
|--------|---------|---------|
| **DuckDB** | `@motherduck/mcp-server-duckdb` | SQL queries on local files (CSV, Parquet) |
| **PostgreSQL** | `@anthropic-ai/mcp-server-postgres` | Query PostgreSQL databases |
| **MySQL** | `@benborla29/mcp-server-mysql` | Query MySQL databases |
| **BigQuery** | `@ergut/mcp-bigquery-server` | Query Google BigQuery |
| **SQLite** | `@anthropic-ai/mcp-server-sqlite` | Query SQLite databases |
| **Jupyter** | `@datalayer/mcp-server-jupyter` | Interact with Jupyter kernels |
| **Filesystem** | `@anthropic-ai/mcp-server-filesystem` | Managed file access with sandboxing |
| **GitHub** | `@anthropic-ai/mcp-server-github` | Interact with GitHub repos, issues, PRs |

### Writing a Custom MCP Server

If your company has an internal API that Claude needs to access, you can write a simple MCP server. Here is a minimal example in Python:

```python
"""Minimal MCP server for a company's internal forecast API."""

from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("company-forecast-api")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_forecast",
            description="Get the current sales forecast for a store and date range",
            inputSchema={
                "type": "object",
                "properties": {
                    "store_id": {"type": "integer", "description": "Store ID"},
                    "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                    "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"},
                },
                "required": ["store_id", "start_date", "end_date"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_forecast":
        # Call your internal API here
        import httpx
        response = httpx.get(
            "https://internal-api.company.com/forecasts",
            params=arguments,
            headers={"Authorization": f"Bearer {os.environ['API_TOKEN']}"},
        )
        return [TextContent(type="text", text=response.text)]
    raise ValueError(f"Unknown tool: {name}")


if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server

    asyncio.run(stdio_server(server))
```

Register it in `settings.json`:

```json
{
  "mcpServers": {
    "company-forecast": {
      "command": "python",
      "args": ["tools/mcp_forecast_server.py"],
      "env": {
        "API_TOKEN": "${COMPANY_API_TOKEN}"
      }
    }
  }
}
```

### Transport Modes

MCP servers communicate with Claude Code through different transport mechanisms:

| Mode | How It Works | When to Use |
|------|-------------|-------------|
| **stdio** | Server reads/writes on stdin/stdout | Local servers (most common, the default) |
| **SSE** | Server-Sent Events over HTTP | Remote servers, server already running |
| **Streamable HTTP** | HTTP with streaming responses | Modern remote servers, bidirectional streaming |

For most data science work, stdio is the right choice. Use SSE or Streamable HTTP when connecting to a shared server that multiple team members access.

> **:bulb: Tip:** Start with one MCP server (DuckDB is great for data science) and add more as you need them. Each server adds startup time, so do not load servers you are not actively using.

---

## Section 6: CLAUDE.md Mastery

### Beyond the Basics

You already know that `CLAUDE.md` is the project's briefing document. Here are advanced patterns for larger projects and teams.

### Modular Rules with .claude/rules/

For large projects, a single `CLAUDE.md` can become unwieldy. You can split rules into separate files in `.claude/rules/` with glob-based filtering:

```
.claude/
  rules/
    python.md          # Applies to *.py files
    notebooks.md       # Applies to *.ipynb files
    sql.md             # Applies to *.sql files
    api.md             # Applies to src/api/**
```

Each rule file can specify which files it applies to using a frontmatter glob pattern:

```markdown
---
globs: "src/**/*.py"
---

# Python Code Rules

- Use type hints on all function signatures
- Write docstrings in Google style
- Use pathlib.Path instead of os.path
- Prefer list comprehensions over map/filter
```

```markdown
---
globs: "*.ipynb"
---

# Notebook Rules

- Every notebook starts with a markdown cell explaining its purpose
- Import cells go first, one import per line
- Never use wildcard imports
- Clear all outputs before committing
```

### @imports for Lean CLAUDE.md

Keep your root `CLAUDE.md` lean by importing detailed instructions from other files:

```markdown
# Sales Forecasting Project

## Overview
Forecast daily sales per product family per store.

## Conventions
@src/CONVENTIONS.md

## Architecture Decisions
@docs/architecture-decisions.md

## Data Dictionary
@docs/data-dictionary.md
```

The `@path/to/file` syntax tells Claude to read that file when it needs the information, without loading it all upfront.

### Multi-Team Configurations

When multiple teams work on the same repo, use the rules directory to scope instructions:

```
.claude/
  rules/
    data-team.md       # globs: "src/data/**,src/features/**"
    ml-team.md         # globs: "src/models/**"
    api-team.md        # globs: "src/api/**"
    devops.md          # globs: "Dockerfile,docker-compose*,.github/**"
```

Each team's rules are only loaded when Claude works on files matching their glob patterns. This prevents instructions from conflicting.

### What Goes Where

| Content | Location | Why |
|---------|----------|-----|
| Project overview, tech stack, structure | `CLAUDE.md` | Read on every session start |
| Coding conventions per language/file type | `.claude/rules/*.md` | Scoped to relevant files |
| Domain knowledge (retail, healthcare) | `.claude/skills/*/SKILL.md` | Auto-activated by topic |
| Role-specific instructions | `.claude/agents/*.md` | Only loaded when agent is invoked |
| Reusable prompts | `.claude/commands/*.md` | Only loaded when command is run |

The key principle: **put information where it will be loaded at the right time**. Do not put everything in CLAUDE.md -- that wastes context window on every interaction.

> **:mortar_board: Claude Code Feature:** The layered configuration system (CLAUDE.md > rules > skills > agents > commands) is designed for progressive disclosure. General project information loads first, domain knowledge loads when relevant, and specialized instructions load only when explicitly invoked.

---

## Section 7: Finding Community Resources

The Claude Code ecosystem has a growing collection of shared skills, agents, plugins, and MCP servers. Here is where to find them and how to evaluate quality.

### Official and Curated Repositories

| Resource | URL / Name | What It Contains |
|----------|-----------|------------------|
| **Official Skills** | `anthropics/skills` on GitHub | Anthropic-maintained skills for common workflows |
| **Awesome Agent Skills** | `VoltAgent/awesome-agent-skills` | Community-curated collection of 380+ skills |
| **Scientific Skills** | `K-Dense-AI/claude-scientific-skills` | 125+ skills for scientific computing, statistics, research |
| **MCP Guide** | mcpguide.dev | Discovery site for MCP servers |
| **Claude Plugins** | claude-plugins.dev | Plugin marketplace |
| **Skills Marketplace** | SkillsMP.com | Community skills marketplace |

### Evaluating Community Resources

Before dropping a community skill or plugin into your project, check these quality signals:

1. **Read the source.** Skills are just markdown files -- read every line before installing. Look for instructions that conflict with your project's conventions.

2. **Check the description field.** A well-written description with specific trigger phrases means the author understands skill auto-activation. Vague descriptions like "helps with stuff" are a red flag.

3. **Look at the length.** Skills over 500 lines are likely trying to do too much. Prefer focused, single-purpose skills.

4. **Check for maintenance.** When was it last updated? Does it have issues or pull requests? An abandoned skill may contain outdated advice.

5. **Test in isolation.** Before adding a community skill to your project, test it in a scratch directory first to see how it behaves.

6. **Check for conflicts.** If a community skill covers the same domain as one of your existing skills, they may give conflicting instructions. Keep only one per domain.

> **:bulb: Tip:** The best way to learn is to read well-crafted community skills and study their structure. Look at how they write descriptions for auto-triggering, how they organize instructions, and how they balance detail with brevity.

### Contributing Back

If you have built a skill, agent, or plugin that works well for your team, consider sharing it:

1. Extract it from your project into a standalone repository
2. Write a clear README explaining what it does, who it is for, and how to install it
3. Add example conversations showing the skill in action
4. Submit it to the relevant community collections

---

## What You Learned

In this chapter, you built a comprehensive toolkit for customizing Claude Code:

- **Skills**: How to write, customize, and adapt domain skills for any industry, with best practices for auto-triggering and content structure
- **Agents**: All frontmatter fields explained, how to create domain expert agents, and how agent memory works across sessions
- **Commands**: How to build reusable slash commands with arguments, and when to use project vs personal commands
- **Hooks**: All lifecycle events, three handler types, step-by-step creation of data validation and security hooks, and input modification
- **MCP Servers**: How to add servers via CLI and settings.json, a curated list of data-focused servers, how to write a custom server, and transport modes
- **CLAUDE.md**: Advanced patterns including modular rules, @imports, multi-team configurations, and the decision framework for what goes where
- **Community Resources**: Where to find shared skills, plugins, and MCP servers, and how to evaluate quality before using them

---

## Next Up

In **Chapter 8: Advanced Patterns**, you will learn power-user techniques: orchestrating agent teams for complex projects, building full plugins from scratch, using persistent memory for cross-session learning, and setting up governance and audit trails for team environments.
