# Chapter 8: Advanced Patterns

This final chapter covers power-user techniques that make Claude Code truly shine on complex, real-world data science projects. You will learn how to orchestrate teams of agents, build distributable plugins, use persistent memory for cross-session learning, integrate multiple tools into a cohesive workflow, and set up governance for team environments.

These patterns are optional -- you can be highly productive with Claude Code using just the basics from earlier chapters. But when your projects grow in complexity, the techniques here will scale with you.

---

## Section 1: Agent Teams for Complex Projects

### The Problem with Solo Agents

A single Claude Code session is powerful, but some tasks benefit from multiple perspectives working in parallel. Consider building a new feature end-to-end: you need research on the best approach, implementation code, and a critical review before merging. Doing all three in one conversation can lead to context overload and conflicting priorities (the same "mind" that writes the code is poorly positioned to critically review it).

### Architecture: Team Lead + Teammates

Claude Code supports a team model where one agent (the Team Lead) coordinates others (Teammates). The Team Lead:
- Breaks down the overall task into subtasks
- Assigns work to specialized teammates
- Collects results and synthesizes them
- Makes the final decision

Teammates:
- Work on their assigned subtask in isolation
- Report back to the Team Lead with their findings
- Do not communicate with each other directly (all coordination goes through the lead)

### Communication: TeammateTool

The Team Lead communicates with teammates through the `TeammateTool`, which supports these operations:

| Operation | Purpose |
|-----------|---------|
| `create_task` | Assign a new task to a teammate |
| `get_task_status` | Check if a teammate has finished |
| `get_task_result` | Retrieve the teammate's output |
| `send_message` | Send additional context or clarification |
| `list_teammates` | See available teammates |
| `list_tasks` | See all assigned tasks and their status |
| `cancel_task` | Cancel a running task |
| `set_priority` | Change task execution priority |
| `get_teammate_info` | Get details about a teammate's capabilities |
| `create_shared_context` | Share information accessible to all teammates |
| `get_shared_context` | Read shared information |
| `update_shared_context` | Modify shared information |
| `get_task_history` | View completed tasks and their results |

### Real Example: End-to-End Feature Development

Here is how you would orchestrate our four agents to build a new "promotion impact analysis" feature:

**Step 1: Start the orchestration**

```
I need a complete promotion impact analysis for the retail forecasting project.
This should include:
1. A clear definition of what "promotion impact" means for our business
2. Feature engineering to capture promotion effects
3. A model that isolates the incremental lift from promotions
4. A critical review of the methodology before we finalize

Orchestrate this using the business-analyst, data-engineer, ml-engineer,
and qa-reviewer agents as a team.
```

**Step 2: Claude (as Team Lead) delegates**

The Team Lead breaks this into subtasks:

- **@business-analyst**: "Define promotion impact for our grocery retail context. What KPIs should we measure? What counts as a successful promotion? Write a brief requirements document."

- **@data-engineer**: "Engineer promotion-related features from our data. Include: is_on_promotion, promo_duration, days_since_last_promo, promo_type encoding, and post-promotion dip indicators. Save to data/processed/promo_features.parquet."

- **@ml-engineer**: "Build a model that estimates the incremental sales lift from promotions. Compare a model with promotion features vs without. Quantify the average uplift per product family."

- **@qa-reviewer**: "Review the entire promotion analysis pipeline. Check for data leakage (are we using promotion information that would not be available at prediction time?), verify the causal claims, and assess whether the business conclusions are supported."

**Step 3: Each teammate works independently**

The business-analyst produces a requirements document. The data-engineer builds features. The ml-engineer trains and compares models. The qa-reviewer scrutinizes everything.

**Step 4: Team Lead synthesizes**

