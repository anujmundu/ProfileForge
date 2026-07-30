# Quick Start Guide

Generate a production GitHub profile README and theme-driven SVG cards in under 2 minutes.

---

## 1. Set GitHub Access Token (Optional)

```bash
export GITHUB_TOKEN="ghp_your_personal_access_token"
```

---

## 2. Execute Automated Pipeline

Create a Python script `run.py`:

```python
from profileforge.automation import AutomationOrchestrator, AutomationConfiguration

# Configure output directory
config = AutomationConfiguration(output_dir="./dist", overwrite_existing=True)
orchestrator = AutomationOrchestrator(config=config)

# Run full pipeline for target username
report = orchestrator.execute_workflow(username="octocat")

print(f"Workflow ID: {report.workflow_id}")
print(f"Success: {report.result.success}")
print(f"Artifacts Published: {report.result.publish_result.artifacts_published_count}")
```

Run script:
```bash
python run.py
```

---

## 3. Output Artifacts Created

Check `./dist/`:
- `README.md`: Profile README with statistics and portfolio summary.
- `stats_card.svg`: Theme-driven SVG card displaying repository stars and language metrics.
- `tech_card.svg`: Inferred technology stack SVG card.
- `profileforge.json`: Complete JSON snapshot of presentation model.
