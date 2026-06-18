# Aegis — Agent Specifications

## Overview

Aegis employs five AI verification agents, each with a distinct responsibility. Agents run sequentially within a single verification pipeline, producing structured outputs consumed by the Kratos consensus engine.

---

## Agent 1: Argus — Evidence Collector

**Role**: Verify that work actually exists in the repository.

**Inputs**:
- Repository URL
- Milestone submission date
- Date range (milestone start → submission)

**Process**:
1. Fetch commits in the date range via GitHub API
2. Count changed files and lines of code
3. List pull requests merged in the period
4. Detect active branches

**Output Schema**:
```json
{
  "evidence_found": true,
  "commits_count": 12,
  "files_changed": 34,
  "lines_added": 980,
  "lines_removed": 120,
  "pull_requests_merged": 3,
  "confidence": 0.87
}
```

**Confidence Formula**:
```
confidence = min(1.0, (commits * 0.4 + files_changed * 0.3 + pr_count * 0.3) / threshold)
```

**Pass Threshold**: `confidence > 0.70`

---

## Agent 2: Themis — Scope Validator

**Role**: Compare milestone requirements to actual repository changes.

**Model**: Claude Haiku (via Anthropic API)

**Inputs**:
- Milestone title and description
- Acceptance criteria (from milestone definition)
- List of changed files and commit messages (from Argus output)
- Diff summaries

**Process**:
1. Send milestone spec + evidence to Claude Haiku
2. Ask model to score how well the changes satisfy the requirements
3. Parse structured response

**Output Schema**:
```json
{
  "scope_match": 0.82,
  "requirements_met": ["authentication flow", "JWT tokens", "refresh logic"],
  "requirements_missing": ["unit tests"],
  "reasoning": "The commits demonstrate a complete OAuth implementation with GitHub..."
}
```

**Pass Threshold**: `scope_match > 0.75`

**Prompt Strategy**: Structured few-shot prompt with explicit JSON output format enforcement.

---

## Agent 3: Dike — Quality Analyzer

**Role**: Assess code quality, documentation, and implementation completeness.

**Model**: Claude Haiku (via Anthropic API)

**Inputs**:
- Changed file contents (sampled, up to 50KB)
- Commit messages
- PR descriptions

**Process**:
1. Sample up to 10 representative changed files
2. Check for: type annotations, docstrings, test coverage indicators, error handling
3. LLM-score the overall quality

**Output Schema**:
```json
{
  "quality_score": 0.78,
  "risks": [
    "No unit tests found for authentication module",
    "Missing error handling in API client"
  ],
  "strengths": [
    "Consistent type annotations",
    "Clear commit messages"
  ],
  "has_tests": false,
  "has_documentation": true
}
```

**Pass Threshold**: `quality_score > 0.65`

---

## Agent 4: Chronos — Deadline Verifier

**Role**: Confirm the milestone was submitted on time.

**Inputs**:
- Milestone deadline (UTC)
- Submission timestamp (UTC)

**Process**:
1. Compare submission time to deadline
2. Calculate lateness in hours (negative = early)
3. Check if last commit predates deadline

**Output Schema**:
```json
{
  "on_time": true,
  "deadline": "2026-07-01T23:59:59Z",
  "submitted_at": "2026-07-01T18:32:00Z",
  "lateness_hours": -5.47,
  "last_commit_before_deadline": true
}
```

**Note**: Chronos result is advisory. Late submission reduces confidence score but does not automatically block payment. Final policy is configurable per-project.

---

## Agent 5: Kratos — Consensus Engine

**Role**: Aggregate all agent outputs into a final approval decision.

**Inputs**:
- Argus output
- Themis output
- Dike output
- Chronos output

**Consensus Rules**:
```python
approved = (
    argus.confidence > 0.70
    and themis.scope_match > 0.75
    and dike.quality_score > 0.65
)
```

**Output Schema**:
```json
{
  "approved": true,
  "overall_score": 0.83,
  "argus_passed": true,
  "themis_passed": true,
  "dike_passed": true,
  "chronos_on_time": true,
  "reasoning": "All three primary agents passed their thresholds. Strong evidence of work, scope alignment, and quality.",
  "escrow_release_recommended": true,
  "timestamp": "2026-07-01T18:35:00Z"
}
```

**Escrow Trigger**: If `approved = true` AND `chronos.on_time = true` (or late penalty waived by client), escrow release is initiated.

---

## Future Agents (Not Building Now)

### Nemesis — Dispute Resolver
Handles appeals when a developer contests a rejection. Uses adversarial prompting to re-evaluate evidence with stricter scrutiny.

### Plutus — Streaming Payments
Monitors continuous work streams and releases micropayments based on incremental progress rather than milestone-level approval.

---

## Agent Configuration

All agent thresholds are configurable at the project level:

```python
class AgentConfig(BaseModel):
    argus_confidence_threshold: float = 0.70
    themis_scope_threshold: float = 0.75
    dike_quality_threshold: float = 0.65
    chronos_advisory_only: bool = True
    llm_model: str = "claude-haiku-4-5"
    llm_temperature: float = 0.1
```
