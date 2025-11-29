# Agent Architecture & Data Flow

## Overview
This system implements a multi-agent architecture for autonomous Facebook Ads performance analysis. The agents collaborate to diagnose ROAS fluctuations, identify root causes, and recommend creative improvements.

## Agent Roles

### 1. **Planner Agent** (`src/agents/planner.py`)
**Purpose**: Decomposes user queries into executable subtasks and orchestrates the analysis workflow.

**Inputs**: 
- User query (e.g., "Analyze ROAS drop in last 7 days")

**Outputs**: 
- Structured plan with subtasks and agent assignments

**Responsibilities**:
- Parse user intent
- Determine required analysis steps
- Assign tasks to appropriate agents
- Define execution order

---

### 2. **Data Agent** (`src/agents/data_agent.py`)
**Purpose**: Loads Facebook Ads data and generates statistical summaries for downstream analysis.

**Inputs**: 
- CSV file path

**Outputs**: 
- Pandas DataFrame (full dataset)
- Data summary dict (aggregated metrics, trends, top/bottom performers)

**Responsibilities**:
- Load and validate CSV data
- Calculate aggregate metrics (mean ROAS, CTR, spend)
- Identify platform/campaign performance leaders and laggards
- Extract time-series trends (e.g., 7-day ROAS trajectory)
- Find low-CTR campaigns for creative optimization

---

### 3. **Insight Agent** (`src/agents/insight_agent.py`)
**Purpose**: Generates data-driven hypotheses explaining performance changes using LLM reasoning.

**Inputs**: 
- Data summary from Data Agent

**Outputs**: 
- List of hypotheses with reasoning and initial confidence scores

**Responsibilities**:
- Analyze patterns in summary statistics
- Formulate hypotheses for ROAS/CTR changes
- Provide reasoning for each hypothesis
- Assign preliminary confidence scores

**Reasoning Structure**:
1. **Think**: Identify anomalies in metrics
2. **Analyze**: Determine potential root causes
3. **Conclude**: Rank hypotheses by plausibility

---

### 4. **Evaluator Agent** (`src/agents/evaluator_agent.py`)
**Purpose**: Validates hypotheses quantitatively using the full dataset.

**Inputs**: 
- Full DataFrame from Data Agent
- Hypotheses from Insight Agent

**Outputs**: 
- Validated insights with evidence and refined confidence scores

**Responsibilities**:
- Test hypotheses against actual data
- Calculate statistical evidence (e.g., trend confirmation, threshold checks)
- Filter out low-confidence insights (< 0.6)
- Provide quantitative justification for each validated insight

**Quality Criteria**:
- Confidence ≥ 0.6 threshold
- Evidence must cite specific data points
- Reasoning must be backed by calculations

---

### 5. **Creative Generator Agent** (`src/agents/creative_generator.py`)
**Purpose**: Produces new ad creative variations for underperforming campaigns.

**Inputs**: 
- Data summary (especially low-CTR campaigns)
- Existing creative messages

**Outputs**: 
- JSON array of new creative recommendations (headlines, messages, CTAs)

**Responsibilities**:
- Identify campaigns with CTR < threshold
- Analyze existing successful creative patterns
- Generate diverse creative variations (emotional, logical, urgency-based)
- Provide reasoning for each creative recommendation

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER QUERY                               │
│           "Analyze ROAS drop in last 7 days"                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
                  ┌────────────────────┐
                  │  PLANNER AGENT     │
                  │  Decomposes query  │
                  │  into subtasks     │
                  └────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   Execution Plan       │
              │   [Task 1, Task 2,...] │
              └────────┬───────────────┘
                       │
       ┌───────────────┴───────────────┐
       │                               │
       ▼                               ▼
