import streamlit as st
from typing import Dict, Any
import yaml
from benchmark.evaluation.criteria_parser import CriteriaParser
from benchmark.defaults.evaluation_criteria import BenchmarkDefaults
from benchmark.core import BenchmarkRunner
from benchmark.sources import get_available_sources

class BenchmarkUI:
    def __init__(self):
        st.set_page_config(
            page_title="AI Agent Benchmark Configuration",
            layout="wide"
        )
        self.criteria_parser = CriteriaParser(st.session_state.get('llm_client'))
        
    def render(self):
        st.title("AI Agent Benchmark Configuration")
        
        # Sidebar for global settings
        with st.sidebar:
            self._render_sidebar()
            
        # Main content in tabs
        tab1, tab2, tab3 = st.tabs([
            "1. Agent Category", 
            "2. Data Sources", 
            "3. Evaluation Criteria"
        ])
        
        with tab1:
            self._render_category_selection()
            
        with tab2:
            self._render_data_sources()
            
        with tab3:
            self._render_evaluation_criteria()
            
        # Bottom section for running benchmark
        self._render_run_section()
    
    def _render_sidebar(self):
        st.sidebar.header("Global Settings")
        
        # Environment selection
        st.sidebar.selectbox(
            "Environment",
            ["sandbox", "production"],
            help="Select testing environment"
        )
        
        # Battle mode
        st.sidebar.selectbox(
            "Evaluation Mode",
            ["standard", "battle", "team_battle"],
            help="Choose how to evaluate agents"
        )
        
        # API Keys section
        st.sidebar.subheader("API Keys")
        with st.sidebar.expander("Configure Keys"):
            st.text_input("OpenAI API Key", type="password")
            st.text_input("Salesforce Token", type="password")
            st.text_input("HubSpot API Key", type="password")
    
    def _render_category_selection(self):
        st.header("Select Agent Category")
        
        col1, col2 = st.columns([2,1])
        
        with col1:
            category = st.selectbox(
                "Agent Category",
                [
                    "sales_development",
                    "marketing",
                    "customer_support",
                    "business_analyst",
                    "recruiter",
                    "general_purpose"
                ]
            )
            
        with col2:
            st.metric(
                "Default Criteria Count", 
                len(BenchmarkDefaults.get_criteria(category).split("\n"))
            )
            
        # Show category description
        st.markdown(self._get_category_description(category))
    
    def _render_data_sources(self):
        st.header("Configure Data Sources")
        
        available_sources = get_available_sources()
        
        # Data source selection
        selected_sources = st.multiselect(
            "Select Data Sources",
            available_sources.keys()
        )
        
        # Configuration for each selected source
        for source in selected_sources:
            with st.expander(f"Configure {source}"):
                config = self._render_source_config(
                    source, 
                    available_sources[source]
                )
                st.session_state[f"{source}_config"] = config
    
    def _render_source_config(self, source: str, schema: Dict) -> Dict[str, Any]:
        """Render configuration fields for a data source"""
        config = {}
        
        for field, details in schema.items():
            if details["type"] == "string":
                config[field] = st.text_input(
                    field,
                    help=details.get("description", "")
                )
            elif details["type"] == "number":
                config[field] = st.number_input(
                    field,
                    help=details.get("description", "")
                )
            elif details["type"] == "boolean":
                config[field] = st.checkbox(
                    field,
                    help=details.get("description", "")
                )
                
        return config
    
    def _render_evaluation_criteria(self):
        st.header("Customize Evaluation Criteria")
        
        category = st.session_state.get("category", "general_purpose")
        
        # Show default criteria
        with st.expander("Default Criteria", expanded=True):
            default_criteria = BenchmarkDefaults.get_criteria(category)
            st.code(default_criteria)
        
        # Custom criteria input
        st.subheader("Add Custom Criteria")
        custom_criteria = st.text_area(
            "Enter additional evaluation criteria",
            height=200,
            help="Add your company-specific evaluation criteria"
        )
        
        if custom_criteria:
            if st.button("Preview Parsed Criteria"):
                criteria = self.criteria_parser.parse_criteria(custom_criteria)
                st.json(criteria)
    
    def _render_run_section(self):
        st.markdown("---")
        
        col1, col2 = st.columns([3,1])
        
        with col1:
            st.text_input("Agent Endpoint URL", help="API endpoint for your agent")
            
        with col2:
            if st.button("Run Benchmark", type="primary"):
                self._run_benchmark()
    
    def _run_benchmark(self):
        """Execute benchmark with current configuration"""
        try:
            # Create progress bar
            progress = st.progress(0)
            status = st.empty()
            
            # Get configuration
            config = self._get_current_config()
            
            # Initialize runner
            runner = BenchmarkRunner(**config)
            
            # Run benchmark
            results = runner.run_benchmark(config["agent_url"])
            
            # Show results
            st.json(results)
            
        except Exception as e:
            st.error(f"Error running benchmark: {str(e)}")
    
    def _get_current_config(self) -> Dict[str, Any]:
        """Get current UI configuration"""
        return {
            "category": st.session_state.get("category"),
            "data_sources": self._get_configured_sources(),
            "evaluation_criteria": self._get_evaluation_criteria(),
            "mode": st.session_state.get("mode", "standard"),
            "agent_url": st.session_state.get("agent_url")
        }

if __name__ == "__main__":
    ui = BenchmarkUI()
    ui.render() 