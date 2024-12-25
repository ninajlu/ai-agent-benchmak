from typing import Dict, Any

DEFAULT_CRITERIA = {
    "sales_development": """
    Evaluate SDR agent performance on:
    - Conversation Quality: Natural dialogue flow, appropriate responses, understanding context
    - Lead Qualification: Accurate BANT assessment, identifying decision makers, pain points
    - Response Relevance: Addressing specific customer needs, staying on topic
    - Follow-up Strategy: Timing, persistence, multi-channel approach
    - Sales Process: Following methodology, moving leads through pipeline
    - Objection Handling: Identifying and addressing concerns effectively
    """,

    "marketing": """
    Evaluate marketing agent performance on:
    - Content Quality: Clarity, engagement, brand voice consistency
    - Audience Targeting: Understanding demographics, personalization
    - Campaign Strategy: Goal alignment, channel selection, timing
    - Creativity: Unique approaches, innovative ideas
    - Brand Consistency: Message alignment, visual guidelines
    - Performance Analysis: Metric interpretation, optimization suggestions
    """,

    "customer_support": """
    Evaluate support agent performance on:
    - Resolution Quality: Complete and accurate problem solving
    - Response Time: Speed of initial and follow-up responses
    - Empathy: Understanding customer frustration, appropriate tone
    - Technical Accuracy: Correct solutions, product knowledge
    - Process Adherence: Following support protocols
    - Documentation: Ticket details, solution recording
    """,

    "business_analyst": """
    Evaluate analyst agent performance on:
    - Insight Depth: Meaningful patterns, actionable findings
    - Data Coverage: Comprehensive analysis, relevant data sources
    - Methodology: Appropriate analytical approaches
    - Actionability: Clear recommendations, business impact
    - Communication: Clear presentation of findings
    - Technical Rigor: Statistical validity, data quality
    """,

    "recruiter": """
    Evaluate recruiter agent performance on:
    - Candidate Matching: Skills alignment, culture fit assessment
    - Communication: Clear, professional interactions
    - Evaluation Quality: Thorough candidate assessment
    - Process Efficiency: Time-to-fill, candidate pipeline
    - Compliance: Following hiring regulations, documentation
    - Candidate Experience: Professional treatment, timely updates
    """,

    "general_purpose": """
    Evaluate general agent performance on:
    - Task Completion: Meeting objectives, accuracy
    - Output Quality: Thoroughness, correctness
    - Efficiency: Time and resource usage
    - Adaptability: Handling various tasks
    - Communication: Clear interaction style
    - Problem Solving: Approach to challenges
    """
}

class BenchmarkDefaults:
    @staticmethod
    def get_criteria(category: str) -> str:
        """Get default evaluation criteria for a category"""
        return DEFAULT_CRITERIA.get(category, DEFAULT_CRITERIA["general_purpose"])
    
    @staticmethod
    def create_custom_criteria(base_criteria: str, custom_criteria: str) -> str:
        """Merge default criteria with custom company criteria"""
        return f"""
        Standard Evaluation Criteria:
        {base_criteria}
        
        Company-Specific Criteria:
        {custom_criteria}
        """ 