┌──────────────┐              ┌──────────────────┐
│ DATA AGENT   │              │  (Other Tasks)   │
│ Load CSV     │              │                  │
└──────┬───────┘              └──────────────────┘
       │
       ├──► DataFrame (full dataset)
       │
       └──► Data Summary (dict)
              │
              ├─► roas_mean, ctr_mean, spend_mean
              ├─► best_platform, worst_platform
              ├─► roas_trend (7-day time series)
              └─► lowest_ctr_rows (campaigns needing help)
              │
              ▼
       ┌──────────────────┐
       │  INSIGHT AGENT   │
       │  Generate        │
       │  hypotheses      │
       └────────┬─────────┘
                │
                ├──► Hypothesis 1: "ROAS decreased"
                ├──► Hypothesis 2: "CTR too low"
                └──► Hypothesis 3: "Platform inefficiency"
                │
                ▼
       ┌──────────────────┐
       │ EVALUATOR AGENT  │◄─── DataFrame (for validation)
       │ Validate with    │
       │ quantitative     │
       │ evidence         │
       └────────┬─────────┘
                │
                └──► Validated Insights (JSON)
                       │
                       ├─► insight + evidence + confidence ≥ 0.6
                       │
                       ▼
                  ┌────────────────┐
                  │ insights.json  │
                  └────────────────┘

       Data Summary
              │
              ▼
       ┌────────────────────────┐
       │ CREATIVE GENERATOR     │
       │ Produce new ad copy    │
       │ for low-CTR campaigns  │
       └────────┬───────────────┘
                │
                └──► Creative Recommendations (JSON)
                       │
                       ├─► new_headline + new_message + new_cta
                       │
                       ▼
                  ┌────────────────┐
                  │ creatives.json │
                  └────────────────┘

       All Results
              │
              ▼
       ┌────────────────┐
       │  ORCHESTRATOR  │
       │  Generate      │
       │  final report  │
       └────────┬───────┘
                │
                ▼
         ┌──────────────┐
         │  report.md   │
         └──────────────┘
```

## Execution Flow

1. **User Query** → Orchestrator receives natural language query
2. **Planning Phase** → Planner Agent decomposes query into subtasks
3. **Data Loading** → Data Agent loads CSV and creates summary
4. **Hypothesis Generation** → Insight Agent formulates explanations
5. **Validation** → Evaluator Agent tests hypotheses quantitatively
6. **Creative Ideation** → Creative Generator produces new ad variations
7. **Reporting** → Orchestrator compiles results into:
   - `insights.json` (validated hypotheses)
   - `creatives.json` (creative recommendations)
   - `report.md` (human-readable summary)

## Agent Interaction Patterns

### Pattern 1: Sequential Pipeline
```
Data Agent → Insight Agent → Evaluator Agent
```
Insights are generated from summary, then validated against full dataset.

### Pattern 2: Parallel Consumption
```
Data Summary → Insight Agent
            → Creative Generator
```
Both agents consume the same summary independently.

### Pattern 3: Reflection Loop (Future Enhancement)
```
Evaluator → (Low confidence?) → Insight Agent (retry with different approach)
```

## Quality Control Mechanisms

1. **Confidence Thresholds**: Evaluator filters insights with confidence < 0.6
2. **Evidence Requirements**: All insights must cite specific metrics/data points
3. **Data Validation**: Data Agent checks for required columns before processing
4. **Structured Output**: JSON schemas enforce consistent format across agents

## Technology Stack

- **Framework**: Python 3.10+
- **Data Processing**: pandas
- **LLM**: Google Gemini (via `google.generativeai`)
- **Orchestration**: Custom multi-agent orchestrator
- **Configuration**: YAML-based config
- **Logging**: Structured JSON logs

## Agentic Reasoning Features

✅ **Decomposition**: Planner breaks queries into subtasks  
✅ **Hypothesis-driven**: Insight Agent proposes explanations  
✅ **Validation**: Evaluator tests hypotheses quantitatively  
✅ **Reflection**: Low-confidence results can trigger retries (future)  
✅ **Contextual**: Creative Generator uses existing successful patterns  

## Extensibility

New agents can be added by:
1. Creating agent class in `src/agents/`
2. Adding corresponding prompt file in `prompts/`
3. Registering agent in Orchestrator
4. Updating Planner to assign relevant subtasks
