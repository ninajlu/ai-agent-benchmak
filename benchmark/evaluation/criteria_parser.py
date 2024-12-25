from typing import Dict, Any, List
import json
from dataclasses import dataclass

@dataclass
class EvaluationCriteria:
    name: str
    description: str
    scoring_guide: str
    weight: float = 1.0
    min_score: int = 1
    max_score: int = 10

class CriteriaParser:
    """Converts natural language evaluation criteria into structured format"""
    
    def __init__(self, llm_client):
        self.llm = llm_client
        
    async def parse_criteria(self, criteria_text: str) -> List[EvaluationCriteria]:
        """Parse natural language criteria into structured format"""
        
        prompt = f"""
        Convert the following evaluation criteria into specific, measurable criteria.
        For each criterion:
        1. Extract the main metric name
        2. Create a clear description
        3. Provide a specific scoring guide (1-10 scale)
        4. Suggest an appropriate weight (0.5-2.0)

        Evaluation Criteria:
        {criteria_text}

        Format as JSON:
        {{
            "criteria": [
                {{
                    "name": "metric_name",
                    "description": "clear description",
                    "scoring_guide": "how to score 1-10",
                    "weight": float
                }},
                ...
            ]
        }}
        """
        
        response = await self.llm.generate(prompt)
        parsed = json.loads(response)
        
        return [
            EvaluationCriteria(**criterion)
            for criterion in parsed["criteria"]
        ]

    async def generate_judge_prompt(self, criteria: List[EvaluationCriteria]) -> str:
        """Generate LLM judge prompt from criteria"""
        
        prompt_parts = [
            "Evaluate the following based on these criteria:\n"
        ]
        
        for c in criteria:
            prompt_parts.append(f"""
            {c.name} (weight: {c.weight})
            Description: {c.description}
            Scoring: {c.scoring_guide}
            """)
            
        return "\n".join(prompt_parts) 