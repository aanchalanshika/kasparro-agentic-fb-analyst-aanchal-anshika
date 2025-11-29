import json
import os

class InsightAgent:
    def __init__(self, model=None):
        """Initialize Insight Agent with LLM model"""
        self.model = model
        self.prompt_template = self._load_prompt("prompts/insight_prompt.md")
    
    def _load_prompt(self, filepath):
        """Load prompt template from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def generate_insights(self, summary):
        """Generate hypotheses using LLM or fallback to rule-based"""
        if not self.model:
            return self._fallback_insights(summary)
        
        # Fill prompt with data summary
        filled_prompt = self.prompt_template.format(
            data_summary=json.dumps(summary, indent=2)
        )
        
        try:
            # Generate insights using LLM
            response = self.model.generate_content(filled_prompt)
            insights_text = response.text.strip()
            
            # Extract JSON from response
            if "```json" in insights_text:
                insights_text = insights_text.split("```json")[1].split("```")[0].strip()
            elif "```" in insights_text:
                insights_text = insights_text.split("```")[1].split("```")[0].strip()
            
            insights = json.loads(insights_text)
            return insights
        
        except Exception as e:
            print(f"⚠️ LLM insight generation failed: {e}. Using fallback.")
            return self._fallback_insights(summary)
    
    def _fallback_insights(self, summary):
        """Rule-based fallback insights if LLM fails"""
        insights = []

        # ROAS trend insight
        if summary.get("roas_trend_7d"):
            values = list(summary["roas_trend_7d"].values())
            if len(values) >= 2 and values[-1] < values[0]:
                insights.append({
                    "hypothesis": "ROAS has decreased in recent days",
                    "reasoning": f"THINK: ROAS dropped from {values[0]:.2f} to {values[-1]:.2f}. ANALYZE: Declining returns despite consistent spend suggests audience fatigue or creative saturation. CONCLUDE: Most likely creative fatigue or audience exhaustion.",
                    "confidence": 0.75,
                    "evidence_metrics": ["roas", "roas_trend_7d"],
                    "category": "roas_decline"
                })

        # CTR low insight
        avg_ctr = summary.get("avg_metrics", {}).get("ctr", 0)
        if avg_ctr < 0.02:
            insights.append({
                "hypothesis": "Average CTR is below industry standard",
                "reasoning": f"THINK: CTR is {avg_ctr:.4f}, below 2% benchmark. ANALYZE: Low engagement despite spend suggests creative quality issues. CONCLUDE: Creative messaging may not be resonating with target audience.",
                "confidence": 0.72,
                "evidence_metrics": ["ctr"],
                "category": "ctr_issue"
            })

        # Platform comparison insight
        platforms = summary.get("platform_performance", {})
        if platforms:
            best_platform = max(platforms.items(), key=lambda x: x[1].get("roas", 0))
            worst_platform = min(platforms.items(), key=lambda x: x[1].get("roas", 0))
            
            insights.append({
                "hypothesis": f"{best_platform[0]} platform performs better than {worst_platform[0]}",
                "reasoning": f"THINK: {best_platform[0]} ROAS ({best_platform[1].get('roas', 0):.2f}) significantly outperforms {worst_platform[0]} ({worst_platform[1].get('roas', 0):.2f}). ANALYZE: Platform-specific audience fit or competition levels differ. CONCLUDE: Budget reallocation may improve overall efficiency.",
                "confidence": 0.78,
                "evidence_metrics": ["platform", "roas"],
                "category": "platform_efficiency"
            })

        return insights
