import pandas as pd
import os

class DataAgent:
    def __init__(self, model=None):
        """Initialize Data Agent (doesn't need LLM for summary generation)"""
        self.model = model
        self.prompt_template = self._load_prompt("prompts/data_agent_prompt.md")
    
    def _load_prompt(self, filepath):
        """Load prompt template from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_and_summarize(self, path):
        """Load CSV and generate statistical summary"""
        df = pd.read_csv(path)

        summary = {
            "date_range": f"{df['date'].min()} to {df['date'].max()}",
            "total_campaigns": df['campaign_name'].nunique(),
            "total_spend": round(df["spend"].sum(), 2),
            "total_revenue": round(df["revenue"].sum(), 2),
            "overall_roas": round(df["revenue"].sum() / df["spend"].sum(), 4) if df["spend"].sum() > 0 else 0,
            
            "avg_metrics": {
                "roas": round(df["roas"].mean(), 4),
                "ctr": round(df["ctr"].mean(), 4),
                "spend": round(df["spend"].mean(), 4),
                "purchases": round(df["purchases"].mean(), 4)
            },
            
            "platform_performance": df.groupby("platform").agg({
                "roas": "mean",
                "ctr": "mean",
                "spend": "sum"
            }).round(4).to_dict(orient="index"),
            
            "roas_trend_7d": df.groupby("date")["roas"].mean().tail(7).round(4).to_dict(),
            
            "top_5_campaigns": df.groupby("campaign_name").agg({
                "roas": "mean",
                "spend": "sum"
            }).nlargest(5, "roas").round(4).reset_index().to_dict(orient="records"),
            
            "bottom_5_campaigns": df.groupby("campaign_name").agg({
                "roas": "mean",
                "ctr": "mean"
            }).nsmallest(5, "roas").round(4).reset_index().to_dict(orient="records"),
            
            "low_ctr_campaigns": df[df["ctr"] < 0.02].nsmallest(5, "ctr")[
                ["campaign_name", "ctr", "creative_message"]
            ].to_dict(orient="records")
        }

        return df, summary
