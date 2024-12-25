from flask import Flask, render_template, request, jsonify
from benchmark.evaluation.criteria_parser import CriteriaParser
from benchmark.defaults.evaluation_criteria import BenchmarkDefaults
from benchmark.core import BenchmarkRunner
from benchmark.sources import get_available_sources

app = Flask(__name__)

@app.route('/')
def index():
    """Main configuration page"""
    return render_template('index.html',
        categories=AGENT_CATEGORIES,
        data_sources=get_available_sources()
    )

@app.route('/api/criteria/<category>')
def get_criteria(category):
    """Get default criteria for category"""
    return jsonify({
        'default_criteria': BenchmarkDefaults.get_criteria(category)
    })

@app.route('/api/parse_criteria', methods=['POST'])
def parse_criteria():
    """Parse and preview custom criteria"""
    criteria_text = request.json.get('criteria')
    parser = CriteriaParser(request.json.get('llm_config'))
    parsed = parser.parse_criteria(criteria_text)
    return jsonify(parsed)

@app.route('/api/run_benchmark', methods=['POST'])
def run_benchmark():
    """Run benchmark with provided configuration"""
    config = request.json
    
    try:
        runner = BenchmarkRunner(
            data_sources=_setup_data_sources(config['data_sources']),
            category=config['category'],
            evaluation_criteria=config['criteria'],
            mode=config.get('mode', 'standard')
        )
        
        results = runner.run_benchmark(config['agent_url'])
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

AGENT_CATEGORIES = [
    {
        'id': 'sales_development',
        'name': 'Sales Development',
        'description': 'Evaluate SDR agent capabilities'
    },
    {
        'id': 'marketing',
        'name': 'Marketing',
        'description': 'Test marketing automation agents'
    },
    {
        'id': 'customer_support',
        'name': 'Customer Support',
        'description': 'Assess support agent performance'
    },
    {
        'id': 'business_analyst',
        'name': 'Business Analyst',
        'description': 'Evaluate analytical capabilities'
    },
    {
        'id': 'recruiter',
        'name': 'Recruiter',
        'description': 'Test recruitment agent skills'
    },
    {
        'id': 'general_purpose',
        'name': 'General Purpose',
        'description': 'Evaluate general AI capabilities'
    }
]

def _setup_data_sources(configs):
    """Initialize data sources from configs"""
    sources = []
    for source_type, config in configs.items():
        if source_type == 'salesforce':
            from benchmark.sources.salesforce import SalesforceDataSource
            sources.append(SalesforceDataSource(config))
        elif source_type == 'hubspot':
            from benchmark.sources.hubspot import HubspotDataSource
            sources.append(HubspotDataSource(config))
        elif source_type == 'gmail':
            from benchmark.sources.google import GmailDataSource
            sources.append(GmailDataSource(config))
        elif source_type == 'google_drive':
            from benchmark.sources.google import GoogleDriveDataSource
            sources.append(GoogleDriveDataSource(config))
        elif source_type == 'slack':
            from benchmark.sources.slack import SlackDataSource
            sources.append(SlackDataSource(config))
        elif source_type == 'synthetic':
            from benchmark.sources.synthetic import SyntheticDataSource
            sources.append(SyntheticDataSource(config))
    return sources

if __name__ == '__main__':
    app.run(debug=True) 