# Chapter 5: Evaluation

> **CRISP-DM Phase 5** -- Evaluate results, review process, determine next steps

Building a model is not the finish line. Evaluation is where you find out whether your model actually solves the business problem -- or just looks good on a leaderboard. This is the phase where many data science projects stumble: the model performs well on test data, but fails in production because of data leakage, methodology errors, or a disconnect between technical metrics and business value.

In this chapter, you will put your models under a microscope. You will use adversarial review to hunt for hidden bugs, translate abstract metrics into concrete business impact, and build visualizations that tell a story stakeholders can understand.

**Time estimate:** 60--75 minutes

**What you will produce:**
- A comprehensive model evaluation report
- An adversarial review checking for leakage, bias, and methodology errors
- Business impact translation (RMSLE to dollars and units)
- Evaluation visualizations (actual vs predicted, error distributions, feature importance)
- A stakeholder recommendation document

**Prerequisites:** You should have completed Chapter 4 (Modeling) with at least a baseline and one trained model.

---

## Why Evaluation Needs Its Own Chapter

It is tempting to glance at a single metric ("RMSLE is 0.45 -- ship it!") and move on. But CRISP-DM makes evaluation a full phase because real-world models fail in ways that a single number cannot capture:

- A model with great average accuracy might systematically over-predict for small stores
- A model that looks perfect might be cheating by leaking future information
- A model with good RMSLE might still cause *more* overstock than the current manual process

This chapter teaches you to catch these problems using Claude Code's multi-agent capabilities.

---

## Exercise 1: Generate the Evaluation Report

Start by using the `/model-report` command to generate a comprehensive baseline report. If you already ran this at the end of Chapter 4, you can skip to Step 2 and review what you have.

### Step 1: Run the model-report command

```
/model-report
```

Claude reads the command template at `.claude/commands/model-report.md` and systematically works through seven report sections:

1. **Executive Summary** -- Your best model, its headline metric, and a deploy/iterate/abandon recommendation
2. **Model Comparison Table** -- All models side by side
3. **Best Model Deep Dive** -- Hyperparameters, feature importance, learning curves
4. **Segment Analysis** -- Performance broken down by store, product family, and time period
5. **Error Analysis** -- The 20 worst predictions and what went wrong
6. **Business Impact** -- Metrics translated to overstock units and lost sales dollars
7. **Recommendations** -- Next steps with justification

The report is saved to `reports/model_evaluation_report.md` with visualizations in `reports/figures/`.

### Step 2: Review the report critically

Open the report and ask yourself (and Claude) these questions:

```
I've read the model evaluation report. Help me answer these questions:

1. Is the improvement from baseline to XGBoost statistically significant,
   or could it be noise?
2. Are there any product families where the model is WORSE than the baseline?
3. Does accuracy degrade for predictions further in the future (day 1 vs day 28)?
4. What percentage of the error comes from the top 10% worst predictions?
```

These are the kinds of questions that separate a junior analysis from a senior one. Claude will dig into the data and give you specific answers.

---

## Exercise 2: Adversarial Review with the QA Reviewer Subagent

Now bring in the skeptic. The `qa-reviewer` subagent is configured with an adversarial mindset -- its job is to find problems that everyone else missed.

### Deep Dive: The QA Reviewer Agent

The `qa-reviewer` agent at `.claude/agents/qa-reviewer.md` is fundamentally different from the other agents. While the data-engineer and ml-engineer are *builders*, the qa-reviewer is a *critic*:

```markdown
---
name: qa-reviewer
description: "Quality assurance and adversarial reviewer for data science
  projects. Checks for data leakage, bias, overfitting, methodology errors,
  and code quality."
tools: Read, Glob, Grep, Bash
model: sonnet
maxTurns: 30
skills:
  - crisp-dm-guide
  - data-validation
---

You are a senior data science reviewer with a skeptical, detail-oriented
mindset. Your job is to find problems that others miss.
```

Notice what is *different* about this agent:

| Aspect | Builder Agents | QA Reviewer |
|--------|---------------|-------------|
| **Tools** | Read, Write, Edit, Bash | Read, Grep, Bash (NO Write/Edit) |
| **Mindset** | "How do I build this?" | "What is wrong with this?" |
| **Skills** | Domain + methodology | Methodology + validation |
| **Output** | Code and artifacts | Review reports and issue lists |

The qa-reviewer deliberately does **not** have Write or Edit permissions. It can only read and analyze -- it cannot "fix" issues itself. This separation of concerns is intentional: the reviewer finds problems, and you (with the builder agents) decide how to fix them.

### Step 1: Run the adversarial review

