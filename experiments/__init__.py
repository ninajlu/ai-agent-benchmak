from typing import Dict, Any
import json
import os

class ExperimentRegistry:
    """Registry for tracking agent submissions and results"""
    
    def __init__(self, storage_path: str = "submissions"):
        self.storage_path = storage_path
        
    def register_submission(self, 
                          agent_name: str,
                          metadata: Dict[str, Any],
                          results: Dict[str, Any]) -> str:
        """Register a new agent submission"""
        # Generate submission ID
        submission_id = f"{datetime.now().strftime('%Y%m%d')}_{agent_name}"
        
        # Create submission directory
        submission_path = os.path.join(self.storage_path, submission_id)
        os.makedirs(submission_path, exist_ok=True)
        
        # Save metadata and results
        with open(os.path.join(submission_path, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)
            
        with open(os.path.join(submission_path, "results.json"), "w") as f:
            json.dump(results, f, indent=2)
            
        return submission_id 