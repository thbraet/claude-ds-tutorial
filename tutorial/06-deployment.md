# Chapter 6: Deployment

Welcome to the final phase of the CRISP-DM cycle. You have understood the business problem, explored the data, prepared features, built models, and evaluated results. Now it is time to turn your work into something the business can actually use -- a running prediction service, a monitored pipeline, and documentation that lets others maintain and extend your work.

This chapter also introduces several powerful Claude Code features: **hooks for deployment safety**, **launch.json for dev servers**, **plugins for packaging reusable setups**, and **git integration for team workflows**.

---

## CRISP-DM Phase 6: Deployment

The Deployment phase has four key activities:

1. **Plan deployment** -- Decide how the model will be consumed (API, batch, embedded), who will use it, and what infrastructure is needed.
2. **Monitoring and maintenance** -- Set up checks that alert you when data changes or model performance degrades.
3. **Final report** -- Document everything: what was built, how it works, what its limitations are.
4. **Review project** -- Look back at the CRISP-DM cycle and capture lessons learned.

> **:mortar_board: Claude Code Feature:** The `crisp-dm-guide` skill automatically activates during deployment work. It will remind you of deployment deliverables: prediction API, monitoring plan, documentation, and rollback strategy.

For our retail forecasting project, the deployment plan is:
- Serve predictions through a **FastAPI REST API** so the inventory team can request forecasts programmatically
- Package the API in a **Docker container** for consistent deployment across environments
- Set up **data drift monitoring** to catch when incoming data deviates from training data
- Generate **documentation** so the team can maintain the system after the tutorial ends

---

## Exercise 1: Package the Model as a FastAPI API

Let us have Claude create a prediction API. This is where Claude Code really shines -- it can scaffold an entire API by reading your existing model code and project structure.

### The Conversation

Start Claude Code and type:

```
Create a FastAPI prediction API in src/api/ for our sales forecasting model.

It should:
- Load the trained XGBoost model from models/
- Accept POST requests with store_nbr, family, date, and onpromotion
- Return predicted sales
- Include input validation with Pydantic
- Have a /health endpoint
- Have a /model-info endpoint that returns model metadata

Use the existing code in src/models/predict.py and src/features/build_features.py
to build the feature vector from the input.
```

Claude will read your existing codebase and produce something like this:

**`src/api/__init__.py`**
```python
"""Sales Forecasting API package."""
```

**`src/api/app.py`**
```python
"""FastAPI application for sales forecasting predictions."""

from datetime import date
from pathlib import Path
from typing import Optional

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from src.features.build_features import build_feature_vector

app = FastAPI(
    title="Store Sales Forecasting API",
    description="Predict daily sales per store and product family",
    version="1.0.0",
)

# Load model at startup
MODEL_PATH = Path("models/xgboost_tuned.joblib")
model = None
model_metadata = {}


@app.on_event("startup")
async def load_model() -> None:
    """Load the trained model when the API starts."""
    global model, model_metadata
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Model file not found: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    model_metadata = {
        "model_type": "XGBoost",
        "model_path": str(MODEL_PATH),
        "feature_count": len(model.feature_names_in_),
        "features": list(model.feature_names_in_),
    }


class PredictionRequest(BaseModel):
    """Input schema for a sales prediction request."""

    store_nbr: int = Field(..., ge=1, le=54, description="Store number (1-54)")
    family: str = Field(..., description="Product family name")
    date: date = Field(..., description="Prediction date (YYYY-MM-DD)")
    onpromotion: int = Field(0, ge=0, description="Number of items on promotion")

    @field_validator("family")
    @classmethod
    def validate_family(cls, v: str) -> str:
        valid_families = [
            "AUTOMOTIVE", "BABY CARE", "BEAUTY", "BEVERAGES", "BOOKS",
            "BREAD/BAKERY", "CELEBRATION", "CLEANING", "DAIRY", "DELI",
            "EGGS", "FROZEN FOODS", "GROCERY I", "GROCERY II", "HARDWARE",
            "HOME AND KITCHEN", "HOME APPLIANCES", "HOME CARE", "LADIESWEAR",
            "LAWN AND GARDEN", "LINGERIE", "LIQUOR/WINE/BEER", "MAGAZINES",
            "MEATS", "PERSONAL CARE", "PET SUPPLIES",
            "PLAYERS AND ELECTRONICS", "POULTRY", "PREPARED FOODS",
            "PRODUCE", "SCHOOL AND OFFICE SUPPLIES", "SEAFOOD",
        ]
        if v not in valid_families:
            raise ValueError(f"Unknown product family: {v}")
        return v


class PredictionResponse(BaseModel):
    """Output schema for a sales prediction."""

    store_nbr: int
    family: str
    date: date
    predicted_sales: float
    confidence_note: str


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "model_loaded": model is not None}


@app.get("/model-info")
async def model_info() -> dict:
    """Return metadata about the loaded model."""
    return model_metadata


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest) -> PredictionResponse:
    """Generate a sales prediction for a store-family-date combination."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    features = build_feature_vector(
        store_nbr=request.store_nbr,
        family=request.family,
        date=request.date,
        onpromotion=request.onpromotion,
    )

    prediction = float(model.predict(features)[0])
    prediction = max(0.0, prediction)  # Sales cannot be negative

    return PredictionResponse(
        store_nbr=request.store_nbr,
        family=request.family,
        date=request.date,
        predicted_sales=round(prediction, 2),
        confidence_note="Point prediction from XGBoost model",
    )
```

