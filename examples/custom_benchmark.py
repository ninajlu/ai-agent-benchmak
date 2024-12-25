from benchmark.core import BenchmarkTask
from benchmark.evaluation.criteria_parser import CriteriaParser

async def main():
    # Using default criteria
    default_task = BenchmarkTask(
        name="lead_qualification",
        description="Evaluate agent's ability to qualify leads",
        category="sales_development"
    )
    
    # Adding custom criteria
    custom_task = BenchmarkTask(
        name="lead_qualification",
        description="Evaluate agent's ability to qualify leads",
        category="sales_development",
        custom_criteria="""
        Additional evaluation criteria:
        - Industry-specific knowledge in manufacturing
        - Use of our custom qualification framework
        - Integration with our CRM workflow
        - Compliance with regional sales regulations
        """
    )
    
    # Initialize parser and tasks
    parser = CriteriaParser(your_llm_client)
    await default_task.initialize(parser)
    await custom_task.initialize(parser)
    
    # Compare criteria
    print("Default Criteria:")
    for c in default_task.criteria:
        print(f"- {c.name}: {c.description}")
        
    print("\nCustomized Criteria:")
    for c in custom_task.criteria:
        print(f"- {c.name}: {c.description}")

if __name__ == "__main__":
    asyncio.run(main()) 