The Team Lead collects all results, resolves any conflicts (for example, if the qa-reviewer flags a leakage issue that invalidates the ml-engineer's results), and produces a final deliverable.

### When to Use Teams vs Single Agent vs Subagents

| Scenario | Recommended Approach | Why |
|----------|---------------------|-----|
| Quick analysis question | Single session | No coordination overhead needed |
| Write a function with tests | Single session | One context is enough |
| Full feature (code + tests + docs) | Single agent, sequential | The same context helps maintain consistency |
| Multi-perspective review | Team (2-3 agents) | Different agents catch different issues |
| Large cross-cutting project | Full team (4+ agents) | Parallel work saves wall-clock time |
| Routine automated check | Subagent within a hook | Lightweight, triggered automatically |

### Trade-Offs

**Token cost**: Each teammate runs in its own context, so a 4-agent team uses roughly 4x the tokens of a single session. Only use teams when the quality benefit justifies the cost.

**Coordination overhead**: The Team Lead spends tokens on task management messages. For small tasks, this overhead can exceed the task itself.

**Parallel execution benefits**: Teammates can work simultaneously. If you have four independent subtasks that each take 2 minutes, a team finishes in 2 minutes instead of 8.

**Context isolation**: Each teammate has a fresh context. This is a feature (no cross-contamination) and a limitation (teammates cannot see each other's work unless the Team Lead shares it).

> **:mortar_board: Claude Code Feature:** Agent teams are most valuable when you need diverse perspectives or parallel execution. The QA reviewer agent is especially powerful as a teammate -- it catches issues that the author of the code would naturally overlook, because it starts from a position of skepticism rather than ownership.

---

## Section 2: Building a Reusable Plugin

### Full Walkthrough

In Chapter 6, you saw the plugin structure in outline. Here we will build one from scratch and test it.

### Step 1: Create the Directory Structure

```bash
mkdir -p .claude-plugin/{skills/crisp-dm-guide,skills/retail-domain,skills/data-validation,agents,commands,hooks,settings}
```

### Step 2: Write the plugin.json Manifest

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "ds-crisp-dm-toolkit",
  "version": "1.0.0",
  "description": "Complete data science project toolkit following CRISP-DM methodology. Provides specialized agents for business analysis, data engineering, ML engineering, and QA review. Includes domain skills, analysis commands, safety hooks, and DuckDB integration.",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": "https://github.com/your-org/ds-crisp-dm-toolkit",
  "keywords": [
    "data-science",
    "crisp-dm",
    "machine-learning",
    "forecasting",
    "retail"
  ],
  "skills": [
    "skills/crisp-dm-guide",
    "skills/retail-domain",
    "skills/data-validation"
  ],
  "agents": [
    "agents/business-analyst.md",
    "agents/data-engineer.md",
    "agents/ml-engineer.md",
    "agents/qa-reviewer.md"
  ],
  "commands": [
    "commands/eda.md",
    "commands/data-quality.md",
    "commands/model-report.md",
    "commands/feature-importance.md"
  ],
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "handler": "hooks/validate-data-load.sh"
      },
      {
        "matcher": "Write|Edit",
        "handler": "hooks/protect-production.sh"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|NotebookEdit",
        "handler": "hooks/lint-notebook.sh"
      }
    ]
  },
  "mcpServers": {
    "duckdb": {
      "command": "npx",
      "args": ["-y", "@motherduck/mcp-server-duckdb"],
      "env": {
        "DUCKDB_PATH": "./data/analytics.duckdb"
      }
    }
  },
  "settings": {
    "permissions": {
      "allow": [
        "Read",
        "Glob",
        "Grep",
        "Bash(python *)",
        "Bash(pip install *)",
        "Bash(pytest *)",
        "Bash(jupyter *)",
        "Bash(git *)",
        "Bash(ls *)",
        "Bash(mkdir *)",
        "Bash(duckdb *)",
        "Write",
        "Edit",
        "NotebookEdit",
        "Task"
      ],
      "deny": [
        "Read(.env)",
        "Read(*credentials*)",
        "Read(*secret*)",
        "Bash(rm -rf *)",
        "Bash(DROP TABLE*)",
        "Bash(DELETE FROM*)"
      ]
    }
  },
  "minClaudeCodeVersion": "1.0.0"
}
```

### Step 3: Copy Files into the Plugin

Ask Claude to help:

```
Copy all the skills, agents, commands, and hooks from .claude/ into
.claude-plugin/ following the plugin directory structure. Preserve
the exact content of each file.
```

### Step 4: Create Default Settings

Create `.claude-plugin/settings/default-settings.json`:

```json
{
  "_comment": "These settings are applied when the plugin is installed. They merge with existing project settings.",
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(python *)",
      "Bash(pytest *)",
      "Write",
      "Edit",
      "NotebookEdit"
    ],
    "deny": [
      "Read(.env)",
      "Read(*credentials*)",
      "Bash(rm -rf *)",
      "Bash(DROP TABLE*)"
    ]
  }
}
```

### Step 5: Test the Plugin Locally

Run Claude Code with the plugin directory:

```bash
claude --plugin-dir .claude-plugin/
```

Verify that:
- Skills appear and auto-activate when you discuss relevant topics
- Agents are available via `@business-analyst`, `@data-engineer`, etc.
- Commands work: `/eda`, `/data-quality`, `/model-report`, `/feature-importance`
- Hooks fire when reading data files or writing notebooks

### All plugin.json Fields Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique plugin identifier (lowercase, hyphens) |
| `version` | string | Yes | Semantic version (major.minor.patch) |
| `description` | string | Yes | What the plugin does (shown during discovery) |
| `author` | string | No | Author name and optional email |
| `license` | string | No | License identifier (MIT, Apache-2.0, etc.) |
| `repository` | string | No | URL to the source repository |
| `keywords` | array | No | Tags for search and discovery |
| `skills` | array | No | Paths to skill directories within the plugin |
| `agents` | array | No | Paths to agent definition files |
| `commands` | array | No | Paths to command files |
| `hooks` | object | No | Hook configurations with handler paths |
| `mcpServers` | object | No | MCP server definitions to install |
| `settings` | object | No | Default permission and configuration settings |
| `minClaudeCodeVersion` | string | No | Minimum required Claude Code version |

### Publishing Considerations

When you are ready to share your plugin:

1. **Remove project-specific details.** Replace hardcoded paths, store numbers, and product families with placeholder instructions that users can customize.

2. **Write a thorough README.** Include: what the plugin does, who it is for, installation instructions, configuration options, and example conversations.

3. **Version carefully.** Follow semantic versioning -- breaking changes to skills or agent instructions should bump the major version.

4. **Test with a fresh project.** Install the plugin in an empty project directory to verify nothing depends on your specific project files.

> **:mortar_board: Claude Code Feature:** Plugins are the highest-level abstraction in Claude Code's configuration hierarchy. A single plugin can establish an entire team's workflow -- coding conventions, domain expertise, analysis patterns, safety guardrails, and tool access -- with one installation step.

---

## Section 3: Persistent Agent Memory

### How Memory Works

Agents can maintain persistent memory across sessions using the `memory` field in their frontmatter. This is not conversation history (which resets each session) -- it is an explicit knowledge store that the agent reads and writes.

### Configuration

In the agent's frontmatter:

```yaml
---
name: ml-engineer
memory: .claude/agent-memory/ml-engineer/
---
```

### Memory Directories

Memory files can live in two locations:

| Location | Scope | Persists Across |
|----------|-------|-----------------|
| `.claude/agent-memory/` | Project-specific | Sessions in this project |
| `~/.claude/agent-memory/` | Global (user-wide) | All projects |

### MEMORY.md Auto-Loading

When an agent starts, Claude Code automatically reads the first 200 lines of the `MEMORY.md` file in the agent's memory directory. This provides instant context without the agent needing to search for past information.

A typical `MEMORY.md` structure:

```markdown
# ML Engineer Memory

