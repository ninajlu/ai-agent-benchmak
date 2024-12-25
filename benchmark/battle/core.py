from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class BattleMode(Enum):
    HEAD_TO_HEAD = "head_to_head"
    TOURNAMENT = "tournament"
    TEAM_BATTLE = "team_battle"

@dataclass
class BattleMetrics:
    leads_converted: int = 0
    response_quality: float = 0.0
    strategy_adaptation: float = 0.0
    resource_efficiency: float = 0.0

class AgentBattle:
    """Manages competitive agent evaluations"""
    
    def __init__(self, 
                 category: str,
                 max_rounds: int = 10,
                 environment: str = "competitive"):
        self.category = category
        self.max_rounds = max_rounds
        self.environment = environment
        self.agents: Dict[str, Any] = {}
        
    def register_agent(self, agent_id: str, agent: Any):
        """Register an agent for battle"""
        self.agents[agent_id] = agent
        
    async def run_competition(self, 
                            data_source: Any,
                            metrics: List[str]) -> Dict[str, Any]:
        """Run head-to-head competition"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "category": self.category,
            "rounds": [],
            "final_scores": {}
        }
        
        for round_num in range(self.max_rounds):
            round_results = await self._run_round(
                round_num=round_num,
                data_source=data_source,
                metrics=metrics
            )
            results["rounds"].append(round_results)
            
        results["final_scores"] = self._calculate_final_scores(results["rounds"])
        return results
    
    async def _run_round(self,
                        round_num: int,
                        data_source: Any,
                        metrics: List[str]) -> Dict[str, Any]:
        """Run a single competition round"""
        round_results = {
            "round": round_num,
            "agent_actions": {},
            "metrics": {}
        }
        
        # Get round data
        data = await data_source.get_data({
            "round": round_num,
            "competitive": True
        })
        
        # Each agent takes action
        for agent_id, agent in self.agents.items():
            action = await agent.act(
                data,
                opponent_actions=round_results["agent_actions"]
                if self.environment == "competitive" else None
            )
            round_results["agent_actions"][agent_id] = action
            
        # Evaluate round
        round_results["metrics"] = await self._evaluate_round(
            round_results["agent_actions"],
            metrics
        )
        
        return round_results
    
    def generate_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate battle report with insights"""
        return {
            "summary": self._generate_summary(results),
            "detailed_metrics": self._analyze_metrics(results),
            "agent_strategies": self._analyze_strategies(results),
            "recommendations": self._generate_recommendations(results)
        } 