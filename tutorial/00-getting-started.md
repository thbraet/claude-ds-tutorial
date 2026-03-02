# Chapter 0: Getting Started

Welcome to the Claude Code for Data Scientists tutorial. By the end of this chapter, you will have Claude Code installed, connected, and ready to work on a real data science project. No prior experience with command-line tools is required -- we will walk through everything together.

---

## What Is Claude Code?

Think of Claude Code as **a coding partner that lives in your terminal**. Instead of switching between a browser chatbot and your coding environment, Claude Code sits right next to your files, your data, and your Python scripts. You type a request in plain English, and Claude reads your files, writes code, runs analyses, and creates notebooks -- all while you watch.

For **business analysts**: You do not need to be a programmer. Claude Code lets you describe what you want in everyday language ("Show me sales trends by product family") and it does the coding for you. You will learn just enough terminal basics to get started.

For **junior data scientists**: You already know Python, but Claude Code will dramatically accelerate your workflow. It understands your project structure, remembers your conventions, and can scaffold entire analyses in seconds.

---

## Installation

### Prerequisites

You need two things installed on your computer:

1. **Node.js** (version 18 or later) -- this is the runtime that Claude Code runs on
2. **Python 3.11+** -- for the data science work in this tutorial

> **:bulb: Tip:** Not sure if you have Node.js? Open your terminal and type `node --version`. If you see a version number like `v20.11.0`, you are good. If not, download it from [nodejs.org](https://nodejs.org).

### Install Claude Code

Open your terminal and run:

```bash
npm install -g @anthropic-ai/claude-code
```

This installs Claude Code globally on your machine so you can run it from any folder.

> **:warning: Note:** On macOS, if you get a permissions error, try `sudo npm install -g @anthropic-ai/claude-code` and enter your computer password when prompted.

Verify the installation:

```bash
claude --version
```

You should see a version number printed. If you do, the installation was successful.

---

## Terminal Survival Guide

If you are a business analyst or someone who does not use the terminal daily, this section is for you. The terminal (also called the command line or shell) is a text-based way to interact with your computer. Here are the only commands you need to know:

| Command | What it does | Example |
|---------|-------------|---------|
| `pwd` | **P**rint **w**orking **d**irectory -- shows where you are | `pwd` |
| `ls` | **L**i**s**t the files in the current folder | `ls` |
| `cd` | **C**hange **d**irectory -- move to a different folder | `cd Documents` |
| `cd ..` | Go up one folder level | `cd ..` |
| `clear` | Clear the screen when it gets cluttered | `clear` |

A quick practice session:

```bash
# See where you are right now
pwd

# List what is in this folder
ls

# Move into a folder called Documents (if it exists)
cd Documents

# Go back up
cd ..
```

> **:bulb: Tip:** You can press the **Tab** key to autocomplete folder and file names. Start typing a folder name and press Tab -- the terminal will fill in the rest. This saves time and prevents typos.

---

## First Run and Authentication

### Get Your API Key

Claude Code requires an Anthropic API key. Here is how to get one:

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Navigate to **API Keys** in the left sidebar
4. Click **Create Key** and give it a name like "claude-code-tutorial"
5. Copy the key (it starts with `sk-ant-...`)

> **:warning: Note:** Keep your API key private. Never share it, paste it into a public website, or commit it to a git repository.

### Start Claude Code for the First Time

Open your terminal and simply type:

```bash
claude
```

The first time you run Claude Code, it will ask for your API key. Paste the key you just copied and press Enter. Claude Code stores this securely on your machine -- you will not need to enter it again.

You will see Claude Code's interactive prompt appear, ready for your instructions.

### Alternative: Set the Environment Variable

If you prefer, you can set your API key as an environment variable before running Claude Code:

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
claude
```

---

## Clone the Tutorial Repository

This tutorial comes with a pre-configured project repository that includes custom agents, skills, commands, hooks, and MCP server configurations. Let us get it set up.

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/claude-ds-tutorial.git
```

### Step 2: Move into the Project Folder

```bash
cd claude-ds-tutorial
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Launch Claude Code

```bash
claude
```

When Claude Code starts inside this project folder, it automatically reads the project's configuration files. You should see it acknowledge the project context.

### Step 5: Verify Everything Works

Once inside Claude Code, type:

```
What files are in this project? Give me a quick overview of the structure.
```

Claude should list the project's folders (`data/`, `src/`, `notebooks/`, `tutorial/`, `.claude/`) and describe what each one contains.

> **What just happened?** Claude Code detected the project's `CLAUDE.md` file and loaded the project context. It can now see your entire project structure, read your data files, and understand your conventions. We will explore `CLAUDE.md` in detail in the next chapter.

---

## Understanding the Interface

### The Prompt

When Claude Code is running, you see a prompt where you type natural language requests. There are no special programming commands to learn -- just describe what you want:

```
Summarize the columns in data/raw/train.csv

Create a bar chart showing sales by product family

Write a function that calculates rolling 7-day average sales
```

Claude reads your files, writes code, and executes it -- all from your plain-English descriptions.

### Slash Commands

Claude Code has built-in commands that start with a forward slash (`/`). Here are the most important ones:

| Command | What it does |
|---------|-------------|
| `/help` | Show all available commands and options |
| `/compact` | Summarize the conversation to free up context space |
| `/clear` | Start a fresh conversation |
| `/cost` | Show how much API usage the current session has consumed |

Try it now -- type `/help` inside Claude Code and read through the options.

### The Permission Model

Claude Code asks for your permission before performing potentially impactful actions. You will see prompts like:

```
Claude wants to run: python src/data/load.py
Allow? (y/n/always)
```

- Type **y** to allow this one time
- Type **n** to deny
- Type **always** to allow this type of action for the rest of the session

This tutorial's repository comes pre-configured with sensible permission rules (in `.claude/settings.json`) that automatically allow common data science operations like reading files, running Python, and executing pytest. Dangerous operations like deleting files or dropping database tables are automatically blocked.

> **:bulb: Tip:** The permission model is there to keep you safe. If Claude ever wants to do something you are not sure about, just say **n** and ask it to explain what it is trying to do.

---

## What Comes Pre-Configured

This tutorial repository is not a blank slate. It comes loaded with Claude Code features that make data science work smoother. You do not need to understand all of these right now -- each chapter will introduce the relevant features as you need them.

Here is a quick map of what is included:

| Feature | Location | Purpose |
|---------|----------|---------|
| **CLAUDE.md** | `CLAUDE.md` | Project "brain" -- tells Claude about your project goals, conventions, and structure |
| **Skills** | `.claude/skills/` | Domain knowledge that auto-activates (CRISP-DM guide, retail domain, data validation) |
| **Agents** | `.claude/agents/` | Specialized subagents (business analyst, data engineer, ML engineer, QA reviewer) |
| **Commands** | `.claude/commands/` | Custom slash commands (`/eda`, `/data-quality`, `/model-report`, `/feature-importance`) |
| **Hooks** | `.claude/hooks/` | Automatic checks that run before/after Claude takes actions (data validation, notebook linting) |
| **MCP Servers** | `.claude/settings.json` | External tool connections (DuckDB for SQL queries on your data) |

> **:mortar_board: Claude Code Feature:** This layered configuration system is what makes Claude Code powerful for data science. Instead of explaining your project from scratch every time, these files give Claude persistent context, domain expertise, and specialized tools.

---

## Explore With `/help`

Let us do one more thing before wrapping up this chapter.

### Exercise: Run `/help`

Inside Claude Code, type:

```
/help
```

**What just happened?** Claude shows you a list of all available commands, including the custom ones defined in this project. You should see the built-in commands (`/help`, `/compact`, `/clear`, `/cost`) alongside project-specific ones like `/eda` and `/data-quality`.

### Exercise: Try `/compact`

Have a conversation with Claude -- ask it a few questions about the project. Then type:

```
/compact
```

**What just happened?** Claude Code summarized your conversation into a shorter form. This is useful during long analysis sessions when the conversation gets very long. It frees up context window space so Claude can continue helping you effectively. Think of it as Claude taking notes and clearing its short-term memory while keeping the key facts.

---

## Key Concept: CLAUDE.md

Before we move on, let us talk about the single most important file in any Claude Code project: **`CLAUDE.md`**.

`CLAUDE.md` is like a briefing document you hand to a new team member on their first day. It tells Claude:

- What this project is about
- What technology you are using
- What coding conventions to follow
- How the project is organized
- What rules to always respect

When Claude Code starts in a folder that contains a `CLAUDE.md` file, it reads that file first, before doing anything else. This means every conversation starts with Claude already understanding your project.

You will explore the contents of this file in detail in Chapter 1 and even modify it with Claude's help.

> **:mortar_board: Claude Code Feature:** `CLAUDE.md` is the foundation of project-aware AI assistance. Without it, Claude is a general-purpose assistant. With it, Claude becomes a team member who knows your project inside and out.

---

## What You Learned

In this chapter, you accomplished the following:

- **Installed Claude Code** using `npm install -g @anthropic-ai/claude-code`
- **Authenticated** with your Anthropic API key
- **Learned terminal basics** -- `cd`, `ls`, `pwd` -- enough to navigate your project
- **Cloned the tutorial repository** and launched Claude Code inside it
- **Explored the interface** -- natural language prompts, slash commands, and the permission model
- **Discovered `/help` and `/compact`** -- two commands you will use in every session
- **Understood `CLAUDE.md`** -- the project briefing document that makes Claude project-aware
- **Saw the pre-configured features** -- skills, agents, commands, hooks, and MCP servers that this tutorial repository includes

---

## Next Up

In **Chapter 1: Business Understanding**, you will start your first real data science workflow. You will define the business problem with Claude's help, meet the `business-analyst` subagent, explore the `CLAUDE.md` file in depth, and create a project charter -- all without writing a single line of code yourself. This is where the CRISP-DM journey begins.
