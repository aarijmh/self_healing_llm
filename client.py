import requests
import json
import time
from typing import Dict, List, Optional

class SelectorHealerClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def run_test(self, test_case: Dict) -> Dict:
        """Submit test for execution and wait for completion"""
        # Start test
        response = requests.post(f"{self.base_url}/test/run", json=test_case)
        response.raise_for_status()
        
        job_data = response.json()
        job_id = job_data["job_id"]
        
        # Poll for completion
        while True:
            status_response = requests.get(f"{self.base_url}/job/{job_id}")
            status_response.raise_for_status()
            
            status = status_response.json()
            
            if status["status"] == "completed":
                return status["result"]
            elif status["status"] == "failed":
                raise Exception(f"Test failed: {status['error']}")
            
            time.sleep(1)
    
    def heal_selector(self, url: str, failed_selector: str, 
                     description: str, alternatives: Optional[List[str]] = None) -> str:
        """Heal a single selector"""
        payload = {
            "url": url,
            "failed_selector": failed_selector,
            "description": description,
            "alternatives": alternatives
        }
        
        response = requests.post(f"{self.base_url}/heal", json=payload)
        response.raise_for_status()
        
        return response.json()["healed_selector"]

# Example usage
if __name__ == "__main__":
    client = SelectorHealerClient()
    
    # Load test case
    with open("example_test.json", "r") as f:
        test_case = json.load(f)
    
    # Run test
    result = client.run_test(test_case)
    print("Updated test case:", json.dumps(result, indent=2))