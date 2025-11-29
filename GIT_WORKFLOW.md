# Git Workflow for Submission

This document guides you through the Git hygiene requirements for the Kasparro assignment.

## Requirements

✅ At least 3 commits  
✅ v1.0 release tag  
✅ PR titled "self-review"  

## Step-by-Step Git Workflow

### 1. Initialize Git Repository (if not already done)

```bash
cd d:\class\sem7\kasparro-agentic-fb-analyst-aanchal
git init
git branch -M main
```

### 2. Make Initial Commit

```bash
# Stage all files
git add .

# Create initial commit
git commit -m "Initial commit: Project structure and basic agents"

# Verify
git log --oneline
```

### 3. Make Feature Commits (to reach 3+ commits)

```bash
# Commit 2: Prompts and LLM integration
git add prompts/ src/agents/ src/orchestrator/
git commit -m "feat: Add LLM-based agents with prompt templates from files

- Implement Planner agent with dynamic task decomposition
- Add prompt templates for all agents in prompts/
- Update Orchestrator to use Planner in control loop
- Integrate Google Gemini for hypothesis generation"

# Commit 3: Tests and documentation
git add tests/ data/README.md agent_graph.md Makefile
git commit -m "feat: Add comprehensive testing and documentation

- Implement unit tests for Evaluator and Data agents
- Add agent_graph.md with architecture diagram
- Create data/README.md with schema documentation
- Add Makefile for standardized commands"

# Commit 4: Final polish
git add README.md config/config.yaml requirements.txt
git commit -m "docs: Complete README and configuration

- Comprehensive README with quick start guide
- Add config.yaml with LLM and threshold settings
- Pin dependencies in requirements.txt
- Add troubleshooting and example queries"

# Verify you have 3+ commits
git log --oneline
```

### 4. Create v1.0 Release Tag

```bash
# Create annotated tag
git tag -a v1.0 -m "Release v1.0: Agentic Facebook Performance Analyst

Features:
- Multi-agent architecture with Planner-driven execution
- LLM-powered insight generation and validation
- Creative recommendation engine
- Comprehensive testing and documentation
- Structured prompt templates and logging"

# Verify tag
git tag -l
git show v1.0
```

### 5. Create Self-Review Branch and PR

```bash
# Create new branch for self-review
git checkout -b self-review

# Create SELF_REVIEW.md document
# (See content below)

# Add self-review document
git add SELF_REVIEW.md
git commit -m "docs: Add self-review document with design rationale"

# Push both branches
git checkout main
git push origin main
git push origin self-review
git push origin v1.0

# Go to GitHub and create PR from self-review → main
# Title: "self-review"
```

### 6. Create GitHub Repository

```bash
# On GitHub: Create new repository (public)
# Name: kasparro-agentic-fb-analyst-aanchal

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/kasparro-agentic-fb-analyst-aanchal.git

# Push everything
git push -u origin main
git push origin --tags
git push origin self-review
```

### 7. Create Pull Request on GitHub

