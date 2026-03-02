# Chapter 2: Data Understanding

**CRISP-DM Phase 2 of 6**

In the previous chapter, you defined what the business needs. Now it is time to meet the data. Data Understanding is where the theoretical meets the practical -- you will discover what data you actually have, what condition it is in, and whether it can support the forecasting goals you set in Phase 1. Claude is going to do the heavy lifting, but you will learn to steer the exploration.

> **:mortar_board: Claude Code Feature:** This chapter introduces **MCP Servers** (connecting Claude to external tools like databases), **Custom Commands** (`/eda`, `/data-quality`), **Hooks** (automatic safety checks), and the **Task/Explore agent** (built-in agents for scanning files).

---

## The CRISP-DM Context

Phase 2 of CRISP-DM -- **Data Understanding** -- has four tasks:

1. **Collect initial data** -- Acquire the data and load it into your working environment
2. **Describe data** -- Document what each column means, its type, and its range
3. **Explore data** -- Find patterns, distributions, relationships, and anomalies
4. **Verify data quality** -- Identify missing values, outliers, inconsistencies, and potential problems

Rushing through this phase is the number one cause of failed data science projects. A model trained on misunderstood data will produce misunderstood results. We are going to be thorough.

---

## Exercise 1: Connect to Data via MCP

Before we can explore data, Claude needs a way to query it. This project uses **DuckDB** -- a fast, SQL-friendly database engine that can query CSV files directly. Claude connects to DuckDB through something called an **MCP server**.

### What Is MCP?

**MCP** stands for **Model Context Protocol**. It is an open standard that lets Claude Code connect to external tools, databases, and APIs. Think of MCP as a universal adapter: just as a USB-C cable lets you connect different devices to your laptop, MCP lets Claude connect to different data sources and services.

Without MCP, Claude can only read files directly. With MCP, Claude can:

- Run SQL queries against databases
- Access APIs and web services
- Connect to specialized tools (Jupyter, Hugging Face, and more)

### How MCP Is Configured in This Project

The MCP configuration lives in `.claude/settings.json`. Let us look at it.

### Step 1: Ask Claude to Show the MCP Configuration

```
Show me the MCP server configuration in .claude/settings.json and explain
what each part does.
```

Claude will show you the relevant section:

```json
{
  "mcpServers": {
    "duckdb": {
      "command": "npx",
      "args": ["-y", "@motherduck/mcp-server-duckdb"],
      "env": {
        "DUCKDB_PATH": "./data/analytics.duckdb"
      }
    }
  }
}
```

Here is what each part means:

| Field | Purpose |
|-------|---------|
| `"duckdb"` | The name of this MCP server (you choose the name) |
| `"command"` | How to launch the server (`npx` runs a Node.js package) |
| `"args"` | Arguments passed to the command (the DuckDB MCP server package) |
| `"env"` | Environment variables -- here, the path to the DuckDB database file |

When Claude Code starts, it automatically launches this MCP server and discovers the tools it provides (like running SQL queries). You do not need to start it manually.

### Step 2: Query Your Data with SQL

Now let us use DuckDB to explore the sales data. Type:

```
Using DuckDB, run a SQL query to show the first 10 rows of the training data
CSV file at data/raw/train.csv. Also show me the column names and types.
```

You should see output showing columns like `id`, `date`, `store_nbr`, `family`, `sales`, and `onpromotion`, along with sample rows.

### Step 3: Run a Summary Query

```
Using DuckDB, run a SQL query to show: the total number of rows, the date
range (min and max date), the number of unique stores, and the number of
unique product families in data/raw/train.csv.
```

### What Just Happened?

Claude sent SQL queries to the DuckDB MCP server, which read your CSV files and returned results -- all without loading the entire dataset into Python. This is especially powerful for large datasets: DuckDB can query gigabytes of CSV data efficiently.

> **:mortar_board: Claude Code Feature: MCP Servers**
>
> MCP servers extend what Claude can do. They are configured once in `.claude/settings.json` and then Claude auto-discovers the tools each server provides.
>
> Key points about MCP:
> - **Auto-discovery**: Claude automatically learns what tools an MCP server offers (SQL queries, file operations, etc.)
> - **Transparent to you**: You do not need to learn the MCP protocol. Just ask Claude what you want, and it figures out which tool to use.
> - **Composable**: You can run multiple MCP servers simultaneously -- one for DuckDB, one for Jupyter, one for an internal API.
> - **Open standard**: MCP is not proprietary to Anthropic. Many community-built servers exist for different data sources.
>
> Other MCP servers useful for data science:
>
> | MCP Server | Purpose |
> |-----------|---------|
> | **DuckDB** (configured in this project) | SQL queries on CSV/Parquet files |
> | **Jupyter MCP** (by Datalayer) | Execute notebook cells programmatically |
> | **mcp-pandas** | DataFrame operations through MCP |
> | **PostgreSQL MCP** | Connect to PostgreSQL databases |
> | **Hugging Face MCP** | Access models, datasets, and Spaces |

