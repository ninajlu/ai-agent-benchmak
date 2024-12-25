from benchmark.core import BenchmarkRunner
from benchmark.sources.synthetic import SyntheticDataSource
from benchmark.sources.salesforce import SalesforceDataSource
from benchmark.tasks.sales_analysis import SalesAnalysisTask
import asyncio

async def main():
    # Set up data sources
    synthetic = SyntheticDataSource({
        "employee_count": 200,
        "num_opportunities": 300
    })
    
    salesforce = SalesforceDataSource({
        "username": "test@example.com",
        "password": "password123",
        "security_token": "token123",
        "domain": "test"
    })
    
    # Create tasks
    tasks = [
        SalesAnalysisTask()
    ]
    
    # Initialize benchmark runner
    runner = BenchmarkRunner(
        data_sources=[synthetic, salesforce],
        tasks=tasks,
        judge_llm=your_llm_client
    )
    
    # Run benchmark
    results = await runner.run_benchmark(your_agent)
    
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    asyncio.run(main()) 