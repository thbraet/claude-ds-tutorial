# Chapter 4: Modeling

> **CRISP-DM Phase 4** -- Select modeling technique, generate test design, build model, assess model

This is the chapter many data scientists look forward to most: building models. But CRISP-DM reminds us that modeling is not about jumping to the fanciest algorithm. It is a disciplined process -- start with a baseline, add complexity only when justified, and evaluate rigorously.

In this chapter, Claude Code becomes your modeling partner. You will use specialized subagents to build models, agent teams to run parallel experiments, and new tools like Context7 and worktrees to work more efficiently than ever.

**Time estimate:** 75--100 minutes

**What you will build:**
- A naive baseline model
- A linear regression model
- An XGBoost model with hyperparameter tuning
- A model comparison report
- Parallel experiments using agent teams

**Prerequisites:** You should have completed Chapter 3 (Data Preparation) and have `data/processed/train_features.parquet` ready.

---

## Exercise 1: Selecting the Right Modeling Approach

Before writing any model code, let us have Claude help us think through the modeling strategy. This is CRISP-DM's "select modeling technique" sub-task.

### Step 1: Ask Claude for modeling recommendations

Open Claude Code and type:

```
I need to select modeling approaches for our store sales forecasting problem.

Context:
- We're predicting daily sales per store per product family
- The dataset has ~3M rows, 33 product families, 54 stores
- We've engineered lag features (1, 7, 14, 28, 364 days), rolling statistics
  (7-day and 28-day mean/std/min/max), time features, holiday features,
  and promotion features
- The evaluation metric is RMSLE
- The business goal is reducing overstock by 15% and out-of-stock by 20%

Recommend 3-4 modeling approaches, ordered from simplest to most complex.
For each, explain:
1. Why it's appropriate for this problem
2. Expected strengths and weaknesses
3. Approximate training time
4. When we would choose it over the others
```

### What Just Happened?

Claude analyzed the problem characteristics (time series, tabular data, millions of rows, business-oriented metric) and recommended a progression. You should see something like:

