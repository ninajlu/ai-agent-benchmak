from typing import Dict, Any, List
import random
import json
import os
from datetime import datetime

class VerificationRunner:
    """Runs verification checks on submitted results"""
    
    def __init__(self, benchmark_runner, storage_path: str = "submissions"):
        self.benchmark_runner = benchmark_runner
        self.storage_path = storage_path
        
    async def verify_submission(self,
                              submission_id: str,
                              agent,
                              sample_size: int = 3) -> Dict[str, Any]:
        """Verify a submission by re-running subset of tasks"""
        
        # Load submitted results
        results_path = os.path.join(self.storage_path, submission_id, "results.json")
        with open(results_path) as f:
            submitted_results = json.load(f)
            
        # Sample tasks to verify
        tasks = self.benchmark_runner.tasks
        verify_tasks = random.sample(tasks, min(sample_size, len(tasks)))
        
        # Run verification
        verify_results = await self.benchmark_runner.run_benchmark(
            agent,
            tasks=verify_tasks
        )
        
        # Compare results
        comparison = self._compare_results(submitted_results, verify_results)
        
        # Save verification results
        verification = {
            "timestamp": datetime.now().isoformat(),
            "tasks_verified": [t.name for t in verify_tasks],
            "comparison": comparison,
            "passed": comparison["score_diff"] <= 0.1  # Within 10% tolerance
        }
        
        self._save_verification(submission_id, verification)
        
        return verification
        
    def _compare_results(self,
                        submitted: Dict[str, Any],
                        verified: Dict[str, Any]) -> Dict[str, Any]:
        """Compare submitted vs verified results"""
        
        submitted_scores = self._extract_scores(submitted)
        verified_scores = self._extract_scores(verified)
        
        return {
            "submitted_avg": sum(submitted_scores) / len(submitted_scores),
            "verified_avg": sum(verified_scores) / len(verified_scores),
            "score_diff": abs(submitted_scores[0] - verified_scores[0]) / submitted_scores[0],
            "details": {
                "submitted": submitted_scores,
                "verified": verified_scores
            }
        }
        
    def _extract_scores(self, results: Dict[str, Any]) -> List[float]:
        """Extract evaluation scores from results"""
        scores = []
        for task in results["tasks"]:
            if "evaluation" in task:
                scores.append(sum(task["evaluation"].values()) / len(task["evaluation"]))
        return scores
        
    def _save_verification(self, submission_id: str, verification: Dict[str, Any]):
        """Save verification results"""
        path = os.path.join(self.storage_path, submission_id, "verification.json")
        with open(path, "w") as f:
            json.dump(verification, f, indent=2) 