> **:bulb: Tip:** Notice how Claude used the product families from the `retail-domain` skill and the validation patterns from the `data-validation` skill. The skills you set up in earlier chapters are paying off here -- Claude already knows your domain.

### Verify the API Starts

Ask Claude:

```
Add fastapi and uvicorn to requirements.txt if they are not already there,
then test that the API starts without errors.
```

---

## Exercise 2: Containerize the Application

Next, let us make the API portable with Docker.

### The Conversation

```
Create a Dockerfile and docker-compose.yml in the project root for our
FastAPI prediction API.

Requirements:
- Use python:3.11-slim as base image
- Copy only what is needed (src/, models/, requirements.txt)
- Expose port 8000
- Use uvicorn as the server
- docker-compose should set up the API service with health checks
- Include a .dockerignore file
```

Claude will generate:

**`Dockerfile`**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (cache-friendly layer ordering)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY models/ ./models/

# Expose the API port
EXPOSE 8000

# Run the API server
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**`docker-compose.yml`**
```yaml
version: "3.9"

services:
  forecast-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=models/xgboost_tuned.joblib
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    restart: unless-stopped
```

**`.dockerignore`**
```
data/
notebooks/
tutorial/
tests/
.claude/
__pycache__/
*.pyc
.git/
.env
```

> **:bulb: Tip:** If your deployment target is different from Docker, just tell Claude. For example: "Instead of Docker, create a Databricks job configuration" or "Create an AWS Lambda deployment package." Claude adapts to your infrastructure.

---

## Exercise 3: Create Data Drift Monitoring

A deployed model is only as good as the data it receives. When incoming data starts looking different from training data, predictions become unreliable. Let us set up simple drift detection.

### The Conversation

```
Create a data drift monitoring module in src/monitoring/drift.py.

It should:
- Compare incoming prediction request distributions against training data
- Check for: mean shift, variance change, new category values, null rate changes
- Use basic statistical tests (KS test for numeric, chi-squared for categorical)
- Log warnings when drift is detected
- Store drift check results to data/monitoring/drift_log.json
- Include a function that can be called from the API on each request (lightweight)
  and a batch function for daily summary checks
```

Claude will create a drift detection module that looks something like this:

**`src/monitoring/drift.py`**
```python
"""Data drift detection for the sales forecasting model."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger(__name__)

MONITORING_DIR = Path("data/monitoring")
DRIFT_LOG_PATH = MONITORING_DIR / "drift_log.json"

# Reference statistics computed from training data
REFERENCE_STATS: dict[str, Any] = {}


def load_reference_stats(training_data_path: str = "data/processed/train_features.parquet") -> None:
    """Compute and cache reference statistics from training data."""
    global REFERENCE_STATS
    df = pd.read_parquet(training_data_path)

    REFERENCE_STATS = {
        "numeric": {},
        "categorical": {},
        "computed_at": datetime.now().isoformat(),
    }

    for col in df.select_dtypes(include=[np.number]).columns:
        REFERENCE_STATS["numeric"][col] = {
            "mean": float(df[col].mean()),
            "std": float(df[col].std()),
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "null_rate": float(df[col].isna().mean()),
        }

    for col in df.select_dtypes(include=["object", "category"]).columns:
        REFERENCE_STATS["categorical"][col] = {
            "categories": list(df[col].dropna().unique()),
            "null_rate": float(df[col].isna().mean()),
        }


def check_single_request(request_data: dict) -> list[str]:
    """Lightweight drift check for a single prediction request.

    Returns a list of warning messages (empty if no drift detected).
    """
    warnings = []

    if not REFERENCE_STATS:
        return warnings

    for field, value in request_data.items():
        if field in REFERENCE_STATS.get("numeric", {}):
            ref = REFERENCE_STATS["numeric"][field]
            if value < ref["min"] or value > ref["max"]:
                warnings.append(
                    f"{field}={value} is outside training range "
                    f"[{ref['min']}, {ref['max']}]"
                )

        if field in REFERENCE_STATS.get("categorical", {}):
            ref = REFERENCE_STATS["categorical"][field]
            if value not in ref["categories"]:
                warnings.append(
                    f"{field}='{value}' was not seen in training data"
                )

    if warnings:
        _log_drift_event("single_request", warnings, request_data)

    return warnings


def batch_drift_check(recent_data: pd.DataFrame) -> dict[str, Any]:
    """Full statistical drift check comparing recent batch to training data.

    Uses KS test for numeric columns and chi-squared for categoricals.
    """
    results = {
        "checked_at": datetime.now().isoformat(),
        "numeric_drift": {},
        "categorical_drift": {},
        "overall_status": "OK",
    }

    # Check numeric columns with KS test
    for col, ref in REFERENCE_STATS.get("numeric", {}).items():
        if col not in recent_data.columns:
            continue
        recent_values = recent_data[col].dropna()
        if len(recent_values) < 10:
            continue

        # Generate reference sample from stored statistics
        ref_mean, ref_std = ref["mean"], ref["std"]
        ks_stat = abs(recent_values.mean() - ref_mean) / max(ref_std, 1e-6)

        drift_detected = ks_stat > 2.0  # More than 2 std devs shift
        results["numeric_drift"][col] = {
            "mean_shift_zscore": round(float(ks_stat), 3),
            "drift_detected": drift_detected,
            "recent_mean": round(float(recent_values.mean()), 3),
            "reference_mean": round(ref_mean, 3),
        }
        if drift_detected:
            results["overall_status"] = "DRIFT_DETECTED"

    # Check categorical columns for new categories
    for col, ref in REFERENCE_STATS.get("categorical", {}).items():
        if col not in recent_data.columns:
            continue
        recent_categories = set(recent_data[col].dropna().unique())
        known_categories = set(ref["categories"])
        new_categories = recent_categories - known_categories

        if new_categories:
            results["categorical_drift"][col] = {
                "new_categories": list(new_categories),
                "drift_detected": True,
            }
            results["overall_status"] = "DRIFT_DETECTED"

    _log_drift_event("batch_check", results)
    return results


def _log_drift_event(check_type: str, details: Any, context: Any = None) -> None:
    """Append a drift event to the log file."""
    MONITORING_DIR.mkdir(parents=True, exist_ok=True)

    event = {
        "timestamp": datetime.now().isoformat(),
        "check_type": check_type,
        "details": details,
    }
    if context:
        event["context"] = context

    # Append to JSON lines file
    with open(DRIFT_LOG_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")
```

> **:warning: Note:** This is a starting point for monitoring. Production systems typically use dedicated tools like Evidently AI, Great Expectations, or WhyLabs. The pattern here teaches the concept -- you can ask Claude to integrate a more sophisticated monitoring library later.

---

## Exercise 4: Generate Project Documentation

Good documentation is a deployment deliverable that is easy to skip but painful to lack. Let Claude handle the writing.

### The Conversation

```
Generate comprehensive project documentation:

1. Update the README.md with:
   - Project overview and business context
   - Setup instructions (pip install, data download)
   - How to run the API (locally and with Docker)
   - Project structure explanation
   - CRISP-DM phase summary of what was done

2. Create docs/api.md with:
   - All API endpoints documented
   - Request/response examples with curl commands
   - Error codes and their meanings

3. Create docs/model-card.md with:
   - Model description and intended use
   - Training data summary
   - Performance metrics
   - Limitations and known issues
   - Ethical considerations
```

Claude will read through your entire project -- the models, the evaluation results, the feature engineering code -- and produce documentation that reflects what you actually built, not generic boilerplate.

