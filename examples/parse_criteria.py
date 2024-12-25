from benchmark.evaluation.criteria_parser import CriteriaParser

async def main():
    parser = CriteriaParser(your_llm_client)
    
    # Company provides criteria in natural language
    criteria_text = """
    We want to evaluate our SDR agents on:
    - How well they understand and respond to customer needs
    - Their ability to accurately qualify leads
    - Professional communication style
    - Follow-up persistence and timing
    - Use of our sales methodology
    """
    
    # Parse into structured criteria
    criteria = await parser.parse_criteria(criteria_text)
    
    # Example output:
    # [
    #     EvaluationCriteria(
    #         name="customer_understanding",
    #         description="Ability to comprehend and address customer needs and pain points",
    #         scoring_guide="1: No understanding shown, 5: Basic needs addressed, 10: Deep understanding demonstrated",
    #         weight=2.0
    #     ),
    #     EvaluationCriteria(
    #         name="lead_qualification",
    #         description="Accuracy in qualifying leads against BANT criteria",
    #         scoring_guide="1: No qualification, 5: Basic qualification, 10: Thorough BANT qualification",
    #         weight=1.8
    #     ),
    #     ...
    # ]
    
    # Generate judge prompt
    judge_prompt = await parser.generate_judge_prompt(criteria)
    
    print("Structured Criteria:")
    for c in criteria:
        print(f"\n{c.name} (weight: {c.weight})")
        print(f"Description: {c.description}")
        print(f"Scoring: {c.scoring_guide}")
        
    print("\nJudge Prompt:")
    print(judge_prompt)

if __name__ == "__main__":
    asyncio.run(main()) 