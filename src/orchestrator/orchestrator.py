import json
import os
import yaml
import google.generativeai as genai
from src.agents.planner import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_generator import CreativeGenerator

class Orchestrator:
    def __init__(self):
        """Initialize orchestrator with all agents and LLM model"""
        # Load config
        self.config = self._load_config("config/config.yaml")
        
        # Initialize LLM model
        self.model = self._initialize_llm()
        
        # Initialize agents with model
        self.planner = PlannerAgent(model=self.model)
        self.data_agent = DataAgent(model=self.model)
        self.insight_agent = InsightAgent(model=self.model)
        self.evaluator = EvaluatorAgent(model=self.model)
        self.creatives = CreativeGenerator(model=self.model)
        
        # Logs
        self.logs = []
    
    def _load_config(self, config_path):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️ Config load failed: {e}. Using defaults.")
            return {
                "llm": {"provider": "google", "model": "gemini-1.5-flash"},
                "data": {"csv_path": "data/synthetic_fb_ads_undergarments.csv"}
            }
    
    def _initialize_llm(self):
        """Initialize LLM model based on config"""
        llm_config = self.config.get("llm", {})
        provider = llm_config.get("provider", "google")
        
        if provider == "google":
            # Get API key from environment
            api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
            if not api_key:
                print("⚠️ GOOGLE_API_KEY not found. Agents will use fallback logic.")
                return None
            
            genai.configure(api_key=api_key)
            model_name = llm_config.get("model", "gemini-1.5-flash")
            return genai.GenerativeModel(model_name)
        
        else:
            print(f"⚠️ Provider {provider} not supported. Using fallback.")
            return None

    def run(self, query):
        """
        Main orchestration loop using Planner-driven execution
        """
        print(f"\n🚀 Starting analysis for query: '{query}'\n")
        
        # Step 1: Generate execution plan using Planner
        print("📋 Step 1: Generating execution plan...")
        plan = self.planner.create_plan(query)
        print(f"✅ Plan created with {len(plan.get('subtasks', []))} subtasks\n")
        self._log("plan_generated", plan)
        
        # Storage for intermediate results
        results = {}
        
        # Step 2: Execute plan subtasks in order
        for subtask in plan.get("subtasks", []):
            task_id = subtask.get("task_id")
            task_desc = subtask.get("task")
            agent_name = subtask.get("agent")
            
            print(f"▶ Task {task_id}: {task_desc} (Agent: {agent_name})")
            
            # Execute appropriate agent based on plan
            if agent_name == "data_agent":
                csv_path = self.config.get("data", {}).get("csv_path", "data/synthetic_fb_ads_undergarments.csv")
                df, summary = self.data_agent.load_and_summarize(csv_path)
                results['dataframe'] = df
                results['data_summary'] = summary
                print(f"  ✓ Loaded {len(df)} rows, {df['campaign_name'].nunique()} campaigns\n")
                self._log("data_loaded", {"rows": len(df), "campaigns": df['campaign_name'].nunique()})
            
            elif agent_name == "insight_agent":
                if 'data_summary' not in results:
                    print("  ⚠️ Skipping: data_summary not available\n")
                    continue
                insights = self.insight_agent.generate_insights(results['data_summary'])
                results['insights'] = insights
                print(f"  ✓ Generated {len(insights)} hypotheses\n")
                self._log("insights_generated", {"count": len(insights)})
            
            elif agent_name == "evaluator_agent":
                if 'dataframe' not in results or 'insights' not in results:
                    print("  ⚠️ Skipping: dataframe or insights not available\n")
                    continue
                validated = self.evaluator.evaluate(results['dataframe'], results['insights'])
                results['validated_insights'] = validated
                print(f"  ✓ Validated {len(validated)} insights (confidence ≥ 0.6)\n")
                self._log("insights_validated", {"count": len(validated)})
            
            elif agent_name == "creative_generator":
                if 'data_summary' not in results:
                    print("  ⚠️ Skipping: data_summary not available\n")
                    continue
                creatives = self.creatives.generate(results['data_summary'])
                results['creatives'] = creatives
                print(f"  ✓ Generated {len(creatives)} creative recommendations\n")
                self._log("creatives_generated", {"count": len(creatives)})

        # Step 3: Save outputs
        print("\n💾 Saving results...")
        self._save_results(results)
        self._save_logs()
        print("✅ Analysis complete!\n")

    def _save_results(self, results):
        """Save JSON and Markdown outputs"""
        os.makedirs("reports", exist_ok=True)
        
        # Save insights.json
        if 'validated_insights' in results:
            with open("reports/insights.json", "w") as f:
                json.dump(results['validated_insights'], f, indent=4)
        
        # Save creatives.json
        if 'creatives' in results:
            with open("reports/creatives.json", "w") as f:
                json.dump(results['creatives'], f, indent=4)
        
        # Save report.md
        self._generate_markdown_report(results)
    
    def _generate_markdown_report(self, results):
        """Generate human-readable markdown report"""
        with open("reports/report.md", "w") as f:
            f.write("# Facebook Ads Performance Analysis Report\n\n")
            f.write(f"**Generated**: {self._get_timestamp()}\n\n")
            
            # Data Summary Section
            if 'data_summary' in results:
                summary = results['data_summary']
                f.write("## Data Overview\n\n")
                f.write(f"- **Date Range**: {summary.get('date_range', 'N/A')}\n")
                f.write(f"- **Total Campaigns**: {summary.get('total_campaigns', 0)}\n")
                f.write(f"- **Total Spend**: ${summary.get('total_spend', 0):,.2f}\n")
                f.write(f"- **Total Revenue**: ${summary.get('total_revenue', 0):,.2f}\n")
                f.write(f"- **Overall ROAS**: {summary.get('overall_roas', 0):.2f}\n\n")
            
            # Key Insights Section
            if 'validated_insights' in results:
                f.write("## Key Insights\n\n")
                for idx, insight in enumerate(results['validated_insights'], 1):
                    f.write(f"### {idx}. {insight.get('hypothesis', 'Insight')}\n\n")
                    f.write(f"**Confidence**: {insight.get('confidence', 0):.0%}\n\n")
                    f.write(f"**Reasoning**: {insight.get('reasoning', 'N/A')}\n\n")
                    f.write(f"**Evidence**: {insight.get('validation_evidence', 'N/A')}\n\n")
                    f.write(f"**Validation Method**: {insight.get('validation_method', 'N/A')}\n\n")
                    f.write("---\n\n")
            
            # Creative Recommendations Section
            if 'creatives' in results:
                f.write("## Creative Recommendations\n\n")
                for creative in results['creatives']:
                    f.write(f"### Campaign: {creative.get('campaign_name', 'Unknown')}\n\n")
                    f.write(f"**Current CTR**: {creative.get('current_ctr', 0):.2%}\n\n")
                    
                    for var in creative.get('creative_variations', []):
                        f.write(f"**Variation {var.get('variation_id')}** ({var.get('framework', 'N/A')})\n")
                        f.write(f"- **Headline**: {var.get('headline', 'N/A')}\n")
                        f.write(f"- **Message**: {var.get('message', 'N/A')}\n")
                        f.write(f"- **CTA**: {var.get('cta', 'N/A')}\n")
                        f.write(f"- **Reasoning**: {var.get('reasoning', 'N/A')}\n\n")
                    
                    f.write("---\n\n")
    
    def _log(self, event, data):
        """Add structured log entry"""
        self.logs.append({
            "timestamp": self._get_timestamp(),
            "event": event,
            "data": data
        })
    
    def _save_logs(self):
        """Save logs to JSON file"""
        os.makedirs("logs", exist_ok=True)
        with open("logs/execution_log.json", "w") as f:
            json.dump(self.logs, f, indent=4)
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
