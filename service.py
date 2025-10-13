from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import uuid
from test_runner import PlaywrightTestRunner
from selector_healer import SelectorHealer
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI(title="Playwright Selector Healer Service")

# In-memory job storage (use Redis/DB for production)
jobs = {}

class TestStep(BaseModel):
    description: str
    action: str
    text: Optional[str] = None
    expected_text: Optional[str] = None
    selectors: List[str]

class TestCase(BaseModel):
    name: str
    url: str
    steps: List[TestStep]

class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str

class JobStatus(BaseModel):
    job_id: str
    status: str
    result: Optional[Dict] = None
    error: Optional[str] = None

executor = ThreadPoolExecutor(max_workers=4)

def run_test_sync(test_data: dict, job_id: str):
    """Run test synchronously in thread"""
    try:
        # Create temp file
        temp_file = f"/tmp/test_{job_id}.json"
        with open(temp_file, 'w') as f:
            json.dump(test_data, f)
        
        runner = PlaywrightTestRunner(temp_file)
        runner.run_test()
        
        # Load updated data
        with open(temp_file, 'r') as f:
            updated_data = json.load(f)
        
        jobs[job_id] = {
            "status": "completed",
            "result": updated_data
        }
    except Exception as e:
        jobs[job_id] = {
            "status": "failed",
            "error": str(e)
        }

@app.post("/test/run", response_model=JobResponse)
async def run_test(test_case: TestCase, background_tasks: BackgroundTasks):
    """Execute test case with selector healing"""
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "running"}
    
    test_data = test_case.dict()
    background_tasks.add_task(run_test_sync, test_data, job_id)
    
    return JobResponse(
        job_id=job_id,
        status="running",
        message="Test execution started"
    )

@app.get("/job/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get job execution status"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_data = jobs[job_id]
    return JobStatus(
        job_id=job_id,
        status=job_data["status"],
        result=job_data.get("result"),
        error=job_data.get("error")
    )

@app.post("/heal")
async def heal_selector(
    url: str,
    failed_selector: str,
    description: str,
    alternatives: Optional[List[str]] = None
):
    """Heal a single selector without running full test"""
    try:
        from playwright.sync_api import sync_playwright
        
        healer = SelectorHealer()
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            
            healed = healer.heal_selector(
                page, failed_selector, description, alternatives
            )
            
            browser.close()
            
        return {"healed_selector": healed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Service health check"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)