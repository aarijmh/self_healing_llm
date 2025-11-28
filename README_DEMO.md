# Playwright Test Healing Demo

This demo shows how LLM-powered selector healing works when UI changes break existing test cases.

## Scenario

1. **Original Page**: A contact form with specific IDs and classes
2. **Modified Page**: Same functionality but all selectors changed (simulating a UI refactor)
3. **Test Case**: Works on original page, fails on modified page
4. **Healing**: LLM analyzes DOM and suggests new selectors

## Files Created

- `demo_page_original.html` - Initial form with IDs like `#name`, `#email`, `#submit-btn`
- `demo_page_modified.html` - Refactored form with new classes and data attributes
- `demo_test.json` - Test case that fills form and verifies success
- `healing_demo.py` - Orchestrates the demo showing failure and healing
- `simple_server.py` - HTTP server to serve demo pages
- `run_demo.py` - Complete demo runner

## Prerequisites

1. **Ollama running**: `ollama serve`
2. **Python dependencies**: `pip install playwright requests`
3. **Playwright browsers**: `playwright install`

## Running the Demo

```bash
# Start the complete demo
python run_demo.py
```

Or run components separately:

```bash
# Start server only
python simple_server.py

# Run healing demo (server must be running)
python healing_demo.py
```

## What You'll See

1. **Step 1**: Test runs successfully on original page
2. **Step 2**: Test switches to modified page, selectors fail
3. **Step 3**: LLM analyzes DOM and heals selectors
4. **Step 4**: Test continues with new selectors and passes

## Key Changes Demonstrated

| Original Selector | Modified Page Element | Healed Selector (LLM suggests) |
|-------------------|----------------------|--------------------------------|
| `#name` | `data-field="name"` | `[data-field="name"]` |
| `#email` | `data-field="email"` | `[data-field="email"]` |
| `#submit-btn` | `data-testid="send-button"` | `[data-testid="send-button"]` |
| `#success-msg` | `data-testid="success-message"` | `[data-testid="success-message"]` |

The LLM analyzes the DOM context and suggests robust selectors that work with the new page structure.