```
@qa-reviewer Conduct a thorough adversarial review of our entire modeling
pipeline. Check everything from data preparation through model evaluation.

Specifically investigate:

1. DATA LEAKAGE: Check src/features/build_features.py -- do any features
   use future information? Check the train/test split -- is it strictly
   time-based? Check any preprocessing -- was it fit on the full dataset?

2. METHODOLOGY: Is TimeSeriesSplit used correctly? Are metrics calculated
   on a proper holdout? Is there a meaningful baseline comparison?

3. REPRODUCIBILITY: Are random seeds set everywhere? Can the full pipeline
   be rerun from raw data? Are dependencies pinned?

4. BIAS: Does the model perform equally across all stores? Are there product
   families with systematically poor predictions?

5. CODE QUALITY: Are there tests for all critical functions? Is error
   handling adequate?

Be constructively critical. I'd rather find problems now than in production.
```

### What Just Happened?

The qa-reviewer agent systematically worked through its built-in checklists:

**Data Leakage Checklist** (from the agent's instructions):
- Target leakage: Are features derived from the target variable?
- Temporal leakage: Do features use future information?
- Train-test contamination: Was preprocessing fit on the full dataset?
- Feature leakage: Would all features be available at prediction time?
- Aggregation leakage: Were statistics computed across the train-test boundary?

**Evaluation Review Checklist:**
- Is the train/test split appropriate?
- Is the metric aligned with the business objective?
- Are confidence intervals reported?
- Is there a meaningful baseline?

The output is a structured review report with findings categorized as **Critical** (must fix), **Warning** (should fix), and **Observation** (nice to have).

### Step 2: Address the findings

If the qa-reviewer found critical issues (and it often does -- even experienced data scientists miss subtle leakage), fix them:

```
The QA review found that our rolling features might include the current day's
sales in the window. Fix the rolling feature functions in
src/features/build_features.py to ensure shift(1) is applied BEFORE the
rolling window, not after. Then rerun the pipeline and retrain the models.
```

> **Tip:** A common finding is that rolling statistics accidentally include the current observation. The fix is simple (`shift(1)` before `.rolling()`), but the impact on model validity is huge. This is exactly why adversarial review matters.

---

## Exercise 3: Translating Metrics to Business Impact

A RMSLE of 0.45 means nothing to a store manager. In this exercise, you will translate technical metrics into language that business stakeholders care about.

### Step 1: Ask Claude for business translation

```
Translate our model's performance into business terms.

Our best model (XGBoost) has:
- RMSLE: 0.45 on the test set
- MAE: about 15 units per store-family-day

The business context:
- 54 stores, 33 product families
- Average product price is roughly $3-5 per unit
- Overstock costs: 30% of unit value (waste for perishables, storage for others)
- Out-of-stock cost: estimated $2 per lost unit in revenue + customer dissatisfaction
- Current manual forecasting error is about 25 units per store-family-day

Calculate:
1. How many units of overstock/understock does this represent per store per week?
2. What is the estimated weekly dollar impact vs the current manual process?
3. Does this meet our project goal of 15% overstock reduction and 20% OOS reduction?
```

### Step 2: Use the business-analyst agent for stakeholder framing

Now bring in the business perspective alongside the technical one:

```
@business-analyst Based on our model evaluation results, draft an executive
summary for the VP of Supply Chain. Include:

1. What we built and why (1-2 sentences)
2. The bottom-line result in business terms (dollars saved, waste reduced)
3. How this compares to the current manual forecasting process
4. Key limitations and risks (be honest)
5. Recommended next steps

Write it for someone who has 5 minutes and no data science background.
Use concrete numbers, not technical jargon.
```

### What Just Happened?

The business-analyst agent wrote in a completely different voice than the ml-engineer. Instead of RMSLE and cross-validation, you should see language like:

- "Reduces estimated weekly overstock by X pallets across all stores"
- "Expected annual savings of $X based on current waste rates"
- "The model is most accurate for high-volume categories like GROCERY and BEVERAGES, and less reliable for low-volume categories like SEAFOOD and MAGAZINES"

This is the power of having specialized agents with different communication styles. The ml-engineer writes for data scientists. The business-analyst writes for executives.

> **Tip:** This is one of the most valuable uses of Claude Code for business analysts -- you do not need to understand the technical details yourself. Let the ml-engineer build the model, then let the business-analyst translate the results. Your job is to make sure the translation is accurate and the recommendations are sound.

---

## Exercise 4: Evaluation Visualizations

Numbers tell the story; visualizations make it memorable. In this exercise, you will create the key evaluation plots.

### Step 1: Actual vs Predicted plots

```
Create evaluation visualizations for our best model:

1. Scatter plot: Actual vs Predicted sales (with a perfect-prediction diagonal line)
2. Error distribution: Histogram of (predicted - actual) residuals
3. Error over time: Plot the average absolute error by day across the test period
4. Error by product family: Horizontal bar chart of MAE per product family
5. Error by store: Map or bar chart of MAE per store

Save all plots to reports/figures/ as PNG files.
Use the visualization functions in src/visualization/plots.py where possible,
and add new functions for any plots not already covered.
```

### Step 2: Feature importance deep dive

Run the feature importance command:

```
/feature-importance
```

This command (defined in `.claude/commands/feature-importance.md`) generates:

1. **Built-in feature importance** -- XGBoost's gain-based importance (top 20 features)
2. **Permutation importance** -- How much accuracy drops when each feature is shuffled
3. **SHAP values** (if the shap package is installed) -- How each feature pushes predictions up or down
4. **Feature group analysis** -- Aggregate importance by category (lag features, time features, promotions, etc.)

The comparison between built-in and permutation importance is particularly valuable. If they disagree significantly, it may indicate correlated features or potential leakage.

### Step 3: Interpret the results

```
Looking at the feature importance results, answer:
1. Which feature GROUP is most important (lags, rolling stats, time, promotions)?
2. Are there any features with high built-in importance but low permutation
   importance? (This could indicate redundancy.)
3. Are there features we could REMOVE without hurting accuracy?
4. What does the feature importance tell us about what actually drives sales
   in this retail chain?
```

---

## Exercise 5: Drafting the Stakeholder Recommendation

CRISP-DM's evaluation phase ends with a critical deliverable: the recommendation document. Should we deploy this model, iterate further, or go back to an earlier phase?

### Step 1: Draft the recommendation

```
@business-analyst Draft a stakeholder recommendation document for our sales
forecasting project. Structure it as:

## Executive Summary
[2-3 sentences: what we did, what we found, what we recommend]

## Business Context
[Why we started this project, what problem it solves]

## Results Summary
[Key metrics in business terms, comparison to current process]

## Model Strengths
[Where the model works well -- which stores, which product families, which
time horizons]

## Model Limitations
[Where the model struggles -- be transparent]

## Risk Assessment
[What could go wrong if we deploy? What's our fallback?]

## Recommendation
[Deploy / Iterate / Abandon -- with clear justification]

## Proposed Next Steps
[Concrete actions with timeline if we proceed]

Base this on the evaluation report in reports/model_evaluation_report.md
and the feature importance analysis.
```

### Step 2: Technical appendix

```
Add a technical appendix to the recommendation document that includes:
- Model architecture and hyperparameters
- Training data summary (date range, row count, feature count)
- Cross-validation strategy
- All metrics with confidence intervals
- Feature importance summary table
- Known issues from QA review and how they were addressed

This section is for the data science team, not executives.
```

---

## Exercise 6: Multi-Agent Review

For the final exercise, you will use the most sophisticated multi-agent pattern: running two different subagents in sequence, each bringing a different perspective to the evaluation.

### The Pattern: Sequential Multi-Agent Review

```
   Your models and code
          |
          v
   qa-reviewer (technical perspective)
     "Is this technically sound?"
          |
          v
   business-analyst (business perspective)
     "Does this solve the business problem?"
          |
          v
   You synthesize both perspectives
```

This is different from agent teams (which run in parallel). Here, the agents run in sequence because the business-analyst benefits from seeing the qa-reviewer's findings.

### Step 1: Technical review first

```
@qa-reviewer Review our complete project one final time before we present
to stakeholders. Focus on:

1. Have all previously identified issues been addressed?
2. Is the final model's performance honestly reported?
3. Are there any remaining leakage risks?
4. Is the pipeline reproducible? (Can someone else rerun it from scratch?)
5. Are the test coverage and code quality production-ready?

Produce a final verdict: PASS, PASS WITH NOTES, or FAIL.
```

### Step 2: Business review second

```
@business-analyst Review the project deliverables from a business perspective:

1. Does the model's accuracy actually meet our success criteria?
   (15% overstock reduction, 20% OOS reduction)
2. Is the recommendation document clear enough for non-technical stakeholders?
3. Are the limitations honestly presented?
4. Is the proposed deployment plan realistic?
5. What questions will the VP of Supply Chain ask, and do we have answers?

Also review the qa-reviewer's findings from the previous step and flag
any technical issues that have business implications.
```

### What Just Happened?

You just completed a dual-perspective evaluation:

1. The **qa-reviewer** verified technical soundness -- no leakage, reproducible pipeline, honest metrics, adequate tests
2. The **business-analyst** verified business alignment -- metrics meet goals, stakeholder document is clear, deployment plan is realistic

This multi-agent pattern is powerful because each agent catches different types of issues. The qa-reviewer catches bugs that could invalidate results. The business-analyst catches disconnects between technical results and business value.

> **Tip:** For important deliverables, always run both perspectives. A technically perfect model that does not solve the business problem is worthless. A business-aligned model with data leakage is dangerous. You need both lenses.

### How Skills Enhance the Review

Notice that during this evaluation, the **crisp-dm-guide** skill activated automatically for both agents. This skill ensures that evaluation covers all CRISP-DM criteria:

- Technical metrics with confidence intervals
- Business impact translation
- Error analysis (where does the model fail?)
- Recommendation document for stakeholders

The skill acts as an invisible checklist, prompting each agent to address items that might otherwise be forgotten.

---

## Personalizing Your Evaluation Workflow

### Define Your Success Metrics in CLAUDE.md

Add your organization's specific evaluation criteria to `CLAUDE.md`:

```markdown
## Evaluation Standards

Success criteria for this project:
- RMSLE < 0.50 on the 28-day holdout test set
- MAE must be lower than the manual forecast baseline (25 units)
- Model must not systematically over-predict by more than 10% for any
  product family
- Business impact: projected 15% reduction in overstock waste,
  20% reduction in out-of-stock incidents
- Model must pass QA review with no CRITICAL findings

When evaluating, always report:
- Metrics with 95% confidence intervals
- Performance broken down by store type (A, B, C, D, E) and product
  family
- Comparison against both naive baseline AND current manual process
```

Every agent and command will reference these criteria automatically.

### Create Evaluation Templates

If your organization has a standard model evaluation template (many regulated industries do), encode it as a skill:

```
.claude/skills/eval-template/SKILL.md
```

```markdown
## Evaluation Template Requirements

All model evaluations must include:
1. Model Card (see template below)
2. Bias Assessment across protected categories
3. Performance degradation analysis (how does accuracy change over time?)
4. Data drift monitoring plan
5. Rollback criteria (when should we stop using this model?)
```

### Responsible AI Toolkits

For organizations with responsible AI requirements, consider integrating:

- **Model cards**: Add a model card template to your evaluation skill
- **Fairness metrics**: Include demographic parity or equalized odds checks in the qa-reviewer's checklist
- **Explainability reports**: Use SHAP or LIME explanations as standard evaluation deliverables
- **Audit trails**: Log all model decisions, data lineage, and evaluation results for regulatory compliance

You can add instructions for any of these to the qa-reviewer agent's markdown file, and they will become part of every review automatically.

---

## What You Learned

In this chapter, you practiced six exercises and deepened your use of four Claude Code features:

| Feature | What It Does | How You Used It |
|---------|-------------|-----------------|
| **Commands (/model-report, /feature-importance)** | Reusable task templates | Generated comprehensive evaluation reports and feature analysis |
| **Subagents (qa-reviewer)** | Adversarial technical review | Hunted for data leakage, bias, and methodology errors |
| **Multi-agent patterns** | Sequential use of different subagents | Combined technical (qa-reviewer) and business (business-analyst) perspectives |
| **Skills (crisp-dm-guide)** | Automatic methodology guidance | Ensured evaluation covered all CRISP-DM requirements |

**Key takeaways:**

1. **One metric is never enough.** RMSLE, MAE, and MAPE each tell a different part of the story. Segment-level analysis reveals problems that averages hide.
2. **Adversarial review catches what you miss.** The qa-reviewer agent found issues that the builder agents introduced, because it was configured to look for problems, not write code.
3. **Business translation is a skill.** The same model result means different things to a data scientist ("RMSLE improved 15%") and a supply chain VP ("$40K less waste per month"). Use the business-analyst agent to bridge this gap.
4. **Multi-agent review covers blind spots.** No single perspective catches everything. The qa-reviewer finds technical bugs; the business-analyst finds strategic misalignment. Running both gives you confidence.
5. **Encode your standards in CLAUDE.md and skills.** Success criteria, evaluation templates, and governance requirements should be in configuration, not in your memory. This way every evaluation is consistent.

---

## Next Up

In **Chapter 6: Deployment**, you will take your validated model and put it into production. You will build a FastAPI prediction service, set up monitoring for data drift and model degradation, and create the documentation needed for a production handoff.

Your model has passed both technical and business review. It is time to ship it.