---

## Exercise 2: Run the `/eda` Command

This project includes a custom slash command called `/eda` that runs a comprehensive exploratory data analysis. Instead of asking Claude step by step, you can trigger the entire workflow with a single command.

### Step 1: Run the Command

Type the following into Claude Code:

```
/eda data/raw/train.csv
```

### Step 2: Watch the Output

Claude will execute a multi-step analysis:

1. Load the data and report its shape
2. List every column with its data type and sample values
3. Calculate missing value counts and percentages
4. Compute descriptive statistics (mean, median, standard deviation, quartiles)
5. Analyze distributions of numeric columns
6. Generate a correlation matrix
7. Look for time-based patterns (trends, seasonality, day-of-week effects)
8. Flag potential outliers
9. Summarize the five most important findings

This may take a minute or two. Claude is generating code, running it, reading the output, and producing visualizations.

### Step 3: Review the Findings

When Claude finishes, read through the key findings carefully. For the store sales dataset, you will likely discover things like:

- Sales have strong day-of-week patterns (weekends are different from weekdays)
- Some product families (GROCERY I, BEVERAGES) dominate total sales volume
- There are zero-sales entries that need investigation (are they true zeros or missing data?)
- Promotion status varies significantly across product families
- There are seasonal patterns around holidays

### What Just Happened?

You triggered a pre-built analysis workflow with a single command. Let us look at how it works.

> **:mortar_board: Claude Code Feature: Custom Commands**
>
> Custom commands are markdown files in `.claude/commands/`. When you type `/eda`, Claude reads the file `.claude/commands/eda.md` and follows its instructions.
>
> Ask Claude to show you the command file:
>
> ```
> Show me .claude/commands/eda.md and explain how it works.
> ```
>
> You will see that the file contains:
> - A description of what the command does
> - The `$ARGUMENTS` placeholder -- this is replaced with whatever you type after the command (in this case, `data/raw/train.csv`)
> - Step-by-step instructions that Claude follows
> - Output format specifications
>
> The `$ARGUMENTS` syntax is simple: in the command file, `$ARGUMENTS` is a placeholder. When you type `/eda data/raw/train.csv`, Claude replaces `$ARGUMENTS` with `data/raw/train.csv` and follows the instructions.
>
> This project includes four custom commands:
>
> | Command | File | Purpose |
> |---------|------|---------|
> | `/eda` | `.claude/commands/eda.md` | Full exploratory data analysis |
> | `/data-quality` | `.claude/commands/data-quality.md` | Data quality assessment |
> | `/model-report` | `.claude/commands/model-report.md` | Model evaluation report (used in later chapters) |
> | `/feature-importance` | `.claude/commands/feature-importance.md` | Feature importance analysis (used in later chapters) |
>
> You can create your own commands for any workflow you repeat often. Just add a markdown file to `.claude/commands/`.

---

## Exercise 3: Run the `/data-quality` Command

Data quality is so important it gets its own dedicated command. Let us run a thorough quality assessment.

### Step 1: Run the Command

```
/data-quality data/raw/train.csv
```

### Step 2: Understand the Assessment

The data quality command checks five dimensions:

1. **Completeness** -- How many values are missing? Which columns are affected?
2. **Uniqueness** -- Are there duplicate rows? Is the expected primary key actually unique?
3. **Validity** -- Are values within expected ranges? Are dates valid? Are categories spelled consistently?
4. **Consistency** -- Do cross-column relationships make sense? (e.g., sales should be non-negative)
5. **Timeliness** -- What is the date range? Are there gaps in the time series?

Each finding gets a severity rating:

- **CRITICAL** -- Must fix before any modeling (e.g., data leakage, wrong data types, massive missing data)
- **WARNING** -- Should investigate before modeling (e.g., moderate missing data, suspicious outliers)
- **INFO** -- Worth noting but not blocking (e.g., minor patterns, optimization opportunities)