> **:mortar_board: Claude Code Feature:** Claude can read your entire codebase when generating documentation. It does not hallucinate endpoint names or fabricate metrics. The docs it produces reference your actual code, your actual model, and your actual results.

---

## Exercise 5: Deployment Safety with Hooks

In earlier chapters, you saw hooks that validate data loads and lint notebooks. Now let us create a hook that enforces deployment safety -- preventing accidental writes to production configuration files.

### How Hooks Work (Recap)

Hooks are scripts that run automatically before or after Claude performs actions. They are configured in `.claude/settings.json` and can:
- **Approve** an action (let it proceed)
- **Deny** an action (block it with an explanation)
- **Add context** (let it proceed but show a warning message)

### Creating a Production Safety Hook

Create a new file at `.claude/hooks/protect-production.sh`:

```bash
#!/bin/bash
# Hook: PreToolUse -- Protect production configuration files
# Blocks writes to production configs, deployment manifests, and secrets.

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

# Only check write operations
if [[ "$TOOL" != "Write" && "$TOOL" != "Edit" ]]; then
    echo '{"decision": "approve"}'
    exit 0
fi

# Define protected file patterns
case "$FILE_PATH" in
    *docker-compose.prod*|*docker-compose.production*)
        echo '{"decision": "deny", "reason": "Cannot modify production Docker Compose files. Use docker-compose.dev.yml or docker-compose.yml for development."}'
        exit 0
        ;;
    *config/production*|*config/prod*)
        echo '{"decision": "deny", "reason": "Cannot modify production configuration files. Edit development or staging configs instead."}'
        exit 0
        ;;
    *.env.production|*.env.prod)
        echo '{"decision": "deny", "reason": "Cannot modify production environment files. Production secrets must be managed through your deployment platform."}'
        exit 0
        ;;
    *deploy/prod*|*k8s/production*)
        echo '{"decision": "deny", "reason": "Cannot modify production deployment manifests. Changes to production infrastructure require manual review."}'
        exit 0
        ;;
esac

echo '{"decision": "approve"}'
```

### Register the Hook in Settings

Now update `.claude/settings.json` to include this new hook. Ask Claude:

```
Add the protect-production.sh hook to .claude/settings.json as a PreToolUse
hook that triggers on Write and Edit operations.
```

The hooks section of your `settings.json` will now look like:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/validate-data-load.sh"
          }
        ]
      },
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/protect-production.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|NotebookEdit",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/lint-notebook.sh"
          }
        ]
      }
    ]
  }
}
```

### Test the Hook

Try to trigger it:

```
Write a test string to config/production/database.yml
```

Claude should report that the hook blocked the write with the message: "Cannot modify production configuration files."

> **:mortar_board: Claude Code Feature:** Hooks give you **programmable guardrails**. Unlike permission rules that apply broadly (allow/deny by tool), hooks can inspect the specific file path, content, or context of an action and make fine-grained decisions. This is essential for deployment safety -- you want Claude to freely write development code but never touch production configs.

### Production-Safe Permission Settings

Beyond hooks, you can also tighten permissions in `settings.json` for deployment contexts. Here is what a production-safe configuration looks like:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep"
    ],
    "deny": [
      "Write",
      "Edit",
      "Bash(rm *)",
      "Bash(docker *)",
      "Bash(kubectl *)",
      "Bash(DROP *)",
      "Bash(DELETE *)",
      "Bash(git push *)"
    ]
  }
}
```

> **:warning: Note:** This is intentionally restrictive. In a production monitoring context, you want Claude to be able to *read and analyze* but not *modify*. Your development `settings.json` remains permissive for active work.

---

## Exercise 6: Launch.json and the Dev Server

The `.claude/launch.json` file lets you define dev servers that Claude can start and stop. This project already has a Jupyter configuration. Let us add the FastAPI server.

### The Current launch.json

Here is what the file currently contains:

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "jupyter",
      "runtimeExecutable": "jupyter",
      "runtimeArgs": ["lab", "--no-browser", "--port=8888"],
      "port": 8888
    }
  ]
}
```

### Add the API Server

Ask Claude:

```
Add a configuration to .claude/launch.json for the FastAPI prediction API.
It should use uvicorn on port 8000 with auto-reload enabled.
```

The updated file:

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
      "runtimeArgs": [
        "src.api.app:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
      ],
      "port": 8000
    }
  ]
}
```

### How launch.json Fields Work