## Project-Specific Learnings

### Data Quirks
- Store 42 has anomalous sales data before 2015-03-01 (POS system migration)
- The CELEBRATION category has extreme variance around holidays --
  use robust scaling
- Oil price data has weekend gaps -- forward-fill, do not interpolate

### Model Decisions
- XGBoost with 500 trees, max_depth=6, learning_rate=0.05 is our best config
- Adding store_cluster as a feature improved RMSLE by 0.012
- Lag features beyond 28 days added noise without improving performance

### Failed Experiments
- LSTM model: trained for 3 hours, performed worse than XGBoost on all metrics
- Prophet per store-family: too slow (54 stores x 33 families = 1,782 models)
- Stacking ensemble: marginal improvement (+0.003 RMSLE) not worth complexity

### Stakeholder Preferences
- The VP of Operations prefers weekly granularity reports over daily
- The supply chain team wants predictions 14 days out, not 7
```

### What to Store vs What Not to Store

**Good candidates for memory:**
- Data characteristics that are discovered through analysis (not documented elsewhere)
- Model decisions and their rationale
- Failed experiments and why they failed (prevents repeating them)
- Stakeholder preferences and communication styles
- Project-specific conventions not in CLAUDE.md

**Do NOT store in memory:**
- Credentials, API keys, or sensitive information
- Exact data values or raw data excerpts
- Information that changes rapidly (today's metrics)
- Information already in CLAUDE.md, skills, or agent instructions (avoid duplication)
- Personal information about team members

### Cross-Session Learning Patterns

Here are practical patterns for using memory effectively:

**Pattern 1: Experiment Log**

The ml-engineer agent records every experiment:

```markdown
## Experiment Log

