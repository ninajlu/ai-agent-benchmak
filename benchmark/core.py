from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import logging
import json
from benchmark.evaluation.criteria_parser import CriteriaParser
from benchmark.defaults.evaluation_criteria import BenchmarkDefaults
from benchmark.battle.core import AgentBattle

class DataSource(ABC):
    """Abstract base class for data sources (synthetic or SaaS)"""
    
    @abstractmethod
    async def initialize(self):
        """Initialize the data source"""
        pass
    
    @abstractmethod
    async def get_data(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve data from the source"""
        pass

class BenchmarkTask(ABC):
    """Abstract base class for benchmark tasks"""
    
    def __init__(self, 
                 name: str, 
                 description: str, 
                 category: str,
                 custom_criteria: str = None):
        self.name = name
        self.description = description
        self.category = category
        
        # Get default criteria and optionally merge with custom
        base_criteria = BenchmarkDefaults.get_criteria(category)
        self.criteria_text = (
            BenchmarkDefaults.create_custom_criteria(base_criteria, custom_criteria)
            if custom_criteria else base_criteria
        )
        self.criteria = None
        
    async def initialize(self, criteria_parser: CriteriaParser):
        """Initialize task including parsing evaluation criteria"""
        self.criteria = await criteria_parser.parse_criteria(self.criteria_text)
        
    async def evaluate(self, results: Dict[str, Any], judge_llm) -> Dict[str, Any]:
        """Evaluate task results using LLM judge and parsed criteria"""
        
        # Generate evaluation prompt
        prompt = await self.criteria_parser.generate_judge_prompt(self.criteria)
        prompt += f"\n\nResults to evaluate:\n{results}"
        
        # Get scores from judge
        evaluation = await judge_llm.evaluate(prompt)
        
        # Weight scores
        weighted_scores = {}
        for criterion in self.criteria:
            score = evaluation[criterion.name]
            weighted_scores[criterion.name] = score * criterion.weight
            
        return weighted_scores

class BenchmarkRunner:
    """Main class for running benchmarks"""
    
    def __init__(self, 
                 data_sources: List[DataSource],
                 tasks: List[BenchmarkTask],
                 judge_llm,
                 mode: str = "standard",
                 logger: Optional[logging.Logger] = None):
        self.data_sources = data_sources
        self.tasks = tasks
        self.judge_llm = judge_llm
        self.mode = mode
        self.logger = logger or logging.getLogger(__name__)
        
        # Initialize battle system if needed
        if mode in ["battle", "team_battle"]:
            self.battle_system = AgentBattle(
                category=tasks[0].category if tasks else "general"
            )
        
    async def run_benchmark(self, agent) -> Dict[str, Any]:
        """Run full benchmark suite"""
        results = {
            "agent_id": agent.id,
            "timestamp": datetime.now().isoformat(),
            "tasks": []
        }
        
        # Initialize all data sources
        for ds in self.data_sources:
            await ds.initialize()
            
        # Run each task
        for task in self.tasks:
            try:
                task_result = await task.run(agent, {"data_sources": self.data_sources})
                evaluation = await task.evaluate(task_result, self.judge_llm)
                
                results["tasks"].append({
                    "task_name": task.name,
                    "result": task_result,
                    "evaluation": evaluation
                })
                
            except Exception as e:
                self.logger.error(f"Error in task {task.name}: {str(e)}")
                results["tasks"].append({
                    "task_name": task.name,
                    "error": str(e)
                })
                
        return results 