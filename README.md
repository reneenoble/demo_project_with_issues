# demo_project_with_issues

A Python demo repository for **issue complexity analysis**.

This project models a community sharing platform where members can share books, equipment, and vegetables. It includes:
- lightweight SSO token validation
- donation/request models
- a greedy matching engine
- a small FastAPI-ready app module (`community_share.main`)
- a curated issue backlog with mixed complexity

## Project layout

- `src/community_share/models.py` - domain models
- `src/community_share/auth.py` - SSO validation helper
- `src/community_share/services.py` - matching algorithm
- `src/community_share/main.py` - API entrypoint (FastAPI if installed)
- `issues/seed_issues.json` - issue dataset for analyzer testing
- `scripts/create_issue_commands.py` - generates `gh issue create` commands

## Run tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -p "test_*.py" -v
```

## Optional: run API app

```bash
pip install fastapi uvicorn
PYTHONPATH=src uvicorn community_share.main:app --reload
```

## Seed GitHub issues

Generate commands:

```bash
python scripts/create_issue_commands.py
```

Then run the generated `gh issue create ...` commands in a shell authenticated to this repository.