### 2024-01-15: Baseline models
- Linear regression: RMSLE 0.892
- XGBoost default: RMSLE 0.634
- Decision: proceed with XGBoost tuning

### 2024-01-16: Feature engineering round 1
- Added lag features (7d, 14d, 28d): RMSLE improved to 0.598
- Added rolling stats (7d mean/std): RMSLE improved to 0.571

### 2024-01-17: Hyperparameter tuning
- Optuna 100 trials: best RMSLE 0.543
- Key params: n_estimators=487, max_depth=6, learning_rate=0.048
```

Next session, the agent immediately knows the best model and what has been tried.

**Pattern 2: Data Quality Journal**

The data-engineer agent records data issues as they are found:

```markdown
## Known Data Issues

### Discovered 2024-01-14
- 127 rows in train.csv where sales < 0 (returns coded as negative)
  Resolution: replaced with 0 for forecasting purposes
- store_nbr 52 missing all data for 2016-12 (store renovation)
  Resolution: excluded from that month's training data

### Discovered 2024-01-16
- onpromotion column has 8,431 nulls (1.2% of total)
  Resolution: filled with 0 (assumed not on promotion if null)
```

**Pattern 3: Stakeholder Glossary**

The business-analyst agent maintains a translation table:

```markdown
## Stakeholder Terminology

| They Say | We Mean | Technical Term |
|----------|---------|---------------|
| "accuracy" | forecast closeness | RMSLE or MAE |
| "the model is wrong" | large residual for a specific case | outlier analysis |
| "seasonal pattern" | recurring trend by calendar period | seasonality component |
| "demand sensing" | short-horizon forecasting | 1-7 day ahead prediction |
```

> **:warning: Note:** Memory files are plain text files committed to your project (or stored locally). Treat them the same as any other project file when it comes to sensitive information. Never store secrets, credentials, or PII in memory files.

---

## Section 4: Integration Patterns

### Claude Code + Jupyter + DuckDB + MLflow

Here is how to set up a fully integrated data science environment where all tools work together:

**launch.json configuration:**

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "jupyter",
      "runtimeExecutable": "jupyter",
      "runtimeArgs": ["lab", "--no-browser", "--port=8888"],
      "port": 8888
    },
    {
      "name": "forecast-api",
      "runtimeExecutable": "uvicorn",
      "runtimeArgs": ["src.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
      "port": 8000
    },
    {
      "name": "mlflow",
      "runtimeExecutable": "mlflow",
      "runtimeArgs": ["ui", "--port", "5000"],
      "port": 5000
    }
  ]
}
```

