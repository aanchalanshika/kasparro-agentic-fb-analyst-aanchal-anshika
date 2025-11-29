# Kasparro — Agentic Facebook Performance Analyst

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Multi-agent system for autonomous Facebook Ads performance analysis, ROAS diagnosis, and creative optimization.

## 🚀 Quick Start

```bash
# 1. Clone and navigate
cd kasparro-agentic-fb-analyst-aanchal

# 2. Check Python version (must be >= 3.10)
python --version

# 3. Setup environment and install dependencies
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt

# 4. Set API key (required for LLM agents)
set GOOGLE_API_KEY=your_gemini_api_key_here  # Windows
# export GOOGLE_API_KEY=your_key  # Mac/Linux

# 5. Run analysis
python run.py "Analyze ROAS drop in last 7 days"

# 6. Check outputs
dir reports\  # insights.json, creatives.json, report.md
```

## 📊 Data Setup

### Option 1: Use Sample Data (Default)
The repo includes a sample dataset. No additional setup needed.

```yaml
# config/config.yaml
data:
  csv_path: "data/synthetic_fb_ads_undergarments.csv"
```

### Option 2: Use Full Dataset
Place your full CSV at the path specified in config, or set environment variable:

```bash
set DATA_CSV_PATH=C:\path\to\full_dataset.csv
```

**Data requirements**: See [`data/README.md`](data/README.md) for schema details.

## 🏗️ Architecture

This system implements a **Planner-driven multi-agent architecture** with quantitative validation and creative generation capabilities.

### Agent Roles

1. **Planner Agent** - Decomposes queries into executable subtasks
2. **Data Agent** - Loads CSV and generates statistical summaries
3. **Insight Agent** - Formulates hypotheses explaining performance patterns
4. **Evaluator Agent** - Validates hypotheses with quantitative evidence
5. **Creative Generator** - Produces new ad copy for low-CTR campaigns

**📈 For detailed architecture diagram and data flow**, see [`agent_graph.md`](agent_graph.md)

### Execution Flow

```
User Query → Planner → [Data Agent → Insight Agent → Evaluator Agent]
                     ↓
                Creative Generator → Report
```

## 📁 Repository Structure

```
kasparro-agentic-fb-analyst-aanchal/
├── README.md                   # This file
├── agent_graph.md              # Architecture diagram & agent roles
├── run.py                      # Main CLI entry point
├── requirements.txt            # Pinned dependencies
├── Makefile                    # Automation commands
├── config/
│   └── config.yaml             # Thresholds, paths, LLM settings
├── src/
│   ├── agents/                 # Agent implementations
│   │   ├── planner.py
│   │   ├── data_agent.py
│   │   ├── insight_agent.py
│   │   ├── evaluator_agent.py
│   │   └── creative_generator.py
│   ├── orchestrator/
│   │   └── orchestrator.py     # Multi-agent coordinator
│   └── utils/                  # Helper functions
├── prompts/                    # Structured prompt templates (.md)
│   ├── planner_prompt.md
│   ├── data_agent_prompt.md
│   ├── insight_prompt.md
│   ├── evaluator_prompt.md
│   └── creative_prompt.md
├── data/
│   ├── synthetic_fb_ads_undergarments.csv
│   └── README.md               # Data schema & usage
├── reports/                    # Generated outputs
│   ├── insights.json           # Validated hypotheses
│   ├── creatives.json          # Creative recommendations
│   └── report.md               # Human-readable summary
├── logs/
│   └── execution_log.json      # Structured execution logs
└── tests/
    └── test_evaluator.py       # Unit tests for validation layer
```

## ⚙️ Configuration

Edit `config/config.yaml` to customize:

```yaml
python_version: "3.10"
random_seed: 42
confidence_min: 0.6              # Minimum confidence for validated insights

llm:
  provider: "google"              # LLM provider (google/openai/anthropic)
  model: "gemini-1.5-flash"
  temperature: 0.7

thresholds:
  confidence_minimum: 0.6         # Filter insights below this
  low_ctr_threshold: 0.02         # CTR < 2% triggers creative generation
  roas_trend_days: 7              # Days for ROAS trend analysis
```

## 🔧 Commands (Makefile)

```bash
make setup          # Create venv + install deps
make run            # Run with default query
make test           # Run pytest test suite
make lint           # Check code quality (flake8)
make clean          # Remove generated files
make all            # setup + test + lint

# Custom query
make run-custom QUERY="Why is CTR low?"
```

**Windows users**: Use `mingw32-make` or run commands directly:
```bash
python run.py "Your query here"
pytest tests/ -v
```

## 📤 Outputs

### `reports/insights.json`
Validated hypotheses with confidence scores and evidence:

```json
[
  {
    "hypothesis": "ROAS has decreased in recent days",
    "reasoning": "THINK: ROAS dropped from 2.84 to 1.92...",
    "validation_evidence": "ROAS dropped from 2.84 to 1.92 (32.4% decline)",
    "confidence": 0.92,
    "metrics_checked": ["roas", "date"],
    "validation_method": "trend_confirmation",
    "status": "validated"
  }
]
```

