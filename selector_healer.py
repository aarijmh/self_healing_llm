import json
import requests
from playwright.sync_api import Page
from typing import List, Dict, Optional

class SelectorHealer:
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        
    def heal_selector(self, page: Page, failed_selector: str, step_description: str, 
                     alternative_selectors: List[str] = None) -> Optional[str]:
        """Main method to heal a failed selector"""
        
        # Get page context
        dom_context = self._get_dom_context(page, failed_selector)
        
        # Prepare prompt for Ollama
        prompt = self._create_healing_prompt(failed_selector, step_description, 
                                           dom_context, alternative_selectors)
        
        # Get suggestion from Ollama
        suggested_selector = self._query_ollama(prompt)
        
        # Validate the suggested selector
        if suggested_selector and self._validate_selector(page, suggested_selector):
            return suggested_selector
            
        return None
    
    def _get_dom_context(self, page: Page, failed_selector: str) -> str:
        """Extract relevant DOM context around the failed selector area"""
        try:
            # Get page HTML and find similar elements
            html = page.content()
            
            # Extract body content (simplified)
            body_start = html.find('<body')
            body_end = html.find('</body>') + 7
            if body_start != -1 and body_end != -1:
                body_content = html[body_start:body_end]
                # Limit size for LLM
                return body_content[:8000] if len(body_content) > 8000 else body_content
            
            return html[:8000]
        except:
            return ""
    
    def _create_healing_prompt(self, failed_selector: str, step_description: str, 
                              dom_context: str, alternatives: List[str] = None) -> str:
        """Create a structured prompt for Ollama"""
        
        alternatives_text = ""
        if alternatives:
            alternatives_text = f"\nAlternative selectors that were provided: {alternatives}"
        
        return f"""You are a web automation expert. A Playwright selector has failed and needs healing.

FAILED SELECTOR: {failed_selector}
STEP DESCRIPTION: {step_description}
{alternatives_text}

DOM CONTEXT:
{dom_context}

Analyze the DOM and suggest the BEST selector that would work for this step. Consider:
1. Element stability (avoid dynamic IDs/classes)
2. Uniqueness 
3. Semantic meaning

Respond with ONLY the selector string, no explanation. Examples:
- [data-testid="submit-button"]
- button:has-text("Submit")
- .form-container >> input[type="email"]
"""

    def _query_ollama(self, prompt: str, model: str = "llama3.2") -> Optional[str]:
        """Send prompt to Ollama and get response"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
                
        except Exception as e:
            print(f"Ollama query failed: {e}")
            
        return None
    
    def _validate_selector(self, page: Page, selector: str) -> bool:
        """Test if the suggested selector works"""
        try:
            element = page.locator(selector).first
            return element.count() > 0
        except:
            return False