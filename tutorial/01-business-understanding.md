# Chapter 1: Business Understanding

**CRISP-DM Phase 1 of 6**

Every successful data science project starts not with data, but with a clear understanding of the business problem. In this chapter, you will work with Claude to define what we are trying to achieve, why it matters, and how we will measure success. Along the way, you will learn some of the most powerful features of Claude Code: the `CLAUDE.md` project file, subagents, and skills.

> **:mortar_board: Claude Code Feature:** This chapter introduces **CLAUDE.md** (project memory), **Subagents** (specialized AI team members), and **Skills** (auto-activating domain knowledge).

---

## The CRISP-DM Context

The Cross-Industry Standard Process for Data Mining (CRISP-DM) is a battle-tested framework used by data teams worldwide. Its first phase -- **Business Understanding** -- asks us to:

1. **Define business objectives** -- What does the organization actually need?
2. **Assess the situation** -- What resources, constraints, and risks exist?
3. **Determine data mining goals** -- How do we translate business needs into a technical problem?
4. **Produce a project plan** -- What are the phases, milestones, and deliverables?

Too many data science projects skip this phase and jump straight to modeling. The result? Technically impressive models that nobody uses because they solved the wrong problem. We are going to do it right.

---

## The Tutorial Scenario

Here is your situation:

> **You are an insights translator at Favorita, a large grocery retail chain in Ecuador.** Management has noticed two costly problems: warehouses carry too much stock of slow-moving products (overstock waste), and popular items are frequently unavailable on shelves (out-of-stock incidents). They want to improve inventory planning by **forecasting daily store sales per product family**.
>
> The success criteria are concrete:
> - **Reduce overstock waste by 15%** (measured as unsold perishable inventory)
> - **Reduce out-of-stock incidents by 20%** (measured as empty-shelf scans)
>
> You have access to several years of historical sales data across 54 stores and 33 product families, along with supplementary data on oil prices, holidays, and store metadata.

Your job is to translate this business need into a well-defined data science project. Claude is going to help.

---

## Exercise 1: Define the Business Problem

Let us start a conversation with Claude to formalize the business problem. Make sure you are in the `claude-ds-tutorial` directory and Claude Code is running.

### Step 1: Start Claude Code

If Claude Code is not already running:

```bash
cd claude-ds-tutorial
claude
```

### Step 2: Describe the Problem

Type the following into Claude Code:

```
I'm an insights translator at a grocery retail chain. Management wants to reduce
overstock waste by 15% and out-of-stock incidents by 20% through better inventory
planning. We have historical sales data across 54 stores and 33 product families.
Help me formally define this as a data science problem. What are the business
objectives, data mining goals, and success criteria?
```

### What Just Happened?

Claude responded with a structured breakdown of the business problem, likely covering:

- **Business objectives** framed in terms of cost savings and customer satisfaction
- **Data mining goals** translated into a forecasting task (predict daily sales per store per product family)
- **Success metrics** -- both technical (forecast accuracy: RMSE, MAPE) and business (waste reduction percentage, stock availability rate)

> **:bulb: Tip:** Notice how Claude did not immediately suggest a model or algorithm. It started with the business context. That is the CRISP-DM discipline at work -- and it happened automatically because this project has a **skill** that guides Claude through CRISP-DM phases. More on that shortly.

---

## Exercise 2: Meet the Business Analyst Subagent

Claude Code can dispatch work to **subagents** -- specialized AI assistants with domain-specific knowledge, instructions, and tools. This project includes a `business-analyst` subagent designed for exactly this phase.

### Step 1: Invoke the Subagent

Type the following into Claude Code:

```
Use the business-analyst agent to help define our project charter. The business
problem is: Favorita grocery chain wants to forecast daily sales per product
family per store to reduce overstock waste by 15% and out-of-stock incidents
by 20%. We have historical sales data from 2013-2017 across 54 stores and
33 product families.
```

### Step 2: Review the Output

The business analyst subagent will produce a structured document that typically includes:

- An executive summary written for non-technical stakeholders
- Business context explaining why this problem matters (dollars lost to waste, revenue lost to stockouts)
- Measurable objectives with clear thresholds
- Scope and constraints (data availability, timeline, team capacity)
- Stakeholder identification

### What Just Happened?

