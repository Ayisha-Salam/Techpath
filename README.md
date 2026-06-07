# TechPath

TechPath is a FastAPI website that helps IT students either explore a domain
directly or complete a 25-question career-interest assessment. The backend
normalizes responses across 20 traits and returns five weighted domain matches.

## Run locally

```powershell
python -m pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000`.

## Test

```powershell
pytest
```

The assessment is an educational guidance tool, not a clinical psychometric
instrument. Recommendations should be combined with projects, mentoring, and
real-world exploration.
