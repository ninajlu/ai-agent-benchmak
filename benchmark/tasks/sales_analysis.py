from benchmark.core import BenchmarkTask

class SalesAnalysisTask(BenchmarkTask):
    def __init__(self):
        super().__init__(
            name="sales_analysis",
            description="Analyze sales data and provide recommendations"
        )
        
    async def run(self, agent, context: Dict[str, Any]) -> Dict[str, Any]:
        # Get sales data from available sources
        sales_data = []
        for source in context["data_sources"]:
            try:
                data = await source.get_data({"type": "sales"})
                sales_data.extend(data)
            except:
                continue
                
        # Have agent analyze the data
        analysis = await agent.analyze(
            data=sales_data,
            prompt="Analyze the sales data and provide strategic recommendations"
        )
        
        return {
            "analysis": analysis,
            "data_points": len(sales_data)
        }
        
    async def evaluate(self, results: Dict[str, Any], judge_llm) -> Dict[str, Any]:
        # Have LLM judge evaluate the analysis
        evaluation = await judge_llm.evaluate(
            prompt=f"""
            Evaluate the following sales analysis. Consider:
            1. Depth of insights
            2. Actionability of recommendations
            3. Data coverage
            
            Analysis: {results['analysis']}
            """,
            criteria={
                "insight_depth": "Score 1-10",
                "actionability": "Score 1-10", 
                "data_coverage": "Score 1-10"
            }
        )
        
        return evaluation 