Claude dispatched your request to the `business-analyst` subagent. This subagent has its own persona, its own set of skills (CRISP-DM guide + retail domain knowledge), and instructions that focus it on business-audience communication.

> **:mortar_board: Claude Code Feature: Subagents**
>
> Subagents are defined as markdown files in `.claude/agents/`. Each file specifies:
>
> - **name**: How you refer to the agent
> - **description**: What it is good at (Claude uses this to match your request to the right agent)
> - **tools**: Which Claude Code tools the agent can use
> - **model**: Which Claude model to use (e.g., `sonnet` for faster responses)
> - **maxTurns**: How many back-and-forth steps the agent can take
> - **skills**: Which skill files the agent has access to
>
> Below the frontmatter is the agent's system prompt -- its personality, expertise, and instructions.
>
> Let us look at the actual file. Ask Claude:
>
> ```
> Show me the contents of .claude/agents/business-analyst.md
> ```
>
> You will see the frontmatter at the top (between `---` markers) followed by detailed instructions about the agent's role, communication style, and output format. This project includes four subagents:
>
> | Agent | File | Specialty |
> |-------|------|-----------|
> | `business-analyst` | `.claude/agents/business-analyst.md` | Business problem definition, stakeholder communication, project scoping |
> | `data-engineer` | `.claude/agents/data-engineer.md` | Data cleaning, feature engineering, pipeline building |
> | `ml-engineer` | `.claude/agents/ml-engineer.md` | Model selection, training, hyperparameter tuning |
> | `qa-reviewer` | `.claude/agents/qa-reviewer.md` | Code review, testing, quality assurance |
>
> Why use a subagent instead of asking Claude directly? Subagents carry **dedicated context** -- their system prompt is tuned for a specific role, and they load only the skills relevant to that role. The business analyst knows retail KPIs and CRISP-DM but does not carry the weight of ML engineering knowledge. This focus produces better, more consistent results.

---

## Exercise 3: Explore the CLAUDE.md File

The `CLAUDE.md` file is the most important configuration in any Claude Code project. Let us examine the one that came with this repository.

### Step 1: Ask Claude to Show It

```
Show me the CLAUDE.md file and explain each section. What does it tell you
about this project?
```

### Step 2: Understand Each Section

Claude will walk you through the file. Here is what each section does:

| Section | Purpose |
|---------|---------|
| **Project Overview** | One-paragraph summary so Claude immediately knows what this project is |
| **Business goal** | The specific outcome we are working toward -- Claude factors this into every suggestion |
| **Dataset** | Where the data comes from -- helps Claude understand the domain |
| **Tech Stack** | Which libraries and tools to use -- Claude will write code using these, not random alternatives |
| **Conventions** | Coding rules (snake_case, parquet format, docstrings) -- Claude follows these automatically |
| **Project Structure** | Folder layout -- Claude knows where to put files and where to find things |
| **How to Run** | Execution instructions -- Claude can run tests and start notebooks |
| **CRISP-DM Phase Tracking** | Phase definitions -- Claude identifies which phase your current work belongs to |

### Step 3: Discuss Improvements

Now ask Claude:

```
Based on what we've discussed about our business problem, what should we add
or change in CLAUDE.md to make it more specific to our forecasting project?
```

Claude might suggest adding:

- Specific success metric thresholds (RMSLE < 0.5, MAPE < 15%)
- Key stakeholders and their roles
- Data update frequency and freshness requirements
- Known risks (oil price volatility, earthquake impacts in the historical data)
- Sprint timeline aligned with CRISP-DM phases

### Step 4: Update CLAUDE.md Together

If you agree with Claude's suggestions:

```
Go ahead and update CLAUDE.md with those improvements. Keep the existing
structure but add the new details we discussed.
```

### What Just Happened?

You and Claude collaboratively refined the project's "brain." Every future conversation in this project -- whether with you, a subagent, or a team member -- will benefit from this improved context. The `CLAUDE.md` file is a living document. You should update it as the project evolves: when you discover data quirks, when business requirements change, or when you settle on a modeling approach.

