# Playwright Selector Healer with Ollama

Automatically heal broken selectors in Playwright tests using local Ollama LLM.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install
```

2. Start Ollama with a model:
```bash
ollama pull llama3.2
ollama serve
```

## Usage

### CLI (Original)
```bash
python main.py example_test.json
```

### Service Mode
```bash
# Start service
python service.py

# Or with Docker
docker-compose up

# Use client
python client.py
```

### API Endpoints
- `POST /test/run` - Execute test with healing
- `GET /job/{job_id}` - Check job status
- `POST /heal` - Heal single selector
- `GET /health` - Health check

## How it works

1. Test runs with provided selectors
2. If all selectors fail, captures page DOM
3. Sends context to Ollama for analysis
4. Tests suggested selector
5. Updates JSON file with working selector

## Test JSON Format

```json
{
  "name": "Test Name",
  "url": "https://example.com",
  "steps": [
    {
      "description": "Action description",
      "action": "click|fill|type|wait|assert_visible|assert_text",
      "text": "text for fill/type actions",
      "selectors": ["#primary", ".backup", "[data-testid='fallback']"]
    }
  ]
}
```