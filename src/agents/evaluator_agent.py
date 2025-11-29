import json
import os

class EvaluatorAgent:
    def __init__(self, model=None):
        """Initialize Evaluator Agent"""
        self.model = model
        self.prompt_template = self._load_prompt("prompts/evaluator_prompt.md")
        self.confidence_threshold = 0.6
    
    def _load_prompt(self, filepath):
        """Load prompt template from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def evaluate(self, df, insights):
        """
        Validate hypotheses quantitatively using DataFrame
        Returns only insights with confidence >= threshold
        """
        evaluated = []

        for item in insights:
            hypothesis = item.get("hypothesis", item.get("insight", ""))
            reasoning = item.get("reasoning", item.get("reason", ""))
            
            # Perform quantitative validation
            validation_result = self._validate_hypothesis(df, item)
            
            # Only include if confidence meets threshold
            if validation_result["confidence"] >= self.confidence_threshold:
                evaluated.append({
                    "hypothesis": hypothesis,
                    "reasoning": reasoning,
                    "validation_evidence": validation_result["evidence"],
                    "confidence": validation_result["confidence"],
                    "metrics_checked": validation_result["metrics"],
                    "validation_method": validation_result["method"],
                    "status": "validated"
                })

        return evaluated
    
    def _validate_hypothesis(self, df, insight):
        """Validate individual hypothesis against DataFrame"""
        hypothesis = insight.get("hypothesis", insight.get("insight", "")).lower()
        confidence = 0.7  # Base confidence
        evidence = ""
        metrics = []
        method = "threshold_test"
        
        # Validation 1: ROAS decline
        if "roas" in hypothesis and ("decreas" in hypothesis or "drop" in hypothesis or "decline" in hypothesis):
            trend = df.groupby("date")["roas"].mean().tail(7)
            if len(trend) >= 2 and trend.iloc[-1] < trend.iloc[0]:
                decline_pct = ((trend.iloc[0] - trend.iloc[-1]) / trend.iloc[0]) * 100
                evidence = f"ROAS dropped from {trend.iloc[0]:.2f} to {trend.iloc[-1]:.2f} ({decline_pct:.1f}% decline). Confirmed via 7-day trend analysis."
                confidence = 0.92
                metrics = ["roas", "date"]
                method = "trend_confirmation"
            else:
                evidence = "No ROAS decline detected in data."
                confidence = 0.2

        # Validation 2: Low CTR
        elif "ctr" in hypothesis and ("low" in hypothesis or "below" in hypothesis):
            avg_ctr = df["ctr"].mean()
            if avg_ctr < 0.02:
                pct_below = (df["ctr"] < 0.02).sum() / len(df) * 100
                evidence = f"CTR mean is {avg_ctr:.4f}, below 0.02 threshold. {pct_below:.1f}% of campaigns have CTR < 2%."
                confidence = 0.86
                metrics = ["ctr"]
                method = "threshold_test"
            else:
                evidence = f"CTR mean is {avg_ctr:.4f}, above threshold."
                confidence = 0.3

        # Validation 3: Platform performance
        elif "platform" in hypothesis and ("perform" in hypothesis or "better" in hypothesis):
            platform_roas = df.groupby("platform")["roas"].mean()
            if len(platform_roas) >= 2:
                best = platform_roas.idxmax()
                worst = platform_roas.idxmin()
                diff_pct = ((platform_roas[best] - platform_roas[worst]) / platform_roas[worst]) * 100
                evidence = f"{best} avg ROAS: {platform_roas[best]:.2f}, {worst} avg ROAS: {platform_roas[worst]:.2f} ({diff_pct:.1f}% difference)"
                confidence = 0.89
                metrics = ["platform", "roas"]
                method = "comparative_analysis"

        # Validation 4: Spend correlation
        elif "spend" in hypothesis:
            correlation = df[["spend", "roas"]].corr().iloc[0, 1]
            evidence = f"Spend-ROAS correlation: {correlation:.3f}"
            confidence = 0.75 if abs(correlation) > 0.3 else 0.4
            metrics = ["spend", "roas"]
            method = "correlation"

        # Default validation
        else:
            evidence = "Generic validation applied."
            confidence = insight.get("confidence", 0.7)
            metrics = insight.get("evidence_metrics", [])
            method = "rule_based"

        return {
            "confidence": round(confidence, 2),
            "evidence": evidence,
            "metrics": metrics,
            "method": method
        }
