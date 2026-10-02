# Build Status

## Local validation performed in the build environment

- Python syntax/bytecode compilation: PASS
- Deterministic unit tests: **8 passed**
- Policy count: **17 SOPs**
- Policy categories: **6**
- Deterministic evals: PASS for clear match, cross-category match, cycling paraphrases, fuzzy picnic variants, session-context fuzzy picnic, high wind, no-SOP, prompt injection, policy count/categories, and session follow-up
- Simulated weather API failure: PASS
- Live severe-weather eval: **NOT RUN** in this environment because outbound network access was unavailable; the runner is designed to perform this check when run in a networked environment.

## Dependency installation note

The build environment did not permit downloading missing third-party packages from PyPI, so the complete LangGraph/Streamlit runtime was not executed here. The repository includes the required pinned-by-range dependencies in `requirements.txt`; run `pip install -r requirements.txt` in a normal networked environment before starting the app.
