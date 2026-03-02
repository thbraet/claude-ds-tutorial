# Chapter 3: Data Preparation

> **CRISP-DM Phase 3** -- Select data, clean data, construct features, integrate data, format data

Welcome to the hands-on heart of data science work. Data preparation typically consumes 60--80% of a real project's time. In this chapter, you will use Claude Code to build a complete data pipeline -- from messy raw CSVs to clean, feature-rich parquet files ready for modeling.

You do not need to memorize pandas syntax or worry about getting every function call right. Claude Code will write the code for you. Your job is to *direct* the work: tell Claude what you need, check what it produces, and iterate until the pipeline is solid.

**Time estimate:** 60--90 minutes

**What you will build:**
- A data cleaning pipeline (`src/data/clean.py`)
- A feature engineering module (extending `src/features/build_features.py`)
- Automated data validation hooks
- A pytest test suite for the pipeline

**Prerequisites:** You should have completed Chapter 2 (Data Understanding) and have the raw CSV files in `data/raw/`.

---

## What Makes This Phase Different with Claude Code?

Without Claude Code, data preparation means hours of writing boilerplate pandas code, debugging dtype mismatches, and manually checking for nulls. With Claude Code, you describe *what* you want in plain English, and Claude writes the Python. You review, iterate, and move on.

But the real power comes from three features you will learn in this chapter:

1. **Subagents** -- specialized AI assistants tuned for specific tasks (like data engineering)
2. **Hooks** -- automated checks that run every time Claude modifies a file
3. **Plan mode** -- a way to think through architecture before writing any code

Let us get started.

---

## Exercise 1: Build a Data Cleaning Pipeline

In this exercise, you will ask Claude to create a complete data cleaning pipeline. This is a great example of the **Write tool** in action -- Claude will create new Python files and modify existing ones, placing code exactly where it belongs in your project structure.

### Step 1: Open Claude Code in your project

Open your terminal, navigate to the project directory, and start Claude Code:

```
cd ~/Documents/claude-ds-tutorial
claude
```

### Step 2: Ask Claude to build the cleaning pipeline

Type this prompt exactly:

```
Build a data cleaning pipeline in src/data/clean.py that:

1. Reads all raw CSVs from data/raw/ using our existing load functions in src/data/load.py
2. Cleans the training data:
   - Remove exact duplicate rows
   - Fill missing oil prices using forward-fill then backward-fill
   - Convert date columns to datetime if not already
   - Ensure store_nbr and family are categorical
   - Clip any negative sales values to 0
   - Validate all data using src/data/validate.py
3. Merges training data with stores, oil prices, holidays, and transactions
4. Saves the merged clean dataset to data/processed/train_clean.parquet
5. Includes a main() function so I can run it with: python src/data/clean.py

Follow the project conventions in CLAUDE.md -- use parquet (never pickle),
snake_case column names, type hints on all functions, and docstrings.
```

Press Enter and watch Claude work.

### What Just Happened?

Claude read your project structure, found the existing `src/data/load.py` and `src/data/validate.py` files, and created a new `src/data/clean.py` that integrates with them. Let us break down what you will see:

1. **Claude used the Read tool** to examine your existing code -- it looked at `load.py` to understand your data loading functions and `validate.py` to understand your validation rules.
2. **Claude used the Write tool** to create `src/data/clean.py` -- a brand new file placed in exactly the right location.
3. **Claude followed your CLAUDE.md conventions** -- parquet output, snake_case names, type hints, and docstrings.

> **What Claude Code Feature: The Write and Edit Tools**
>
> When Claude needs to create or modify files, it uses two precision tools:
> - **Write** creates a new file (or completely replaces an existing one)
> - **Edit** makes surgical changes to specific parts of an existing file
>
> Claude chooses the right tool automatically. For a new file like `clean.py`, it uses Write. For adding a function to an existing file, it uses Edit. You never need to tell Claude which tool to use -- just describe what you want.

### Step 3: Run the pipeline

Ask Claude to run it:

```
Run the cleaning pipeline and show me a summary of the output
```

Claude will use the **Bash tool** to execute:

```bash
python src/data/clean.py
```

> **Tip:** If you see an import error, just tell Claude: "Fix the import error and try again." Claude will read the error, edit the file, and rerun it. This fix-and-retry loop is one of the most productive patterns in Claude Code.

### Step 4: Verify the output

```
Check the output file data/processed/train_clean.parquet -- show me the shape,
column names, data types, and first 5 rows
```

Claude will write a quick Python snippet to load and inspect the parquet file. Confirm that:
- The file exists and is in parquet format (not CSV!)
- Column names are all in snake_case
- Dates are datetime, categoricals are category type
- No negative sales values remain

---

## Exercise 2: Feature Engineering with the Data Engineer Subagent

Now you will learn one of the most powerful Claude Code features: **subagents**. Instead of using the general-purpose Claude, you will invoke a specialized data engineering agent that knows exactly how to build features for retail forecasting.

### What Are Subagents?

> **Claude Code Feature: Subagents**
>
> A subagent is a specialized version of Claude that has its own instructions, tools, and skills. Think of it like calling in a specialist:
>
> - The **main Claude** is a generalist -- good at everything, expert at nothing specific
> - A **subagent** is a specialist -- deeply configured for one type of work
>
> Subagents are defined as markdown files in `.claude/agents/`. Each file contains a frontmatter header (like settings) and a body (the specialist's instructions).

### Deep Dive: The Data Engineer Agent

Let us look at the agent file that powers the data engineer subagent. Open `.claude/agents/data-engineer.md` in your editor, or ask Claude to show it:

```
Show me the contents of .claude/agents/data-engineer.md
```

Here is the full file:

```markdown
---
name: data-engineer
description: "Data preparation specialist for data science pipelines. Expert
  in pandas, data cleaning, feature engineering, data validation, and ETL
  patterns. Use this agent for data wrangling, building reproducible data
  pipelines, and feature engineering."
tools: Read, Glob, Grep, Bash, Write, Edit
model: sonnet
maxTurns: 40
skills:
  - data-validation
  - retail-domain
---

You are a senior data engineer specialized in building clean, reproducible
data pipelines for data science projects.

## Your Role

You help data scientists and analysts:
- Load and explore raw data files
- Clean messy data systematically
- Engineer features from raw variables
- Build reproducible data pipelines in Python
- Validate data quality at every step
- Optimize data storage and formats

## Technical Stack

- **pandas** for data manipulation (prefer vectorized operations over loops)
- **numpy** for numerical operations
- **pyarrow/parquet** for storage (never pickle, always parquet)
- **DuckDB** for SQL-based transformations when cleaner than pandas
- **pytest** for testing data pipelines

...
```

Let us break down the **frontmatter fields** (the part between the `---` markers):

| Field | Value | What It Does |
|-------|-------|-------------|
| `name` | `data-engineer` | The identifier you use to invoke this agent |
| `description` | (long string) | Helps Claude decide when to suggest this agent |
| `tools` | `Read, Glob, Grep, Bash, Write, Edit` | Which tools the agent can use (scoped permissions) |
| `model` | `sonnet` | Which Claude model powers this agent (sonnet is fast and capable) |
| `maxTurns` | `40` | Maximum back-and-forth steps before the agent stops |
| `skills` | `data-validation, retail-domain` | Additional knowledge files loaded for this agent |

The **body** (below the frontmatter) contains the agent's detailed instructions -- its persona, coding conventions, feature engineering patterns, and output expectations.

> **Tip:** The `skills` field is what makes subagents truly powerful. The data-engineer agent automatically loads the `data-validation` skill (which knows our dataset's validation rules) and the `retail-domain` skill (which knows grocery retail patterns like seasonality and promotion effects). The general Claude does not have this focused context.

### Step 1: Invoke the data engineer subagent

In your Claude Code session, type:

```
@data-engineer Add feature engineering to our pipeline. Working with the clean
dataset in data/processed/train_clean.parquet, extend src/features/build_features.py
to add these features:

1. Lag features: sales at 1, 7, 14, 28, and 364 days ago (grouped by store and family)
2. Rolling statistics: 7-day and 28-day rolling mean, std, min, max of sales
3. Time features: day_of_week, month, quarter, week_of_year, is_weekend,
   is_month_start, is_month_end, day_of_year
4. Holiday features: is_holiday, days_until_next_holiday, days_since_last_holiday
5. Promotion features: promo_rolling_7d_sum, promo_rolling_28d_sum

Save the feature-enriched dataset to data/processed/train_features.parquet.
Make sure lag and rolling features use shift(1) to prevent data leakage.
```

The `@data-engineer` prefix tells Claude Code to route this task to the specialized subagent.

### What Just Happened?

The data engineer subagent:

1. **Read the existing code** in `build_features.py` to understand what functions already existed (`add_time_features`, `add_lag_features`, `add_rolling_features`)
2. **Extended the file** rather than rewriting it -- it used the Edit tool to add new functions alongside the existing ones
3. **Applied retail domain knowledge** from its `retail-domain` skill -- it knew to include holiday lead/lag features and promotion rolling sums because those matter in grocery forecasting
4. **Used shift(1) consistently** to prevent data leakage -- the `data-validation` skill reinforced this pattern

> **Why Subagents Produce Better Results**
>
> You could have asked the general Claude the same question and gotten decent code. But the subagent produced *better* results because:
>
> 1. **Focused instructions** -- It was told "you are a senior data engineer" with specific coding patterns, not a generalist trying to do everything.
> 2. **Loaded skills** -- The retail-domain skill gave it knowledge about grocery-specific features (holiday lead effects, perishability patterns). The data-validation skill made it vigilant about leakage prevention.
> 3. **Scoped tools** -- It had exactly the tools it needed (Read, Write, Edit, Bash) and nothing extra, keeping it focused.
> 4. **Higher turn limit** -- With `maxTurns: 40`, it could take its time to read existing code, plan, write, test, and iterate without running out of steps.

### Step 2: Verify the features

```
Load data/processed/train_features.parquet and show me the new columns that
were added, with their data types and a sample of non-null values
```

Check that all the feature groups are present: lag features, rolling statistics, time features, holiday features, and promotion features.

---

## Exercise 3: Automated Validation with Hooks

Every time Claude writes or edits a notebook file in this project, an automated quality check runs behind the scenes. This is powered by **hooks** -- scripts that fire automatically before or after Claude uses specific tools.

### What Are Hooks?

> **Claude Code Feature: Hooks**
>
> Hooks are shell scripts that run automatically at specific points in Claude's workflow:
>
> - **PreToolUse** hooks run *before* Claude executes a tool -- they can approve, warn, or block the action
> - **PostToolUse** hooks run *after* Claude executes a tool -- they can validate the result and alert Claude to issues
>
> Think of hooks as automated guardrails. They enforce your team's standards without you having to remember to check every time.

### Deep Dive: The PostToolUse Hook Configuration

Let us examine how hooks are configured. Open `.claude/settings.json`:

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

Let us break this down:

| Setting | Value | What It Means |
|---------|-------|---------------|
| `PostToolUse` | (array) | These hooks fire *after* a tool runs |
| `matcher` | `"Write\|Edit\|NotebookEdit"` | Fires when Claude uses Write, Edit, OR NotebookEdit |
| `type` | `"command"` | The hook runs a shell command |
| `command` | `"bash .claude/hooks/lint-notebook.sh"` | The script to execute |

The **matcher pattern** uses `|` (pipe) to match multiple tool names. So this single hook fires after any file-writing operation.

### Deep Dive: The lint-notebook.sh Script

Here is the full hook script at `.claude/hooks/lint-notebook.sh`:

```bash
#!/bin/bash
# Hook: PostToolUse -- Lint and validate after notebook modifications
# This hook runs after Write/Edit operations on .ipynb files.

# Read the JSON input from stdin
INPUT=$(cat)

# Extract tool name and file path
TOOL=$(echo "$INPUT" | python3 -c "import sys,json; \
  print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null)
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; \
  inp=json.load(sys.stdin); \
  print(inp.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

# Only check Write/Edit operations on notebooks
if [[ "$TOOL" != "Write" && "$TOOL" != "Edit" && \
      "$TOOL" != "NotebookEdit" ]]; then
    exit 0
fi

case "$FILE_PATH" in
    *.ipynb)
        if [ -f "$FILE_PATH" ]; then
            python3 -c "
import json, sys

with open('$FILE_PATH', 'r') as f:
    try:
        nb = json.load(f)
    except json.JSONDecodeError:
        print('ERROR: Notebook is not valid JSON after edit')
        sys.exit(1)

issues = []
for i, cell in enumerate(nb.get('cells', [])):
    if 'source' not in cell:
        issues.append(f'Cell {i} has no source field')
    if cell.get('cell_type') == 'code':
        source = ''.join(cell.get('source', []))
        if 'import *' in source:
            issues.append(f'Cell {i}: Avoid wildcard imports')
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
```

Here is what happens step by step when Claude writes to a notebook:

1. Claude uses the Write, Edit, or NotebookEdit tool on a `.ipynb` file
2. The hook receives a JSON payload on stdin with the tool name and file path
3. The script checks if the file is a notebook (`.ipynb` extension)
4. If so, it validates the JSON structure and checks for:
   - Missing `source` fields in cells
   - Wildcard imports (`import *`) which are bad practice
   - Possible sensitive data (passwords, secrets) accidentally left in code
5. It prints warnings or a success message back to Claude
6. Claude sees the output and can fix any issues automatically

### Step 1: See the hook in action

Ask Claude to create a notebook so you can watch the hook fire:

```
Create a notebook at notebooks/03_data_preparation.ipynb with cells that:
1. Import pandas and our src.data.load module
2. Load the clean training data from data/processed/train_clean.parquet
3. Display the shape, dtypes, and first 5 rows
4. Show a summary of missing values
```

After Claude creates the notebook, look at the output. You should see either:

```
Notebook validation passed.
```

or warnings about any issues the hook detected.

### Step 2: See the hook catch a problem

Now intentionally trigger a warning:

```
Add a cell to the notebook that contains "from pandas import *" -- I want to see
what the lint hook catches
```

You should see the hook produce:

```
Notebook lint warnings:
  - Cell N: Avoid wildcard imports (import *)
```

Claude will notice this warning and may offer to fix it. That is the power of hooks -- they create a feedback loop where issues are caught and fixed in real time.

> **Note:** The PreToolUse hook (`validate-data-load.sh`) also runs in this project. It fires before any Read operation on data files, warning you if a file is larger than 100MB and blocking access to sensitive files like `.env` or credentials. This is how you protect data governance rules at the tooling level.

---

## Exercise 4: Testing the Data Pipeline

A pipeline without tests is a pipeline waiting to break. In this exercise, you will have Claude create pytest tests for your cleaning and feature engineering code.

### Step 1: Ask Claude to create tests

```
Create pytest tests in tests/test_data_pipeline.py for our data preparation code:

1. Test the cleaning pipeline (src/data/clean.py):
   - Verify that output has no duplicate rows
   - Verify that sales are all non-negative after cleaning
   - Verify that date column is datetime type
   - Verify that output is saved as parquet (not CSV)
   - Verify that all expected columns are present after merge

2. Test the feature engineering (src/features/build_features.py):
   - Verify lag features have correct number of NaN values
   - Verify rolling features use shift(1) -- value at time t should NOT
     include sales at time t
   - Verify time features are in valid ranges (day_of_week 0-6, month 1-12)
   - Verify no data leakage: features at time t only use data from before t

Use small synthetic DataFrames as fixtures, not the real data files.
Include clear docstrings explaining what each test checks.
```

### What Just Happened?

Claude created a test file that:
- Uses `@pytest.fixture` to create small, controlled test DataFrames
- Tests each function independently with known inputs and expected outputs
- Includes a data leakage test (critical for time series projects)
- Follows project conventions with docstrings and type hints

### Step 2: Run the tests

```
Run the tests with python -m pytest tests/test_data_pipeline.py -v and show me
the results
```

Claude will execute:

```bash
python -m pytest tests/test_data_pipeline.py -v
```

The `-v` flag shows verbose output so you can see each test name and whether it passed or failed.

> **Tip:** If any tests fail, do not panic. Just tell Claude: "Fix the failing tests" and it will read the error messages, identify the problem, and edit either the test or the source code. This is the normal development loop -- write tests, see failures, fix code, see green.

### Step 3: Run the full test suite

```
Run the entire test suite with python -m pytest tests/ -v to make sure
we haven't broken anything
```

This runs all tests in the `tests/` directory, including the existing ones from `test_data_validation.py`, `test_features.py`, and `test_model.py`.

---

## Exercise 5: Planning Before Coding with Plan Mode

Sometimes the right move is to *think* before you *build*. Plan mode lets you have a design conversation with Claude before any code gets written.

### What Is Plan Mode?

> **Claude Code Feature: Plan Mode**
>
> Plan mode is a way to ask Claude to analyze, think, and propose an approach *without* writing any files or running any commands. It is like having an architecture discussion with a senior colleague before starting implementation.
>
> **When to use Plan mode:**
> - Before building a complex multi-file pipeline
> - When you are unsure about the right architecture
> - When you want to compare multiple approaches
> - Before refactoring existing code
>
> **When NOT to use Plan mode:**
> - For simple, well-defined tasks (just do them)
> - When you already know exactly what you want
>
> **How to enter Plan mode:**
> - Press `Shift+Tab` to toggle into Plan mode, or type your message and ask Claude to plan
>
> **How to exit Plan mode:**
> - Press `Shift+Tab` again to toggle back to normal mode, or simply tell Claude to proceed with implementation

### Step 1: Enter Plan mode and plan the pipeline architecture

Press `Shift+Tab` to enter Plan mode (you will see an indicator that Plan mode is active), then type:

```
Plan the complete data preparation pipeline architecture for this project.

Consider:
- How should the pipeline stages connect? (raw -> clean -> features -> ready)
- Should each stage be a separate script or one monolithic pipeline?
- How do we handle the train vs test split in features that need history?
- Where should we validate data quality?
- How do we make the pipeline idempotent (safe to rerun)?

Don't write any code yet -- just give me the architecture plan.
```

### What Just Happened?

Claude analyzed the project structure and proposed an architecture without touching any files. You should see a plan that covers:

- **Pipeline stages**: raw -> clean -> merge -> features -> split -> validate
- **File organization**: separate modules in `src/data/` and `src/features/`
- **Idempotency strategy**: delete and recreate output files on each run
- **Leakage prevention**: compute lag/rolling features *before* train/test split, using proper time boundaries
- **Validation checkpoints**: validate after each stage, not just at the end

### Step 2: Discuss and refine

While still in Plan mode, ask follow-up questions:

```
Good plan. Two questions:
1. Should we use DuckDB for the merge step instead of pandas? The data is ~3M rows.
2. How should we handle the 364-day lag? We need over a year of history.
```

Claude will reason through the trade-offs without writing code.

### Step 3: Exit Plan mode and implement

When you are satisfied with the plan, press `Shift+Tab` to exit Plan mode:

```
Implement the pipeline architecture we just discussed. Start with the main
orchestration script at src/data/pipeline.py that calls each stage in order.
```

Now Claude switches from thinking to doing -- it creates files, writes code, and builds what you planned together.

> **Tip:** Plan mode is especially valuable for business analysts who want to understand *what* will be built before it gets built. You can share the Plan mode conversation with stakeholders to get alignment before investing time in implementation.

---

## Exercise 6: Iterative Refactoring

Your pipeline works, but is it *good*? In this exercise, you will ask Claude to review its own work and improve it. This is a pattern you will use constantly in real projects.

### Step 1: Ask for a code review

```
Review the data preparation code we've built so far in src/data/ and
src/features/. Look for:

1. Performance issues (anything slow for 3M rows?)
2. Code duplication
3. Missing error handling
4. Places where documentation could be clearer
5. Any data leakage risks we might have missed

Be critical -- pretend you're reviewing a junior engineer's pull request.
```

### Step 2: Apply the improvements

Claude will identify issues and suggest fixes. Then tell it:

```
Apply all the improvements you suggested. For each change, add a comment
explaining what you changed and why.
```

### Step 3: Verify nothing broke

```
Run the full test suite to make sure the refactoring didn't break anything:
python -m pytest tests/ -v
```

> **Tip:** This three-step pattern -- **review, improve, test** -- is the fundamental loop of professional software development. With Claude Code, you can run through this loop in minutes instead of hours.

---

## Personalizing Your Data Preparation Workflow

The exercises above teach you the mechanics. Now let us make Claude Code work the way *your* team works.

### Encode Your Data Conventions in CLAUDE.md

Open `CLAUDE.md` in your project root and add your team's specific rules. Here are some examples:

```markdown
## Data Conventions

- Always use parquet for processed data (not CSV or pickle)
- Column names must be snake_case (no spaces, no camelCase)
- Date columns must be named 'date' and be datetime64[ns] dtype
- Categorical columns (store_nbr, family) must use pandas Categorical dtype
- Never store data files larger than 50MB in git
- All processed data goes in data/processed/ with descriptive filenames
- Feature names follow the pattern: {base}_{transform}_{window}_{stat}
  Example: sales_rolling_7d_mean, oil_price_lag_14d
```

Claude reads `CLAUDE.md` at the start of every session. By putting your conventions here, every future conversation -- and every subagent -- will follow them automatically.

### Customize the Data Validation Skill

The file `.claude/skills/data-validation/SKILL.md` contains validation rules specific to this dataset. You can extend it with your organization's data quality standards:

```markdown
### Organization-Specific Rules

- All monetary values must be in the same currency (USD)
- Date ranges must not extend beyond the known data collection period
- Any column with >30% missing values must be flagged for removal or imputation review
- PII columns (customer_id, email) must NEVER appear in processed data files
```

### Explore Community Skills

The Claude Code community shares skills for common data engineering patterns. You can find them at:

- **GitHub**: Search for "claude-code-skills data-engineering"
- **Great Expectations integration**: Skills that generate GE validation suites
- **dbt-style patterns**: Skills for SQL-based transformation conventions

To add a community skill, drop the `SKILL.md` file into `.claude/skills/<skill-name>/` and reference it in your agent frontmatter.

---

## What You Learned

In this chapter, you practiced six core workflows and learned five Claude Code features:

| Feature | What It Does | When to Use It |
|---------|-------------|----------------|
| **Subagents** | Specialized agents with focused instructions and skills | When a task needs domain expertise (data engineering, ML, QA) |
| **Hooks** | Automated scripts that fire before/after Claude uses tools | To enforce standards, validate outputs, catch issues automatically |
| **Plan mode** | Architecture discussions without writing code | Before complex builds, when exploring approaches, for stakeholder alignment |
| **Write/Edit tools** | Precise file creation and modification | Every time Claude creates or changes code (automatic) |
| **Bash tool** | Running commands in the terminal | Executing pipelines, running tests, installing packages |

**Key takeaways:**

1. **Describe what you want, not how to code it.** Claude handles the pandas syntax. You handle the data science thinking.
2. **Subagents beat generalists for specialized tasks.** The data-engineer agent produces better feature engineering than a generic prompt because it has focused instructions, relevant skills, and retail domain knowledge.
3. **Hooks are your automated safety net.** They enforce standards without you having to remember every rule.
4. **Plan before you build.** Five minutes in Plan mode can save an hour of rework.
5. **Test, review, improve.** The refactoring loop is fast with Claude Code -- use it liberally.

---

## Next Up

In **Chapter 4: Modeling**, you will use the `ml-engineer` subagent to build and compare forecasting models. You will also learn about **agent teams** for running parallel experiments, **Context7 MCP** for looking up library documentation in real time, and **worktrees** for isolating experiments in separate git branches.

Your clean, feature-rich dataset in `data/processed/train_features.parquet` is ready for modeling. Let us put it to work.
