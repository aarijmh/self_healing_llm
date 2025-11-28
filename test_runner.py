import json
from playwright.sync_api import sync_playwright, Page
from selector_healer import SelectorHealer
from typing import Dict, List
import time

class PlaywrightTestRunner:
    def __init__(self, test_file_path: str):
        self.test_file_path = test_file_path
        self.healer = SelectorHealer()
        self.test_data = self._load_test_data()
        
    def _load_test_data(self) -> Dict:
        """Load test case JSON file"""
        with open(self.test_file_path, 'r') as f:
            return json.load(f)
    
    def _save_test_data(self):
        """Save updated test data back to JSON file"""
        with open(self.test_file_path, 'w') as f:
            json.dump(self.test_data, f, indent=2)
    
    def run_test(self):
        """Execute the test with selector healing"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            try:
                # Navigate to start URL
                if 'url' in self.test_data:
                    page.goto(self.test_data['url'])
                
                # Execute each step
                for i, step in enumerate(self.test_data.get('steps', [])):
                    success = self._execute_step(page, step, i)
                    if not success:
                        print(f"Test failed at step {i + 1}")
                        break
                time.sleep(3)    
            finally:
                browser.close()
    
    def _execute_step(self, page: Page, step: Dict, step_index: int) -> bool:
        """Execute a single test step with healing capability"""
        action = step.get('action')
        selectors = step.get('selectors', [])
        description = step.get('description', f"Step {step_index + 1}")
        
        # Try each selector until one works
        for selector in selectors:
            try:
                success = self._perform_action(page, action, selector, step)
                if success:
                    return True
            except Exception as e:
                print(f"Selector failed: {selector} - {e}")
                continue
        
        # All selectors failed - try healing
        print(f"All selectors failed for: {description}")
        healed_selector = self._heal_step(page, step, step_index)
        
        if healed_selector:
            try:
                success = self._perform_action(page, action, healed_selector, step)
                if success:
                    # Update test data with healed selector
                    self.test_data['steps'][step_index]['selectors'].insert(0, healed_selector)
                    self._save_test_data()
                    print(f"✅ Healed selector: {healed_selector}")
                    return True
            except Exception as e:
                print(f"Healed selector also failed: {e}")
        
        return False
    
    def _perform_action(self, page: Page, action: str, selector: str, step: Dict) -> bool:
        """Perform the specified action on the element"""
        element = page.locator(selector).first
        
        if action == 'click':
            element.click()
        elif action == 'fill':
            text = step.get('text', '')
            element.fill(text)
        elif action == 'type':
            text = step.get('text', '')
            element.type(text)
        elif action == 'wait':
            element.wait_for()
        elif action == 'assert_visible':
            assert element.is_visible()
        elif action == 'assert_text':
            expected_text = step.get('expected_text', '')
            assert expected_text in element.text_content()
        else:
            print(f"Unknown action: {action}")
            return False
            
        return True
    
    def _heal_step(self, page: Page, step: Dict, step_index: int) -> str:
        """Attempt to heal a failed step"""
        failed_selectors = step.get('selectors', [])
        description = step.get('description', f"Step {step_index + 1}")
        
        # Use the first selector as the "failed" one for context
        primary_selector = failed_selectors[0] if failed_selectors else ""
        
        return self.healer.heal_selector(
            page=page,
            failed_selector=primary_selector,
            step_description=description,
            alternative_selectors=failed_selectors[1:] if len(failed_selectors) > 1 else None
        )