> **:mortar_board: Claude Code Feature: CLAUDE.md**
>
> Key facts about `CLAUDE.md`:
>
> - Claude reads it **automatically** when starting in a project directory
> - It supports **any content** -- project goals, coding conventions, team norms, data dictionaries, whatever helps Claude understand your project
> - It is **version controlled** -- commit it to git so the whole team shares the same Claude context
> - You can update it at any time, and Claude incorporates the changes immediately
> - Think of it as **institutional knowledge** -- the things a new team member would need to know on day one

---

## Exercise 4: Generate a Project Charter

A project charter is the foundational document for any data science initiative. Let us have Claude create one.

### Step 1: Request the Charter

```
Create a project charter document for our sales forecasting project. Save it as
docs/project-charter.md. Include:
- Executive summary
- Business context and problem statement
- Objectives with measurable success criteria
- Scope (what's in and what's out)
- Data sources available
- Timeline with CRISP-DM phases
- Risks and mitigation strategies
- Team roles and responsibilities
```

### Step 2: Review the Output

Claude will create a structured markdown document. Read through it carefully. A good project charter should:

- Be understandable by a non-technical executive in under 5 minutes
- Have concrete numbers for every success criterion (not vague phrases like "improve accuracy")
- Clearly state what is out of scope (to prevent scope creep later)
- Identify risks early (data quality issues, seasonal patterns, external shocks)

### Step 3: Refine It

If anything is missing or could be improved:

```
The timeline section needs more detail. Add specific milestones for each
CRISP-DM phase with estimated durations. Also add a section on data privacy
considerations.
```

### What Just Happened?

You created a professional project charter without writing a word yourself. Claude structured it using CRISP-DM best practices (guided by the `crisp-dm-guide` skill) and retail-specific context (guided by the `retail-domain` skill). This document can be shared with stakeholders to align everyone on what the project will and will not do.

---

## Exercise 5: Stakeholder Analysis

The final exercise in the Business Understanding phase is identifying who cares about this project and what they need from it.

### Step 1: Request a Stakeholder Analysis

```
Create a stakeholder analysis for our sales forecasting project. For each
stakeholder, identify:
- Their role and department
- What they need from this project
- How they will use the forecasts
- Their influence level (high/medium/low)
- Their interest level (high/medium/low)
- How we should communicate with them

Think about a typical grocery retail chain: store managers, category managers,
supply chain team, finance, IT, and executive leadership.
```

### Step 2: Review the Stakeholder Map

Claude will produce a comprehensive stakeholder analysis. You might see stakeholders like:

- **Supply Chain Director** (high influence, high interest) -- primary user of forecasts for ordering decisions
- **Store Managers** (low influence, high interest) -- use forecasts to plan shelf stocking
- **Category Managers** (medium influence, high interest) -- use forecasts for promotion planning
- **CFO** (high influence, medium interest) -- cares about the ROI of the project
- **IT Team** (medium influence, low interest) -- needs to support the deployment infrastructure

### Step 3: Save It

```
Save this stakeholder analysis as docs/stakeholder-analysis.md
```

### What Just Happened?

You now have a stakeholder map that tells you who to keep informed, who to involve in decisions, and who needs to sign off on the final results. This is critical for a project that will change how inventory decisions are made across dozens of stores.

---

## How Skills Powered This Chapter

You may have noticed that Claude's responses throughout this chapter were unusually well-structured for a retail forecasting project. That is because two **skills** were active behind the scenes.

> **:mortar_board: Claude Code Feature: Skills**
>
> Skills are markdown files in `.claude/skills/` that provide domain knowledge to Claude. They **auto-activate** based on what you are discussing -- you do not need to turn them on manually.
>
> Each skill file has a frontmatter block:
>
> ```yaml
> ---
> name: crisp-dm-guide
> description: "CRISP-DM methodology guide for data science projects. Activates
>   when discussing project phases, planning analysis workflows, or when the user
>   mentions business understanding, data understanding, data preparation,
>   modeling, evaluation, or deployment in a data science context."
> ---
> ```
>
> The `description` field is the trigger. When your conversation matches the description, Claude loads that skill's instructions. In this chapter, two skills activated:
>
> ### Skill 1: `crisp-dm-guide/SKILL.md`
>
> This skill told Claude to:
> - Detect which CRISP-DM phase applies to your request
> - Ensure the right deliverables are addressed for that phase
> - Remind you about cross-phase dependencies
>
> Ask Claude to show you the file:
> ```
> Show me .claude/skills/crisp-dm-guide/SKILL.md
> ```
>
> ### Skill 2: `retail-domain/SKILL.md`
>
> This skill provided Claude with:
> - Standard retail KPIs (stock turnover, GMROI, out-of-stock rate, etc.)
> - Grocery-specific data patterns (seasonality, promotion effects, perishability)
> - Product family taxonomy for the tutorial dataset
> - Forecasting best practices for retail
>
> Ask Claude to show you this file too:
> ```
> Show me .claude/skills/retail-domain/SKILL.md
> ```
>
> **Why skills matter**: Without the retail domain skill, Claude would give you generic data science advice. With it, Claude knows that grocery sales have weekly cycles, that perishable products need different forecasting approaches, and that oil prices matter for Ecuadorian retail. This domain context makes every response more relevant and actionable.