### Step 3: Check Additional Data Files

The training data is not the only file. Let us check the supplementary files too:

```
/data-quality data/raw/oil.csv
```

```
/data-quality data/raw/holidays_events.csv
```

```
/data-quality data/raw/stores.csv
```

### What Just Happened?

You now have a data quality baseline across all your data sources. The quality report tells you exactly what needs fixing before you can build reliable forecasting models. Common issues you might find:

- Oil prices have missing values on weekends and holidays (expected and needs interpolation)
- Some holidays are "transferred" (moved to a different date) which affects modeling
- Store metadata should be joined carefully using `store_nbr` as the key

> **:bulb: Tip:** The data quality command automatically uses the `data-validation` skill, which contains validation rules specific to this dataset. The skill knows that sales should be non-negative, that dates should range from 2013 to 2017, and that there are exactly 54 stores and 33 product families. This domain-specific validation catches issues that a generic quality check would miss.

---

## Exercise 4: Generate a Full EDA Notebook

Reports in the terminal are useful, but for a data science project you want a proper Jupyter notebook that you can share with colleagues, annotate, and come back to later.

### Step 1: Ask Claude to Create the Notebook

```
Create a Jupyter notebook at notebooks/01-eda.ipynb that performs a complete
exploratory data analysis of our sales dataset. Include:
- Data loading and initial inspection
- Missing value analysis with visualizations
- Sales distributions by product family (bar chart)
- Time series plots showing sales trends over time
- Day-of-week and month-of-year patterns
- Correlation analysis between sales, promotions, and oil prices
- Store-level analysis (which stores sell the most?)
- Key findings summary in markdown cells

Use matplotlib and seaborn for all plots. Make it presentation-ready with
clear titles, labels, and explanations in markdown cells between code cells.
```

### Step 2: Review the Notebook

Claude will create a complete `.ipynb` file with alternating markdown and code cells. To view and run it:

```bash
jupyter lab notebooks/01-eda.ipynb
```

Or ask Claude:

```
Run all the code cells in notebooks/01-eda.ipynb and tell me if there are
any errors.
```

### What Just Happened?

Claude created a structured, documented Jupyter notebook from scratch. Each section has markdown cells explaining what the analysis shows and why it matters. This notebook serves as both an analysis artifact and a communication tool -- you can share it with stakeholders who want to see the data behind the forecasting project.

> **:warning: Note:** When Claude creates or modifies notebook files, a **hook** automatically runs to validate the notebook. This hook (defined in `.claude/hooks/lint-notebook.sh`) checks that the JSON structure is valid, warns about wildcard imports, and flags any cells that might contain sensitive data. You will learn more about hooks shortly.

---

## Exercise 5: Have Claude Explain the Data

Sometimes the most valuable analysis is a plain-English explanation. Let us ask Claude to be our data interpreter.

### Step 1: Ask for a Data Dictionary

```
Read the training data at data/raw/train.csv and the supplementary files
(oil.csv, holidays_events.csv, stores.csv, transactions.csv). Create a
comprehensive data dictionary that explains:
- What each column means in business terms
- The data type and example values
- Key patterns you've noticed
- How the tables relate to each other

Write it for a business audience who doesn't know what a "feature" or
"dataframe" is.
```

### Step 2: Ask About Key Patterns

```
Based on your analysis of the data, what are the top 5 patterns that will
be most important for building an accurate sales forecast? Explain each one
in business terms and technical terms.
```

### Step 3: Ask About Challenges

```
What are the biggest data challenges we'll face when building this forecast?
Think about things like missing data, seasonal effects, the impact of
holidays, oil price fluctuations, and any other issues you spotted.
```

### What Just Happened?

Claude synthesized its understanding of the data across multiple files and produced business-ready explanations. This is one of Claude's greatest strengths for data science: it can read the raw data, compute statistics, and then translate everything into language that a store manager or supply chain director can understand.

---

## Exercise 6: Use the Explore Agent

Claude Code has a built-in capability for quickly scanning multiple files and directories. This is useful when you want a rapid overview without running a full analysis.

### Step 1: Ask Claude to Explore the Data Directory

```
Explore the data/raw/ directory. For each file, tell me: the filename, file
size, number of rows and columns, and a one-sentence description of what it
contains.
```

### Step 2: Understand What Happened

Claude used its **Task tool** to efficiently scan multiple files in parallel. The Task tool is Claude's built-in mechanism for dispatching sub-tasks -- similar to subagents, but lighter weight and built into Claude's core capabilities.