1. **Naive baseline** (last week's sales) -- The bar every model must beat
2. **Linear regression** with time and lag features -- Interpretable, fast, sets a statistical baseline
3. **XGBoost** -- The standard choice for tabular data; handles nonlinear patterns and feature interactions
4. **LightGBM or ensemble** -- If XGBoost plateaus, try a different boosting framework or blend

> **Tip:** This conversation is valuable even if you already know you want XGBoost. It documents your *reasoning* -- why you chose this approach -- which is a CRISP-DM requirement and makes your work defensible to stakeholders.

---

## Exercise 2: Building Models with the ML Engineer Subagent

### What Is the ML Engineer Agent?

Just as the `data-engineer` agent specialized in data wrangling, the `ml-engineer` agent is tuned for model building. Let us look at its configuration:

```markdown
---
name: ml-engineer
description: "Machine learning engineer for model selection, training,
  hyperparameter tuning, and experiment tracking."
tools: Read, Glob, Grep, Bash, Write, Edit
model: sonnet
maxTurns: 50
skills:
  - crisp-dm-guide
  - retail-domain
---
```

Key differences from the data-engineer agent:

| Aspect | data-engineer | ml-engineer |
|--------|--------------|-------------|
| **maxTurns** | 40 | 50 (modeling often needs more iteration) |
| **Skills** | data-validation, retail-domain | crisp-dm-guide, retail-domain |
| **Focus** | Clean data, build features | Train models, tune parameters, evaluate |

The `ml-engineer` loads the `crisp-dm-guide` skill, which means it will automatically structure its work according to CRISP-DM phases -- starting with a baseline, documenting decisions, and evaluating properly.

### Step 1: Build the baseline model

```
@ml-engineer Build a naive baseline model for our sales forecasting project.

The baseline should predict each store-family's sales using the same day's
sales from 7 days ago (lag-7 baseline).

1. Load data/processed/train_features.parquet
2. Create a time-based train/test split: use the last 28 days as the test set
3. Calculate RMSLE, MAE, and MAPE on the test set
4. Save the results to models/baseline_results.json
5. Print a summary showing the metrics

Use the evaluation functions in src/models/train.py (especially rmsle and
time_series_cv_split).
```

### What Just Happened?

The ml-engineer agent:
- Read the existing `src/models/train.py` to use your `rmsle` function
- Created a proper time-based split (not random -- critical for time series)
- Calculated multiple metrics for a complete picture
- Saved results in a structured format for later comparison

Note the baseline metrics. Every subsequent model must beat these numbers, or it is not worth the complexity.

### Step 2: Build a linear regression model

```
@ml-engineer Now build a linear regression model as our first statistical baseline.

1. Use the features from train_features.parquet
2. Feature columns: all lag features, rolling features, time features,
   onpromotion, and oil_price
3. Handle NaN values in lag features (drop rows or fill with 0 -- justify
   your choice)
4. Use TimeSeriesSplit with 5 folds, 28-day test windows
5. Report cross-validated RMSLE, MAE with standard deviations
6. Save the trained model to models/linear_regression.joblib
7. Compare results against the baseline

Use sklearn LinearRegression. Log the experiment using the
create_experiment_log function in src/models/train.py.
```

### Step 3: Build an XGBoost model

```
@ml-engineer Build an XGBoost model with sensible default parameters.

1. Use the same features and train/test split as the linear regression
2. Start with these XGBoost parameters:
   - n_estimators=500, learning_rate=0.05, max_depth=6
   - early_stopping_rounds=50 using a validation set
3. Use TimeSeriesSplit cross-validation (5 folds, 28 days each)
4. Report CV metrics: RMSLE, MAE, MAPE with standard deviations
5. Extract and display the top 15 most important features
6. Save the model to models/xgboost_default.joblib
7. Compare results against both baseline and linear regression

Print a model comparison table at the end.
```

### What Just Happened?

You now have three models, each more complex than the last. The ml-engineer agent:
- Maintained consistent evaluation (same splits, same metrics) across all three
- Used early stopping to prevent overfitting the XGBoost model
- Produced a comparison table so you can see the improvement at each step
- Followed the CRISP-DM principle of increasing complexity only with justification

---

## Exercise 3: Agent Teams for Parallel Experimentation (Advanced)

Now you will learn one of the most powerful features in Claude Code: **agent teams**. This lets you run multiple experiments simultaneously, each in its own independent context.

### What Are Agent Teams?

> **Claude Code Feature: Agent Teams**
>
> An agent team is a group of Claude instances that work in parallel, coordinated by a Team Lead:
>
> - **Team Lead**: Plans the work, assigns tasks, and synthesizes results
> - **Teammates**: Independent workers that each tackle one task simultaneously
>
> Think of it like a data science team where the lead assigns "you try XGBoost with these features, you try LightGBM, you try a different feature set" -- and everyone works at the same time.
>
> **When to use agent teams:**
> - Parallel experiments (try 3 different approaches simultaneously)
> - Large refactoring tasks (each teammate handles a different module)
> - Comprehensive testing (each teammate tests a different component)
>
> **Trade-offs to consider:**
> - **Token cost**: Each teammate uses its own token budget. Three teammates cost roughly 3x a single agent.
> - **Coordination overhead**: The Team Lead spends tokens planning and synthesizing. Simple tasks may not benefit.
> - **Best for independent work**: Teams work best when tasks do not depend on each other. If teammate B needs teammate A's output, use sequential work instead.

### Architecture: How Agent Teams Work

```
You (the user)
    |
    v
Team Lead (plans, assigns, synthesizes)
    |
    +--> Teammate 1: XGBoost with lag features only
    |
    +--> Teammate 2: XGBoost with all features + tuning
    |
    +--> Teammate 3: LightGBM with all features
    |
    v
Team Lead (collects results, compares, recommends)
```

Each teammate operates independently -- they cannot see each other's work. The Team Lead distributes tasks and collects results.

### Step 1: Launch an agent team

```
Start an agent team with 3 teammates to run parallel modeling experiments.

Shared context for all teammates:
- Dataset: data/processed/train_features.parquet
- Evaluation: TimeSeriesSplit, 5 folds, 28-day windows
- Metrics: RMSLE (primary), MAE, MAPE
- Save models to models/ with descriptive names
- Use the experiment logging from src/models/train.py

Teammate assignments:

Teammate 1 - "Feature Ablation":
  Train XGBoost using ONLY lag and rolling features (no time features,
  no promotions, no oil price). This tells us how much the simple
  features contribute.

Teammate 2 - "Full Feature XGBoost":
  Train XGBoost with ALL available features. Use Optuna for hyperparameter
  tuning with 20 trials. Save the best parameters.

Teammate 3 - "LightGBM Alternative":
  Train a LightGBM model with all features and default parameters.
  Compare its speed and accuracy to XGBoost.

After all teammates finish, produce a comparison table and recommend
which approach to pursue.
```

### What Just Happened?

The Team Lead:
1. Analyzed your request and created three independent work packages
2. Launched three teammates, each with their own Claude instance
3. Each teammate ran its experiment independently and in parallel
4. The Team Lead collected all results and produced a unified comparison

You should see a final comparison table like:

```
| Experiment             | CV RMSLE | CV MAE  | Train Time | Features |
|------------------------|----------|---------|------------|----------|
| Feature Ablation       | X.XXX    | X.XX    | Xs         | N        |
| Full Feature XGBoost   | X.XXX    | X.XX    | Xs         | N        |
| LightGBM Alternative   | X.XXX    | X.XX    | Xs         | N        |
```

> **Note:** Agent teams are a premium feature that uses more tokens. For learning purposes, you can also run these experiments sequentially by asking Claude to do them one at a time. The results will be the same -- teams just save wall-clock time.

---

## Exercise 4: Hyperparameter Tuning with Optuna

If the Full Feature XGBoost experiment from the previous exercise did not include Optuna tuning (or if you skipped agent teams), let us set it up now.

### Step 1: Set up Optuna tuning

```
@ml-engineer Set up Optuna hyperparameter tuning for our XGBoost model.

Create src/models/tune.py that:

1. Defines an Optuna objective function that:
   - Takes a trial object
   - Samples these hyperparameters:
     - n_estimators: 100-1000
     - max_depth: 3-10
     - learning_rate: 0.01-0.3 (log scale)
     - subsample: 0.6-1.0
     - colsample_bytree: 0.6-1.0
     - min_child_weight: 1-10
     - reg_alpha: 1e-8 to 10 (log scale)
     - reg_lambda: 1e-8 to 10 (log scale)
   - Runs 5-fold TimeSeriesSplit cross-validation
   - Returns mean RMSLE

2. Runs 50 trials with a TPE sampler
3. Prints the best parameters and score
4. Trains a final model with the best parameters on all training data
5. Saves the tuned model to models/xgboost_tuned.joblib
6. Saves the Optuna study to models/optuna_study.pkl

Include a __main__ block so I can run: python src/models/tune.py
```

### Step 2: Run the tuning

```
Run the Optuna tuning: python src/models/tune.py
```

> **Tip:** Optuna tuning with 50 trials and 5-fold CV can take 10--30 minutes depending on your hardware. While it runs, this is a good time to read ahead to the evaluation chapter or grab a coffee. Claude will show you the progress as Optuna reports each trial.

### Step 3: Compare tuned vs default

```
Compare the tuned XGBoost model against the default XGBoost model:
- Print both sets of metrics side by side
- Show which hyperparameters changed the most from defaults
- Tell me if the tuning was worth the extra compute time
```

---

## Exercise 5: Looking Up Documentation with Context7

When Claude needs to check the exact syntax of an XGBoost parameter or a scikit-learn function, it can look up the current documentation in real time using Context7.

### What Is Context7?

> **Claude Code Feature: Context7 MCP**
>
> Context7 is a documentation lookup service built into Claude Code. When Claude needs to reference library documentation -- for example, the exact parameters of `XGBRegressor` or the return type of `sklearn.model_selection.TimeSeriesSplit` -- it fetches the current documentation through Context7.
>
> **How it works:**
> 1. Claude identifies that it needs documentation (e.g., "What parameters does XGBRegressor accept?")
> 2. It queries Context7 with the library name and question
> 3. Context7 returns relevant documentation snippets and code examples
> 4. Claude uses this information to write accurate, up-to-date code
>
> **Why this matters:**
> - Claude's training data has a knowledge cutoff. Libraries release new versions with new parameters.
> - Context7 fetches the *current* documentation, so Claude's code matches the library version you have installed.
> - You do not need to do anything special -- Claude uses Context7 automatically when it needs documentation.

### Step 1: See Context7 in action

Ask Claude something that requires current documentation:

```
What are all the eval_metric options available for XGBRegressor in the version
I have installed? Show me the ones relevant to regression problems.
```

Claude will use Context7 to look up the XGBoost documentation and give you an accurate, current answer -- not one based on potentially outdated training data.

### Step 2: Use Context7 for API guidance

```
Using the current scikit-learn documentation, show me how to properly use
TimeSeriesSplit with a gap parameter to prevent data leakage. Is the gap
parameter available in my version?
```

Context7 ensures Claude gives you advice that matches your actual installed library versions.

> **Tip:** You do not need to invoke Context7 explicitly. Just ask Claude questions about library APIs, and it will automatically fetch the relevant documentation. Think of Context7 as Claude's ability to "look things up" instead of relying only on memory.

---

## Exercise 6: Isolated Experiments with Worktrees

What if you want to try a radically different approach without risking your current work? Worktrees let you create an isolated copy of your project on a separate git branch.

### What Are Worktrees?

> **Claude Code Feature: Worktrees**
>
> A git worktree is a separate working directory linked to the same git repository but on a different branch. In Claude Code, worktrees give you isolated sandboxes for experiments:
>
> - Your main branch stays untouched
> - The worktree gets its own branch with all your current files
> - You can experiment freely -- if it works, merge it back; if not, delete the worktree
> - Each worktree is fully independent: different code, different model files, different results
>
> **When to use worktrees:**
> - Trying a fundamentally different modeling approach
> - Experimenting with architectural changes to the pipeline
> - Testing a risky refactoring that might break things
> - Running A/B comparisons between approaches

### Step 1: Create a worktree for a Prophet experiment

First, make sure your current work is committed:

```
Save all our current modeling work -- commit everything with a descriptive
message about the baseline, linear regression, and XGBoost models
```

Then ask Claude to create a worktree:

```
Create a worktree called "prophet-experiment" where we can try Facebook Prophet
for time series forecasting without affecting our main XGBoost work
```

Claude will use the `EnterWorktree` feature to create a new worktree. You will see something like:

```
Created worktree at .claude/worktrees/prophet-experiment
Switched to new branch: prophet-experiment
Working directory: /path/to/project/.claude/worktrees/prophet-experiment
```

### Step 2: Build the Prophet model in the worktree

Now you are in an isolated environment. Everything you do here stays on the `prophet-experiment` branch:

```
@ml-engineer Build a Prophet model for our top 5 product families by total sales.

1. Install prophet if needed: pip install prophet
2. For each of the top 5 families, train a Prophet model on aggregated
   daily sales across all stores
3. Use the same 28-day test period as our other models
4. Calculate RMSLE and MAE for comparison
5. Save results to models/prophet_results.json
```

### Step 3: Compare and decide

```
Compare the Prophet results from this worktree against the XGBoost results
from our main branch. Is Prophet worth pursuing for this problem?
```

If Prophet is not competitive, you can simply exit the session and the worktree will be cleaned up. If it shows promise, you can merge the branch back.

> **Note:** When you end your Claude Code session, you will be asked whether to keep or remove the worktree. Choose "keep" if you want to continue the experiment later, or "remove" if you are done.

---

## Exercise 7: Generate a Model Comparison Report

Time to bring everything together. The `/model-report` command automates the creation of a comprehensive evaluation report.

### What Are Commands?

You learned about subagents earlier. **Commands** are another way to package reusable workflows. They are markdown files in `.claude/commands/` that define a task template.

### Step 1: Run the model-report command

```
/model-report
```

That is it -- just the slash command. Claude reads the template at `.claude/commands/model-report.md` and executes all the steps defined there:

1. **Executive Summary** -- Best model, key metric, business impact, recommendation
2. **Model Comparison Table** -- All models side by side with RMSLE, MAE, MAPE, training time
3. **Best Model Deep Dive** -- Hyperparameters, feature importance, learning curves
4. **Segment Analysis** -- Performance by store, by product family, by time period
5. **Error Analysis** -- Worst predictions, systematic biases, holiday/promo impact
6. **Business Impact** -- RMSLE translated to units of overstock and lost sales
7. **Recommendations** -- Next steps with justification

### Step 2: Review the report

Claude will save the report to `reports/model_evaluation_report.md` and visualizations to `reports/figures/`. Open the report and verify it covers all the CRISP-DM modeling deliverables:

- Justification for algorithm selection
- Baseline comparison
- Hyperparameter search results
- Model artifacts saved reproducibly

> **Tip:** The `/model-report` command runs a substantial amount of analysis. It will take several minutes. The result is a stakeholder-ready document that would take hours to create manually.

---

## Personalizing Your Modeling Workflow

### Add Your Preferred ML Libraries

Edit `.claude/agents/ml-engineer.md` to include libraries your team uses:

```markdown
## Technical Stack

- **scikit-learn** for classical ML
- **XGBoost** for gradient boosting (primary)
- **LightGBM** as alternative gradient boosting (faster for large datasets)
- **optuna** for Bayesian hyperparameter optimization
- **mlflow** for experiment tracking  # ADD THIS
- **wandb** for experiment visualization  # ADD THIS
```

### Integrate with MLflow or Weights & Biases

If your team uses experiment tracking platforms, add instructions to the ml-engineer agent:

```markdown
## Experiment Tracking

When training any model:
1. Start an MLflow run with `mlflow.start_run()`
2. Log all hyperparameters with `mlflow.log_params()`
3. Log all metrics with `mlflow.log_metrics()`
4. Log the model artifact with `mlflow.sklearn.log_model()` or `mlflow.xgboost.log_model()`
5. Tag the run with the CRISP-DM phase: `mlflow.set_tag("crisp_dm_phase", "modeling")`
```

### Discover Pre-trained Models

For projects where pre-trained models might help (e.g., embeddings for product descriptions), you can explore Hugging Face:

```
Search Hugging Face for pre-trained models relevant to retail sales forecasting
or time series prediction
```

If the Hugging Face MCP is configured, Claude can browse model cards and suggest relevant pre-trained models directly.

### Custom Skills for Model Governance

If your organization requires model governance (model cards, bias assessments, approval workflows), create a skill:

```
.claude/skills/model-governance/SKILL.md
```

With content like:

```markdown
## Model Governance Requirements

Before any model can be deployed:
- A model card must be generated (see template below)
- Bias assessment must be completed for all protected segments
- Model must be approved by the ML Review Board
- All training data lineage must be documented
```

This skill can be added to the ml-engineer agent's `skills` list so it automatically follows governance procedures.

---

## What You Learned

In this chapter, you practiced seven exercises and learned five new Claude Code features:

| Feature | What It Does | When to Use It |
|---------|-------------|----------------|
| **Subagents (ml-engineer)** | Specialized agent for model building | Training, tuning, and evaluating ML models |
| **Agent Teams** | Multiple Claude instances working in parallel | Parallel experiments, concurrent approaches |
| **Context7 MCP** | Real-time library documentation lookup | When you need current API docs or parameter details |
| **Commands (/model-report)** | Reusable task templates | Standardized reports, repeatable workflows |
| **Worktrees** | Isolated git branches for experiments | Risky experiments, A/B comparisons, alternative approaches |

**Key takeaways:**

1. **Always start with a baseline.** The naive lag-7 model is the bar every other model must clear. If your XGBoost cannot beat "use last week's sales," something is wrong.
2. **Subagents bring expertise.** The ml-engineer agent knew to use TimeSeriesSplit (not random K-fold), early stopping, and proper experiment logging because its instructions encoded these patterns.
3. **Agent teams trade tokens for time.** When you have three independent experiments, running them in parallel with a team saves wall-clock time. For dependent tasks, sequential work is better.
4. **Context7 keeps code current.** Library APIs change between versions. Context7 ensures Claude's code matches your installed packages.
5. **Worktrees protect your main work.** Experiment freely without fear of breaking what already works.

---

## Next Up

In **Chapter 5: Evaluation**, you will critically assess your models from both technical and business perspectives. You will use the `qa-reviewer` subagent to hunt for data leakage and methodology errors, the `business-analyst` agent to translate metrics into business impact, and multi-agent patterns to get both perspectives simultaneously.

Your models are trained. Now let us find out if they are actually *good*.
