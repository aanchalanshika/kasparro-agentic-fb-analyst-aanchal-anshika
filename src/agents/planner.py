import json
import os
import google.generativeai as genai

class PlannerAgent:
    def __init__(self, model=None):
        """Initialize Planner Agent with LLM model"""
        self.model = model
        self.prompt_template = self._load_prompt("prompts/planner_prompt.md")
    
    def _load_prompt(self, filepath):
        """Load prompt template from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def create_plan(self, user_query):
        """
        Generate execution plan for user query using LLM
        Returns dict with subtasks and agent assignments
        """
        if not self.model:
            # Fallback to rule-based planning if no model
            return self._fallback_plan(user_query)
        
        # Fill prompt template with user query
        filled_prompt = self.prompt_template.format(user_query=user_query)
        
        try:
            # Generate plan using LLM
            response = self.model.generate_content(filled_prompt)
            plan_text = response.text.strip()
            
            # Extract JSON from response (handle markdown code blocks)
            if "```json" in plan_text:
                plan_text = plan_text.split("```json")[1].split("```")[0].strip()
            elif "```" in plan_text:
                plan_text = plan_text.split("```")[1].split("```")[0].strip()
            
            plan = json.loads(plan_text)
            return plan
        
        except Exception as e:
            print(f"⚠️ LLM planning failed: {e}. Using fallback plan.")
            return self._fallback_plan(user_query)
    
    def _fallback_plan(self, query):
        """Rule-based fallback plan if LLM fails"""
        query_lower = query.lower()
        
        subtasks = [
            {"task_id": 1, "task": "Load data and generate summary", "agent": "data_agent", "dependencies": []},
            {"task_id": 2, "task": "Generate hypotheses for performance patterns", "agent": "insight_agent", "dependencies": [1]},
            {"task_id": 3, "task": "Validate hypotheses quantitatively", "agent": "evaluator_agent", "dependencies": [1, 2]},
            {"task_id": 4, "task": "Generate creative recommendations for low-CTR campaigns", "agent": "creative_generator", "dependencies": [1]}
        ]
        
        return {
            "user_query": query,
            "subtasks": subtasks
        }
    
    def plan(self, query):
        """Legacy method for backwards compatibility"""
        return [
            "load_data",
            "summarize_data",
            "analyze_roas",
            "analyze_ctr",
            "generate_hypotheses",
            "validate_hypotheses",
            "generate_creatives",
            "create_report"
        ]