**MCP servers in settings.json:**

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
    "jupyter": {
      "command": "npx",
      "args": ["-y", "@datalayer/mcp-server-jupyter"],
      "env": {
        "JUPYTER_URL": "http://localhost:8888"
      }
    }
  }
}
```

**The workflow:**

1. Start all servers:
   ```
   Start the jupyter, forecast-api, and mlflow servers.
   ```

2. Use DuckDB for quick SQL exploration:
   ```
   Using DuckDB, show me total sales by product family for 2017,
   ordered by total sales descending.
   ```

3. Build features in a Jupyter notebook:
   ```
   Create a notebook that builds all lag and rolling features,
   then saves to parquet.
   ```

4. Train and log to MLflow:
   ```
   Train an XGBoost model and log the experiment to MLflow,
   including parameters, metrics, and the model artifact.
   ```

5. Deploy through the API:
   ```
   Update the forecast API to load the latest model from MLflow
   instead of a static file path.
   ```

### Multiple MCP Servers Working Together

When you have multiple MCP servers, they complement each other:

- **DuckDB** handles SQL queries on local files (fast, no setup)
- **PostgreSQL** connects to your production database (real data)
- **Jupyter** lets Claude execute code in notebook kernels (persistent state)
- **GitHub** enables code review and PR workflows

Claude automatically chooses the right server based on your request. If you ask a SQL question, it uses DuckDB. If you ask about a pull request, it uses GitHub.

### Environment Variables and Secrets Management

Never hardcode secrets in `settings.json`. Use environment variable references:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}"
      }
    }
  }
}
```

The `${DATABASE_URL}` syntax tells Claude Code to read the value from your shell environment. Set it in your `.bashrc`, `.zshrc`, or a `.env` file that is NOT committed to git:

```bash
# In your shell profile
export DATABASE_URL="postgresql://user:password@host:5432/dbname"
```

For team environments, document which environment variables need to be set (without revealing the actual values):

```markdown
# In CLAUDE.md or a setup guide

## Required Environment Variables

- `DATABASE_URL` -- PostgreSQL connection string for the analytics database
- `COMPANY_API_TOKEN` -- Bearer token for the internal forecast API
- `MLFLOW_TRACKING_URI` -- URL of the MLflow tracking server
```

> **:bulb: Tip:** Create a `.env.example` file with placeholder values that shows the required format without exposing real credentials. Add `.env` to your `.gitignore`.

---

## Section 5: Governance and Audit Trails

### Why Governance Matters

When multiple people use Claude Code on the same project -- or when Claude has access to sensitive data -- you need controls. Who accessed what? What changes were made? Can we reconstruct what happened?

### Using Hooks for Compliance Logging

Create a hook that logs every data access and model change:

**`.claude/hooks/audit-log.sh`**

```bash
#!/bin/bash
# Hook: PostToolUse -- Log all tool usage for audit trail
# Writes to data/audit/tool_usage.jsonl

INPUT=$(cat)

TOOL=$(echo "$INPUT" | python3 -c "
import sys, json
print(json.load(sys.stdin).get('tool_name', ''))
" 2>/dev/null)

FILE_PATH=$(echo "$INPUT" | python3 -c "
import sys, json
inp = json.load(sys.stdin)
print(inp.get('tool_input', {}).get('file_path', '') or
      inp.get('tool_input', {}).get('command', ''))
" 2>/dev/null)

# Only log data and model operations
case "$FILE_PATH" in
    *data/*|*models/*|*src/*|*.parquet|*.csv|*.joblib)
        mkdir -p data/audit
        python3 -c "
import json, datetime, os

entry = {
    'timestamp': datetime.datetime.now().isoformat(),
    'tool': '$TOOL',
    'target': '$FILE_PATH',
    'user': os.environ.get('USER', 'unknown'),
    'session': os.environ.get('CLAUDE_SESSION_ID', 'unknown'),
}

with open('data/audit/tool_usage.jsonl', 'a') as f:
    f.write(json.dumps(entry) + '\n')
" 2>/dev/null
        ;;
esac
```