### `reports/creatives.json`
Creative recommendations for low-CTR campaigns:

```json
[
  {
    "campaign_name": "Summer_Comfort",
    "current_ctr": 0.0142,
    "creative_variations": [
      {
        "variation_id": 1,
        "headline": "Experience All-Day Comfort",
        "message": "Breathable, ultra-soft fabrics...",
        "cta": "Shop Comfort Now",
        "framework": "emotional",
        "reasoning": "Emotional appeal addresses core benefit..."
      }
    ]
  }
]
```

### `reports/report.md`
Human-readable Markdown summary for stakeholders.

## ✅ Validation & Quality Control

### Hypothesis Validation Process

1. **Insight Generation**: LLM formulates hypotheses from data summary
2. **Quantitative Testing**: Evaluator tests each hypothesis against full dataset
3. **Confidence Filtering**: Only insights with confidence ≥ 0.6 are kept
4. **Evidence Requirements**: All insights must cite specific data points

**Validation Methods**:
- Trend confirmation (time-series analysis)
- Threshold testing (CTR < 2%, ROAS benchmarks)
- Comparative analysis (platform/campaign performance)
- Correlation analysis (metric relationships)

### Quality Thresholds
- Minimum confidence: 0.6 (configurable)
- Low CTR threshold: 2%
- ROAS decline alert: >20% drop over 7 days

## 🧪 Testing

Run the test suite to verify agent logic:

```bash
pytest tests/ -v

# Specific test file
pytest tests/test_evaluator.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

**Tests include**:
- Confidence threshold filtering
- ROAS decline validation
- CTR threshold checks
- Platform comparison validation
- Data summary format verification

## 🔍 Observability

### Execution Logs
Structured JSON logs in `logs/execution_log.json`:

```json
[
  {
    "timestamp": "2024-01-15 14:30:22",
    "event": "plan_generated",
    "data": {"subtasks": [...]}
  },
  {
    "timestamp": "2024-01-15 14:30:25",
    "event": "insights_validated",
    "data": {"count": 3}
  }
]
```

### Prompt Tracing
All prompts are stored as files in `prompts/`, making it easy to:
- Version control prompt changes
- A/B test different prompt strategies
- Debug LLM outputs

## 🎯 Example Queries

```bash
# ROAS analysis
python run.py "Why did ROAS drop?"
python run.py "Analyze ROAS performance over last 7 days"

# CTR optimization
python run.py "Why is CTR low and how to improve it?"
python run.py "Generate creative ideas for underperforming campaigns"

# Platform comparison
python run.py "Which platform performs better: Facebook or Instagram?"

# Comprehensive analysis
python run.py "Analyze campaign performance and suggest improvements"
```

## 🛠️ Reproducibility

### Seed Randomness
Set `random_seed: 42` in `config/config.yaml` for deterministic results.

### Pinned Dependencies
All versions are pinned in `requirements.txt`:
```
pandas==2.1.4
google-generativeai==0.3.2
pyyaml==6.0.1
pytest==7.4.3
```

### Sample Data Toggle
Switch between sample and full dataset in config:
```yaml
data:
  csv_path: "data/synthetic_fb_ads_undergarments.csv"  # Sample
  # csv_path: "data/full_dataset.csv"                  # Full
```


### Low-quality insights
**Solution**: 
1. Check LLM temperature in config (lower = more deterministic)
2. Verify data summary has sufficient information
3. Review prompt templates in `prompts/`

## 📦 Dependencies

- **pandas** - Data processing and analysis
- **google-generativeai** - LLM for agentic reasoning
- **pyyaml** - Configuration management
- **pytest** - Unit testing framework
- **flake8** - Code quality linting

## 🏷️ Version & Release

**Current Version**: v1.0

**Release Tag**: `v1.0` (See [Releases](https://github.com/your-username/kasparro-agentic-fb-analyst-aanchal/releases/tag/v1.0))

**Commit Hash**: [To be added after git commit]

## 📝 Self-Review PR

See [Pull Request #1: Self-Review](https://github.com/your-username/kasparro-agentic-fb-analyst-aanchal/pull/1) for:
- Design decisions and tradeoffs
- Architecture rationale
- Prompt engineering approach
- Testing strategy

## 🤝 Contributing

This is an assignment submission. Contributions are not expected, but feedback is welcome!

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Built for the **Kasparro Applied AI Engineer Assignment**.

## 📧 Contact

**Developer**: Aanchal  
**Assignment**: Agentic Facebook Performance Analyst  
**Company**: Kasparro

---

**Command to reproduce outputs**:
```bash
set GOOGLE_API_KEY=your_key
python run.py "Analyze ROAS drop in last 7 days"
```

**Expected runtime**: ~10-30 seconds (varies by LLM latency)