> **:mortar_board: Claude Code Feature: Task Tool and Explore Agent**
>
> Claude Code has two types of agents:
>
> **Built-in agents** (like Explore and Task):
> - Part of Claude Code itself -- no configuration needed
> - Task lets Claude dispatch sub-work in parallel for efficiency
> - Explore lets Claude quickly scan files, directories, and codebases
> - Automatically available in every project
>
> **Custom agents** (like `business-analyst`):
> - Defined by you in `.claude/agents/`
> - Have their own system prompts, tools, and skills
> - Specialized for your project's domain
>
> The Task tool is especially useful for data understanding because it can read and summarize multiple files simultaneously, giving you a birds-eye view of your entire dataset.

---

## How Hooks Protected You

Throughout this chapter, Claude read data files, ran Python scripts, and modified notebooks. Behind the scenes, **hooks** were running to keep things safe.

> **:mortar_board: Claude Code Feature: Hooks**
>
> Hooks are scripts that run automatically before or after Claude takes specific actions. They act like safety guardrails.
>
> This project has two hooks:
>
> ### Hook 1: `validate-data-load.sh` (PreToolUse)
>
> This hook runs **before** Claude reads any data file. It checks:
> - **File size**: If a file is over 100MB, it warns Claude to use DuckDB or pandas instead of loading the entire file
> - **Sensitive files**: It blocks access to `.env`, `credentials`, `secret`, and `password` files
>
> Ask Claude to show you the hook:
> ```
> Show me .claude/hooks/validate-data-load.sh and explain what it does.
> ```
>
> ### Hook 2: `lint-notebook.sh` (PostToolUse)
>
> This hook runs **after** Claude writes or edits a notebook file. It checks:
> - **Valid JSON**: Notebooks are JSON files -- a malformed notebook will not open in Jupyter
> - **No wildcard imports**: `from module import *` is a bad practice
> - **No secrets in code**: Warns if a cell contains words like "password" or "secret"
>
> ### Hook Lifecycle Events
>
> Hooks attach to lifecycle events:
>
> | Event | When It Fires | Use Case |
> |-------|--------------|----------|
> | `PreToolUse` | Before Claude executes a tool (Read, Write, Bash, etc.) | Validate inputs, block dangerous operations, warn about large files |
> | `PostToolUse` | After Claude executes a tool | Lint output, validate results, log actions |
>
> The configuration in `.claude/settings.json` maps hooks to specific tools:
>
> ```json
> {
>   "hooks": {
>     "PreToolUse": [
>       {
>         "matcher": "Read",
>         "hooks": [
>           {
>             "type": "command",
>             "command": "bash .claude/hooks/validate-data-load.sh"
>           }
>         ]
>       }
>     ]
>   }
> }
> ```
>
> The `matcher` field specifies which tool triggers the hook. The `command` field is the script to run. You can add your own hooks for any validation or logging you need.

---

## How the Data Validation Skill Helped

In Exercises 2 and 3, you may have noticed that Claude's data quality checks were unusually specific -- it knew the exact valid ranges for store numbers (1-54), the expected date range (2013-2017), and the 33 product families. That knowledge came from the `data-validation` skill.

> **:mortar_board: Claude Code Feature: Skills (Data Validation)**
>
> The `data-validation` skill (`.claude/skills/data-validation/SKILL.md`) auto-activated whenever Claude was loading or examining data files. It provided:
>
> - **Automatic checks on data load**: Shape, missing values, duplicates, data types, value ranges
> - **Project-specific validation rules**: The exact valid ranges for each column in this dataset
> - **A structured report template**: Consistent format for data quality reports
> - **Validation on data write**: Checks when saving processed data (row counts, parquet format, snake_case columns)
>
> This is the third skill you have seen in action:
>
> | Skill | Activates When | Provides |
> |-------|---------------|----------|
> | `crisp-dm-guide` | Discussing project phases | Phase-specific guidance and deliverables |
> | `retail-domain` | Working with retail/grocery data | KPIs, seasonal patterns, product taxonomy |
> | `data-validation` | Loading or checking data files | Validation rules, quality checks, report templates |
>
> All three activated automatically based on your conversation context. You never had to turn them on.

---

## Personalization: Connect Your Own Data

### Add Your Own Database

If your data lives in a database rather than CSV files, you can add an MCP server for it. Here are some common options:

**PostgreSQL:**
Add this to the `mcpServers` section in `.claude/settings.json`:

```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres"],
    "env": {
      "POSTGRESQL_URL": "postgresql://user:password@localhost:5432/mydb"
    }
  }
}
```

**MySQL, BigQuery, Snowflake:** Community MCP servers exist for each. Search for them at [mcpguide.dev](https://mcpguide.dev) -- a directory of available MCP servers organized by category.

### Add MCP Servers from the CLI

You can also add MCP servers without editing JSON files. Use the `claude mcp add` command:

```bash
# Add a DuckDB MCP server
claude mcp add duckdb -- npx -y @motherduck/mcp-server-duckdb

# Add a PostgreSQL MCP server
claude mcp add postgres -- npx -y @modelcontextprotocol/server-postgres
```

This command updates `.claude/settings.json` for you. Run `claude mcp list` to see all configured servers.

### Discover MCP Servers

The MCP ecosystem is growing rapidly. To find servers for your specific data stack:

1. Visit **[mcpguide.dev](https://mcpguide.dev)** -- a curated directory of MCP servers
2. Search by category (databases, APIs, developer tools, data science)
3. Each listing includes installation instructions and configuration examples

### Write a Custom MCP Server

For internal data APIs that do not have a public MCP server, you can write your own. A minimal MCP server is a small program that:

1. Accepts requests over standard input/output (stdin/stdout)
2. Describes its available tools (e.g., "query_sales_api", "get_inventory_levels")
3. Executes tool calls and returns results

Ask Claude for help:

```
Help me write a simple MCP server in Python that connects to our internal
REST API at https://api.internal.company.com/v1/ and exposes endpoints for
querying sales data and inventory levels.
```

Claude can scaffold the entire MCP server for you, including the protocol handling, tool definitions, and API integration.

### Customize Data Validation Rules

If you are working with your own dataset (not the tutorial data), update the validation rules in `.claude/skills/data-validation/SKILL.md`:

1. Replace the column-specific rules with your schema expectations
2. Add business rules (e.g., "revenue must equal quantity times unit_price")
3. Add cross-table consistency checks if you have multiple related tables
4. Include data freshness checks ("latest date should be within 24 hours of today")

### Write Your Own Custom Commands

If you have analysis workflows you repeat often, create custom commands for them:

```bash
# Create a new command file
touch .claude/commands/my-analysis.md
```

Then ask Claude to help you write the command:

```
Create a custom command at .claude/commands/weekly-report.md that generates
a weekly sales summary. It should accept a date range as $ARGUMENTS, query
the sales data, and produce a formatted markdown report with top-selling
categories, year-over-year comparison, and any anomalies.
```

---

## What You Learned

In this chapter, you accomplished the following:

- **Connected to data via MCP** -- configured DuckDB to query CSV files with SQL, and understood how MCP extends Claude's capabilities
- **Ran `/eda`** -- used a custom slash command to perform comprehensive exploratory data analysis in one step
- **Ran `/data-quality`** -- assessed data quality across five dimensions (completeness, uniqueness, validity, consistency, timeliness)
- **Generated an EDA notebook** -- had Claude create a complete, presentation-ready Jupyter notebook
- **Got plain-English data explanations** -- used Claude as a data interpreter for business-audience communication
- **Used the Explore agent** -- quickly scanned multiple data files with Claude's built-in Task tool
- **Understood MCP Servers** -- what they are, how they are configured, and how Claude auto-discovers their tools
- **Understood Custom Commands** -- how `/eda` and `/data-quality` work under the hood, and how to create your own
- **Understood Hooks** -- how `validate-data-load.sh` and `lint-notebook.sh` provide automatic safety checks
- **Understood the Data Validation skill** -- how it auto-activates to enforce dataset-specific quality rules
- **Learned personalization** -- how to connect your own databases, discover MCP servers, and write custom commands

### CRISP-DM Deliverables Completed

At the end of Phase 2, you should have:

- [x] Data dictionary describing every variable
- [x] Data quality report (missing values, outliers, duplicates, type mismatches)
- [x] Initial statistical summary (distributions, correlations, key patterns)
- [x] Visualization of key relationships (in the EDA notebook)

---

## Next Up

In **Chapter 3: Data Preparation**, you will clean the issues you just discovered, engineer features for the forecasting model, and build a reproducible data pipeline. You will meet the `data-engineer` subagent, learn how Claude handles complex multi-step transformations, and prepare your data for modeling. The real hands-on coding begins.
