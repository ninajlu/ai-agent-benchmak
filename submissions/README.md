# Agent Submissions

This directory contains evaluation results from submitted agents.

## Directory Structure

Each submission should follow:

YYYYMMDD_<agent_name>/
├── metadata.json         # Agent configuration and version info
├── results.json         # Full evaluation results
├── trajectories/        # Detailed logs of agent reasoning
└── README.md           # Documentation

## Required Files

1. **metadata.json**: Agent configuration including:
   - Agent name
   - Version
   - Category (one of):
     - sales_development
     - marketing
     - customer_support
     - business_analyst
     - recruiter
     - general_purpose
   - Architecture description
   - Submission timestamp
   - Contact information

2. **results.json**: Full evaluation results including:
   - Task outcomes
   - Performance metrics
   - LLM judge evaluations

3. **trajectories/**: Directory containing:
   - Reasoning logs
   - Action sequences
   - Task outputs
   - Error logs (if any)

4. **README.md**: Documentation including:
   - Agent description
   - Architecture details
   - Key capabilities
   - Setup instructions
   - Performance summary

## Submission Process

1. Fork this repository
2. Create new directory: YYYYMMDD_<agent_name>
3. Add all required files
4. Submit pull request
5. Request verification

## Verification Status

| Status | Meaning |
|--------|---------|
| ✅ Verified | Results independently confirmed |
| ⏳ Pending | Verification in progress |
| ❌ Failed | Verification unsuccessful |

## Guidelines

1. Use descriptive agent names
2. Include complete documentation
3. Provide clear setup instructions
4. Follow directory structure exactly
5. Include all required files
6. Request verification after submission

## Support

For questions or issues:
- Create an issue in this repository
- Email: support@example.com

## Current Submissions

See [Leaderboard](/leaderboard) for current rankings. 

## Categories

### Sales Development Representative (SDR)
Agents focused on lead qualification, outreach, and sales pipeline development.
Evaluated on:
- Conversation quality
- Lead qualification accuracy
- Response relevance
- Follow-up strategy

### Marketing
Agents focused on content creation, campaign management, and audience targeting.
Evaluated on:
- Content quality
- Audience targeting
- Campaign strategy
- Creativity

### Customer Support
Agents focused on customer service and issue resolution.
Evaluated on:
- Resolution quality
- Response time
- Empathy
- Accuracy

### Business Analyst
Agents focused on data analysis and business insights.
Evaluated on:
- Insight depth
- Data coverage
- Actionability
- Methodology

### Recruiter
Agents focused on talent acquisition and candidate evaluation.
Evaluated on:
- Candidate matching
- Communication
- Evaluation quality
- Process efficiency

### General Purpose
Agents designed for multiple or other business functions.
Evaluated on:
- Task completion
- Output quality
- Efficiency
- Adaptability 