1. Go to your repository on GitHub
2. Click "Pull requests" → "New pull request"
3. Base: `main`, Compare: `self-review`
4. Title: **"self-review"**
5. Description: See template below
6. Create PR (don't merge it)

## Self-Review PR Template

```markdown
# Self-Review: Design Decisions & Tradeoffs

## Architecture Decisions

### 1. Planner-Driven Multi-Agent System
**Decision**: Use Planner agent to dynamically decompose queries into subtasks.

**Rationale**: 
- Flexible handling of different query types
- Clear separation of concerns
- Easy to add new agents without changing orchestration logic

**Tradeoff**: 
- ✅ More adaptable to new scenarios
- ❌ Slightly higher latency due to LLM plan generation
- **Mitigation**: Fallback to rule-based planning if LLM fails

### 2. Prompts as External Files
**Decision**: Store all prompts in `prompts/` as Markdown files.

**Rationale**:
- Easy to version control and track changes
- Non-engineers can modify prompts
- A/B testing different prompt strategies

**Tradeoff**:
- ✅ Better maintainability and collaboration
- ❌ Requires file I/O at runtime
- **Impact**: Negligible performance impact vs. massive maintainability gain

### 3. Two-Stage Validation (Insight → Evaluator)
**Decision**: Separate hypothesis generation from validation.

**Rationale**:
- LLMs are better at creative hypothesis generation
- Quantitative validation ensures statistical rigor
- Confidence filtering removes low-quality insights

**Tradeoff**:
- ✅ Higher quality insights
- ❌ More complex pipeline
- **Result**: Worth it for accuracy and trustworthiness

### 4. Fallback Logic for LLM Failures
**Decision**: All agents have rule-based fallbacks if LLM is unavailable.

**Rationale**:
- System still works without API keys
- Graceful degradation for testing
- Reduces API costs during development

**Tradeoff**:
- ✅ More robust and testable
- ❌ More code to maintain
- **Benefit**: Can run tests without API credits

## Prompt Engineering Approach

### Structured Format
All prompts follow this template:
1. **Role definition**: Who is the agent?
2. **Context**: What data/inputs are available?
3. **Task**: What should the agent do?
4. **Reasoning structure**: Think → Analyze → Conclude
5. **Output format**: JSON schema with examples
6. **Quality criteria**: What makes a good output?

### Reflection Questions
Each prompt includes self-check questions to improve LLM accuracy.

### Example-Driven
Prompts include concrete examples of good outputs to guide the LLM.

## Testing Strategy

### Unit Tests
- Focus on Evaluator (core validation logic)
- Test confidence threshold filtering
- Validate different validation methods

### Why Not Full Integration Tests?
**Decision**: Focus on unit tests for evaluator.

**Rationale**:
- LLM outputs are non-deterministic (hard to test)
- Evaluator has testable quantitative logic
- Time constraint (8-10 hours)

**Future Enhancement**: Mock LLM responses for integration tests

## Known Limitations

1. **No long-term memory**: Each run is stateless
2. **Limited error handling**: Basic exception catching
3. **No retry logic**: LLM failures fall back to rules immediately
4. **Hardcoded thresholds**: CTR < 2%, confidence ≥ 0.6

## Future Enhancements

1. **Iterative refinement**: Low-confidence insights trigger re-analysis
2. **Memory layer**: Store insights across runs
3. **Advanced validation**: Statistical significance tests
4. **Multi-LLM support**: OpenAI, Anthropic adapters

## Time Breakdown (~9 hours)

- Architecture design: 1.5 hours
- Agent implementation: 3 hours
- Prompt engineering: 2 hours
- Testing & validation: 1.5 hours
- Documentation: 1 hour

## Conclusion

This implementation prioritizes:
1. **Robustness**: Fallback logic ensures it always runs
2. **Maintainability**: Prompts as files, clear separation
3. **Quality**: Quantitative validation filters bad insights
4. **Extensibility**: Easy to add new agents/validation methods
```

## Submission Checklist

Before submitting:

- [ ] At least 3 commits made
- [ ] v1.0 tag created
- [ ] GitHub repo is public
- [ ] self-review PR created (not merged)
- [ ] README has:
  - [ ] Quick start commands
  - [ ] Link to agent_graph.md
  - [ ] Link to self-review PR
  - [ ] Example outputs
- [ ] All files committed:
  - [ ] agent_graph.md
  - [ ] prompts/*.md
  - [ ] tests/test_evaluator.py
  - [ ] data/README.md
  - [ ] Makefile
  - [ ] config/config.yaml
  - [ ] requirements.txt

## Final Submission Format

```
Repository: https://github.com/YOUR_USERNAME/kasparro-agentic-fb-analyst-aanchal
Commit Hash: abc123def456
Release Tag: v1.0
Self-Review PR: https://github.com/YOUR_USERNAME/kasparro-agentic-fb-analyst-aanchal/pull/1
Command Used: python run.py "Analyze ROAS drop in last 7 days"
```