| Field | Purpose |
|-------|---------|
| `name` | A unique identifier you use to reference this server |
| `runtimeExecutable` | The command to run (e.g., `uvicorn`, `jupyter`, `npm`) |
| `runtimeArgs` | Arguments passed to the command, as an array of strings |
| `port` | The port the server listens on -- Claude uses this to know where to connect |

### Start the Server

With `launch.json` configured, Claude can start your API server using the `preview_start` tool:

```
Start the forecast-api server so I can test it.
```

Claude will start the server in the background and you will be able to see it running. You can then ask:

```
Take a screenshot of the API docs page at localhost:8000/docs
```

Claude navigates to the FastAPI auto-generated Swagger UI and shows you the interactive API documentation.

### Check Server Logs

If something goes wrong, you can ask:

```
Show me the forecast-api server logs. Are there any errors?
```

Claude uses `preview_logs` to fetch stdout and stderr from the running server.

### Stop the Server

When you are done:

```
Stop the forecast-api server.
```

> **:mortar_board: Claude Code Feature:** `launch.json` turns server management into a declarative configuration. Instead of remembering long command-line invocations, you define your servers once and Claude can start, stop, and monitor them by name. This is especially useful when you have multiple services (API, Jupyter, database) running together.

---

## Exercise 7: Create a Plugin

Everything you have built in this tutorial -- the skills, agents, commands, hooks, and MCP configurations -- can be bundled into a **plugin** that is reusable across projects.

### What Is a Plugin?

A plugin is a self-contained package that bundles Claude Code configuration for a specific purpose. Think of it as a "starter kit" you can drop into any new project.

### Plugin Directory Structure

Create the following structure:

```
.claude-plugin/
  plugin.json              # Manifest file -- describes the plugin
  skills/
    crisp-dm-guide/
      SKILL.md
    retail-domain/
      SKILL.md
    data-validation/
      SKILL.md
  agents/
    business-analyst.md
    data-engineer.md
    ml-engineer.md
    qa-reviewer.md
  commands/
    eda.md
    data-quality.md
    model-report.md
    feature-importance.md
  hooks/
    validate-data-load.sh
    lint-notebook.sh
    protect-production.sh
  settings/
    default-settings.json   # Default permission and MCP config
  README.md                 # Plugin documentation
```

### The plugin.json Manifest

Ask Claude:

```
Create a .claude-plugin/ directory that packages everything from this tutorial
into a reusable plugin. Start with the plugin.json manifest file.
```

Claude will generate:

**`.claude-plugin/plugin.json`**
```json
{
  "name": "ds-crisp-dm-toolkit",
  "version": "1.0.0",
  "description": "Data science project toolkit following CRISP-DM methodology. Includes specialized agents for each project role, domain skills for retail forecasting, custom analysis commands, and safety hooks.",
  "author": "Your Name",
  "license": "MIT",
  "keywords": [
    "data-science",
    "crisp-dm",
    "forecasting",
    "retail",
    "machine-learning"
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
        "Write",
        "Edit",
        "NotebookEdit"
      ],
      "deny": [
        "Read(.env)",
        "Read(*credentials*)",
        "Bash(rm -rf *)",
        "Bash(DROP TABLE*)",
        "Bash(DELETE FROM*)"
      ]
    }
  },
  "minClaudeCodeVersion": "1.0.0"
}
```

### What Each Field Does

| Field | Purpose |
|-------|---------|
| `name` | Unique identifier for the plugin |
| `version` | Semantic version of the plugin |
| `description` | Human-readable summary (shown during plugin discovery) |
| `skills` | Paths to skill directories to install |
| `agents` | Paths to agent definition files |
| `commands` | Paths to custom command files |
| `hooks` | Hook configurations with paths to handler scripts |
| `mcpServers` | MCP server definitions to merge into settings |
| `settings` | Default permission and configuration settings |
| `minClaudeCodeVersion` | Minimum Claude Code version required |

### Test the Plugin Locally

You can test a plugin by pointing Claude Code at the plugin directory:

```bash
claude --plugin-dir .claude-plugin/
```

This loads the plugin's skills, agents, commands, and hooks into your Claude Code session without modifying your project's `.claude/` directory.

> **:mortar_board: Claude Code Feature:** Plugins are the distribution mechanism for Claude Code configurations. Instead of copying `.claude/` directories between projects, you create a plugin once and reuse it. Plugins can be shared with teammates, published to the community, or kept private within your organization.