Register it as a PostToolUse hook for all tools:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Read|Write|Edit|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/audit-log.sh"
          }
        ]
      }
    ]
  }
}
```

### Permission Settings for Team Environments

Claude Code supports a hierarchy of settings files:

| File | Scope | Committed to Git? |
|------|-------|-------------------|
| `.claude/settings.json` | Project-wide (shared) | Yes |
| `.claude/settings.local.json` | Project-wide (personal) | No (gitignored) |
| `~/.claude/settings.json` | User-wide (all projects) | N/A |

**Settings merge order** (later overrides earlier):
1. User-wide settings (`~/.claude/settings.json`)
2. Project shared settings (`.claude/settings.json`)
3. Project local settings (`.claude/settings.local.json`)

This hierarchy lets you:
- Set organization-wide policies in the user config (every project gets them)
- Set project-specific rules in the shared config (the whole team gets them)
- Override for personal workflow in the local config (only you get them)

### Deny Rules for Sensitive Operations

For a team environment where you want strong guardrails:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(python *)",
      "Bash(pytest *)"
    ],
    "deny": [
      "Read(.env*)",
      "Read(*credentials*)",
      "Read(*secret*)",
      "Read(*password*)",
      "Write(.claude/settings.json)",
      "Edit(.claude/settings.json)",
      "Bash(rm -rf *)",
      "Bash(DROP *)",
      "Bash(DELETE *)",
      "Bash(TRUNCATE *)",
      "Bash(git push --force*)",
      "Bash(git reset --hard*)",
      "Bash(chmod *)",
      "Bash(chown *)",
      "Bash(curl * | bash)",
      "Bash(wget * | bash)"
    ]
  }
}
```

Key deny rules explained:

| Rule | Why |
|------|-----|
| `Write(.claude/settings.json)` | Prevent Claude from modifying its own permissions |
| `Bash(git push --force*)` | Prevent destructive git operations |
| `Bash(git reset --hard*)` | Prevent losing uncommitted work |
| `Bash(chmod *)` and `Bash(chown *)` | Prevent file permission changes |
| `Bash(curl * \| bash)` | Prevent execution of downloaded scripts |

> **:warning: Note:** Deny rules take precedence over allow rules. If something is in both lists, it is denied. This is a safety-first design -- you cannot accidentally override a deny with an allow.

### Project vs User Settings: A Practical Guide

Here is a decision framework for where to put settings:

**Put in `.claude/settings.json` (shared, committed):**
- Permission rules the whole team should follow
- MCP server configurations (databases, APIs)
- Hook configurations (linting, validation)
- Anything the team has agreed on

**Put in `.claude/settings.local.json` (personal, gitignored):**
- Your personal MCP server credentials (env vars pointing to your accounts)
- Permission overrides for your development workflow
- Experimental hooks you are testing

**Put in `~/.claude/settings.json` (user-wide):**
- Organization-wide policies (deny destructive operations)
- MCP servers you use on every project (personal GitHub, Slack)
- Your preferred model settings

---

## Section 6: What's Next?

### The Ecosystem Is Rapidly Evolving

Claude Code, MCP servers, skills, and plugins are all developing rapidly. New capabilities arrive frequently -- what is experimental today may become a standard pattern tomorrow.

### Keep an Eye On

**Official sources:**
- Claude Code changelog and release notes
- Anthropic's developer documentation
- The `anthropics/skills` GitHub repository for new official skills