---

## Personalization: Make It Your Own

The skills and agents in this tutorial are configured for a grocery retail forecasting project. But they are just templates. Here is how to adapt them for your own work.

### Customize the Retail Domain Skill

Open `.claude/skills/retail-domain/SKILL.md` and modify it for your organization:

1. **Replace the KPIs** with your company's specific metric definitions and targets
2. **Update the product hierarchy** to match your category naming conventions
3. **Add your seasonal calendar** -- which holidays matter, when your fiscal year starts, promotion cycles
4. **Include store-specific attributes** -- your store formats (express, supermarket, hypermarket), location tiers, demographic profiles

For example, if you work in fashion retail instead of grocery, you might replace the perishability section with sell-through rates and markdown cadence.

### Explore Community Skills

The Claude Code community has built hundreds of skills for different domains. Two collections worth exploring:

- **[K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills)** -- Skills for scientific research, statistical analysis, and academic writing. Useful if your data science work leans toward research.

- **[VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)** -- A curated list of 380+ community-built skills covering everything from DevOps to data engineering to financial analysis.

### How to Browse and Install Community Skills

To browse available skills:

```
Show me the README from https://github.com/VoltAgent/awesome-agent-skills
```

To install a community skill, you typically clone it into your `.claude/skills/` directory:

```bash
# Example: installing a statistical analysis skill
cd .claude/skills/
git clone https://github.com/example-org/statistics-skill.git statistics
```

Or, you can simply create a new skill by adding a folder with a `SKILL.md` file:

```bash
mkdir -p .claude/skills/my-company-domain
```

Then ask Claude to help you write the `SKILL.md` file:

```
Create a new skill file at .claude/skills/my-company-domain/SKILL.md for
[describe your domain]. Include our key KPIs, common data patterns, and
domain-specific vocabulary.
```

> **:bulb: Tip:** Skills are just markdown files. You do not need to code anything. If you can describe your domain in plain English, you can create a skill. Think of it as writing a briefing document for a consultant who is about to join your team.

---

## What You Learned

In this chapter, you accomplished the following:

- **Defined the business problem** formally with Claude, distinguishing between business objectives and data mining goals
- **Used the `business-analyst` subagent** to get structured, business-audience-ready output
- **Explored CLAUDE.md** -- understood each section and updated it with project-specific details
- **Generated a project charter** -- a stakeholder-ready document covering scope, success criteria, timeline, and risks
- **Created a stakeholder analysis** -- mapped who needs what from this project and how to communicate with them
- **Understood skills** -- how `crisp-dm-guide` and `retail-domain` skills auto-activate to give Claude domain expertise
- **Learned about subagents** -- what they are, how they are defined, and why dedicated agents produce better results
- **Discovered personalization options** -- how to adapt skills for your own organization and install community skills

### CRISP-DM Deliverables Completed

At the end of Phase 1, you should have:

- [x] Business objectives document with measurable success criteria
- [x] Data mining goals mapped to business goals
- [x] Project charter with resources, risks, and timeline
- [x] Stakeholder map with data owners identified

---

## Next Up

In **Chapter 2: Data Understanding**, you will get your hands on the actual data. You will connect Claude to a DuckDB database via MCP (Model Context Protocol), run exploratory data analysis using custom slash commands, assess data quality, and generate a full EDA notebook -- all guided by Claude. This is where the business problem meets reality.