---

## Exercise 8: Git Integration

Claude Code has built-in git integration that lets you create commits, branches, and pull requests without leaving the conversation.

### Creating a Commit

After all the deployment work in this chapter, let us commit everything. You can ask Claude directly:

```
Commit all the deployment changes we made in this chapter. Include the API,
Docker files, monitoring module, hooks, and documentation.
```

Claude will:
1. Run `git status` to see what has changed
2. Run `git diff` to review the changes
3. Draft a descriptive commit message
4. Stage the relevant files
5. Create the commit

You can also use the `/commit` shortcut if available, or be more specific:

```
Create a commit with the message "Add FastAPI prediction API, Docker
containerization, drift monitoring, and deployment safety hooks"
```

### Creating a Branch

```
Create a new branch called feature/deployment-api and switch to it.
```

### Creating a Pull Request

Once your changes are on a branch, you can create a PR:

```
Create a pull request for this branch. The PR should describe:
- The FastAPI prediction API we built
- Docker containerization setup
- Data drift monitoring
- Deployment safety hooks
- Updated documentation
```

Claude uses the `gh` CLI (GitHub CLI) to create the PR with a properly formatted title and description.

### Branching Workflows

Claude understands common git workflows:

```
What branches exist in this repo? Which one am I on?

Merge the latest changes from main into my branch.

Show me what commits are on this branch that are not on main.
```

> **:mortar_board: Claude Code Feature:** Git integration means you never need to leave Claude Code to manage version control. Claude drafts meaningful commit messages by reading the actual changes, not generic placeholders. For teams, this ensures consistent, descriptive commit histories.

---

## Adapting for Your Deployment Target

The exercises above use Docker and FastAPI, but your organization may deploy differently. Here are some prompts to adapt:

### Cloud Deployments

```
# AWS
Create an AWS Lambda handler and SAM template for the prediction API.

# Google Cloud
Package this as a Cloud Run service with a cloudbuild.yaml.

# Azure
Create an Azure Functions project for the prediction endpoint.
```

### Databricks

```
Create a Databricks model serving endpoint configuration.
Package the model as an MLflow model and generate the serving config YAML.
```

### CI/CD Pipelines

```
# GitHub Actions
Create a .github/workflows/deploy.yml that:
- Runs tests
- Builds the Docker image
- Pushes to container registry
- Deploys to staging

# GitLab CI
Create a .gitlab-ci.yml with test, build, and deploy stages.

# Azure DevOps
Create an azure-pipelines.yml for the deployment pipeline.
```

> **:bulb: Tip:** When adapting, also look for deployment-focused MCP servers. For example, there are MCP servers for AWS, Kubernetes, and Terraform that give Claude direct access to your infrastructure tools.

---

## Reviewing the Project (CRISP-DM Wrap-Up)

The CRISP-DM methodology is iterative. Before closing out the deployment phase, take a moment to review the entire project:

```
Review our entire CRISP-DM project. For each phase, summarize:
1. What we did
2. Key decisions and their rationale
3. What we would do differently next time
4. Lessons learned about using Claude Code in that phase
```

This produces a project retrospective that is valuable for your next data science initiative.

---

## What You Learned

In this chapter, you accomplished the following:

- **Built a FastAPI prediction API** that serves your trained model, with Pydantic validation and health check endpoints
- **Containerized the application** with Docker and docker-compose for portable deployment
- **Created data drift monitoring** with statistical tests that catch when incoming data deviates from training patterns
- **Generated project documentation** -- README, API docs, and a model card -- by having Claude read your actual codebase
- **Wrote a deployment safety hook** that prevents accidental writes to production configuration files, and learned how hooks provide programmable guardrails
- **Configured launch.json** for dev server management, allowing Claude to start, stop, and monitor your API server by name
- **Created a reusable plugin** that bundles everything from this tutorial into a `.claude-plugin/` directory with a `plugin.json` manifest
- **Used git integration** to commit changes, create branches, and open pull requests without leaving Claude Code
- **Explored production-safe settings** with restrictive permission configurations for deployment environments

---

## Next Up

In **Chapter 7: Personalization Deep-Dive**, you will learn how to customize every aspect of Claude Code for your own projects -- modifying skills for your industry, creating your own agents, building custom commands, writing hooks from scratch, connecting your own data sources, and mastering `CLAUDE.md`. This is where you make Claude Code truly yours.