**Community sources:**
- `VoltAgent/awesome-agent-skills` for community-curated skills
- `K-Dense-AI/claude-scientific-skills` for scientific and research skills
- mcpguide.dev for new MCP servers
- claude-plugins.dev for plugin discovery
- SkillsMP.com for marketplace skills

**Emerging patterns:**
- Multi-agent orchestration patterns are still evolving -- expect more structured team workflows
- Plugin distribution and versioning will become more formalized
- MCP server ecosystem is growing rapidly -- new data source integrations appear weekly
- Memory and learning mechanisms will become more sophisticated

### Contribute Back

The best way to improve the ecosystem is to share what works:

1. **Create and share skills** for your domain. If you work in healthcare, finance, logistics, or any specialized field, your domain skill could save dozens of people from writing their own.

2. **Write custom agents** that encode your team's best practices. An agent that knows your company's coding standards, data governance rules, or architectural patterns is valuable to every team member.

3. **Build plugins** that package complete workflows. A "data science project starter" plugin with skills, agents, commands, and hooks is a powerful on-ramp for new team members.

4. **Report issues and suggest improvements** when you find rough edges. The community benefits from bug reports and feature requests.

### Join the Community

Data science with AI-assisted coding is a new discipline. The practices, patterns, and tools are being invented right now by people using them in real projects -- people like you. Whether you share a skill on GitHub, answer a question in a forum, or write about your experience, you are helping to shape how data science will be done.

---

## What You Learned

In this chapter, you explored the most advanced capabilities of Claude Code:

- **Agent Teams**: How to orchestrate multiple agents for complex tasks, with the Team Lead + Teammates architecture and TeammateTool communication. When to use teams vs single agents, and the trade-offs involved.
- **Plugin Creation**: Full walkthrough of building a distributable `.claude-plugin/` directory, the complete `plugin.json` manifest reference, local testing, and publishing considerations.
- **Persistent Memory**: How agents remember across sessions using `MEMORY.md`, the difference between project and global memory, practical patterns for experiment logs, data quality journals, and stakeholder glossaries.
- **Integration Patterns**: How to set up Claude Code + Jupyter + DuckDB + MLflow as a cohesive environment, managing multiple MCP servers, and handling secrets safely with environment variables.
- **Governance and Audit Trails**: Using hooks for compliance logging, the settings hierarchy (user > project shared > project local), deny rules for sensitive operations, and permission management for team environments.
- **Community and Ecosystem**: Where to find skills, plugins, and MCP servers, and how to contribute back to the growing ecosystem.

---

## Tutorial Complete

Congratulations. Over the course of this tutorial, you have:

1. **Set up Claude Code** and learned the fundamentals (Chapter 0)
2. **Defined a business problem** using the business-analyst agent and CRISP-DM (Chapter 1)
3. **Explored and understood your data** with DuckDB, custom commands, and EDA (Chapter 2)
4. **Prepared and engineered features** with the data-engineer agent and validation hooks (Chapter 3)
5. **Built and tuned models** with the ml-engineer agent and experiment tracking (Chapter 4)
6. **Evaluated results** with business impact translation and the qa-reviewer agent (Chapter 5)
7. **Deployed a prediction API** with Docker, monitoring, safety hooks, plugins, and git integration (Chapter 6)
8. **Learned to customize everything** -- skills, agents, commands, hooks, MCP servers, and CLAUDE.md (Chapter 7)
9. **Mastered advanced patterns** -- agent teams, plugins, memory, integrations, and governance (Chapter 8)

You now have the knowledge to take Claude Code from a general-purpose assistant to a domain-expert teammate that understands your data, follows your conventions, and scales with your most complex projects.

The configuration files, agents, skills, and hooks you built are not just tutorial exercises -- they are a working toolkit you can adapt for your next project. Fork it, customize it, and make it yours.
