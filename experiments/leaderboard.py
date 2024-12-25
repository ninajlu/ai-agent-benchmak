from typing import List, Dict, Any
import json
import os
from datetime import datetime
from enum import Enum

class AgentCategory(Enum):
    SDR = "sales_development"
    MARKETER = "marketing"
    SUPPORT = "customer_support"
    ANALYST = "business_analyst"
    RECRUITER = "recruiter"
    GENERAL = "general_purpose"

class Leaderboard:
    """Manages agent rankings and leaderboard by category"""
    
    def __init__(self, storage_path: str = "submissions"):
        self.storage_path = storage_path
        
    def get_rankings(self, category: AgentCategory = None) -> List[Dict[str, Any]]:
        """Get current agent rankings, optionally filtered by category"""
        rankings = []
        
        for submission_id in os.listdir(self.storage_path):
            submission_path = os.path.join(self.storage_path, submission_id)
            
            if not os.path.isdir(submission_path):
                continue
                
            try:
                # Load metadata
                with open(os.path.join(submission_path, "metadata.json")) as f:
                    metadata = json.load(f)
                    
                # Skip if category doesn't match
                if category and metadata.get("category") != category.value:
                    continue
                    
                # Load results    
                with open(os.path.join(submission_path, "results.json")) as f:
                    results = json.load(f)
                    
                # Check verification status
                verification_path = os.path.join(submission_path, "verification.json")
                verified = os.path.exists(verification_path)
                if verified:
                    with open(verification_path) as f:
                        verification = json.load(f)
                        verified = verification["passed"]
                
                rankings.append({
                    "submission_id": submission_id,
                    "agent_name": metadata["agent_name"],
                    "category": metadata["category"],
                    "submitted_at": metadata["submitted_at"],
                    "score": self._calculate_category_score(results, metadata["category"]),
                    "verified": verified,
                    "task_count": len(results["tasks"])
                })
                
            except Exception as e:
                print(f"Error loading submission {submission_id}: {e}")
                continue
                
        # Sort by score
        rankings.sort(key=lambda x: x["score"], reverse=True)
        return rankings

    def _calculate_category_score(self, results: Dict[str, Any], category: str) -> float:
        """Calculate score based on category-specific metrics"""
        scores = []
        
        for task in results["tasks"]:
            if "evaluation" in task:
                # Weight different metrics based on category
                weights = self._get_category_weights(category)
                weighted_score = sum(
                    score * weights.get(metric, 1.0)
                    for metric, score in task["evaluation"].items()
                )
                scores.append(weighted_score / sum(weights.values()))
                
        return sum(scores) / len(scores) if scores else 0

    def _get_category_weights(self, category: str) -> Dict[str, float]:
        """Get metric weights for different categories"""
        weights = {
            "sales_development": {
                "conversation_quality": 2.0,
                "lead_qualification": 2.0,
                "response_relevance": 1.5,
                "follow_up_strategy": 1.5
            },
            "marketing": {
                "content_quality": 2.0,
                "audience_targeting": 2.0,
                "campaign_strategy": 1.5,
                "creativity": 1.5
            },
            "customer_support": {
                "resolution_quality": 2.0,
                "response_time": 1.5,
                "empathy": 2.0,
                "accuracy": 1.5
            },
            "business_analyst": {
                "insight_depth": 2.0,
                "data_coverage": 1.5,
                "actionability": 2.0,
                "methodology": 1.5
            },
            "recruiter": {
                "candidate_matching": 2.0,
                "communication": 1.5,
                "evaluation_quality": 2.0,
                "process_efficiency": 1.5
            },
            "general_purpose": {
                "task_completion": 1.0,
                "output_quality": 1.0,
                "efficiency": 1.0,
                "adaptability": 1.0
            }
        }
        return weights.get(category, weights["general_purpose"])
        
    def get_submission_details(self, submission_id: str) -> Dict[str, Any]:
        """Get detailed results for a submission"""
        submission_path = os.path.join(self.storage_path, submission_id)
        
        with open(os.path.join(submission_path, "metadata.json")) as f:
            metadata = json.load(f)
            
        with open(os.path.join(submission_path, "results.json")) as f:
            results = json.load(f)
            
        verification_path = os.path.join(submission_path, "verification.json")
        verification = None
        if os.path.exists(verification_path):
            with open(verification_path) as f:
                verification = json.load(f)
                
        return {
            "metadata": metadata,
            "results": results,
            "verification": verification
        } 