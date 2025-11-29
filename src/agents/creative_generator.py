import json
import os

class CreativeGenerator:
    def __init__(self, model=None):
        """Initialize Creative Generator with LLM model"""
        self.model = model
        self.prompt_template = self._load_prompt("prompts/creative_prompt.md")
    
    def _load_prompt(self, filepath):
        """Load prompt template from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def generate(self, summary):
        """Generate creative recommendations using LLM or fallback"""
        if not self.model:
            return self._fallback_creatives(summary)
        
        # Fill prompt with data summary
        filled_prompt = self.prompt_template.format(
            data_summary=json.dumps(summary, indent=2)
        )
        
        try:
            # Generate creatives using LLM
            response = self.model.generate_content(filled_prompt)
            creatives_text = response.text.strip()
            
            # Extract JSON from response
            if "```json" in creatives_text:
                creatives_text = creatives_text.split("```json")[1].split("```")[0].strip()
            elif "```" in creatives_text:
                creatives_text = creatives_text.split("```")[1].split("```")[0].strip()
            
            creatives = json.loads(creatives_text)
            return creatives
        
        except Exception as e:
            print(f"⚠️ LLM creative generation failed: {e}. Using fallback.")
            return self._fallback_creatives(summary)
    
    def _fallback_creatives(self, summary):
        """Rule-based fallback creatives if LLM fails"""
        creatives = []
        
        low_ctr_campaigns = summary.get("low_ctr_campaigns", [])

        for row in low_ctr_campaigns[:3]:  # Limit to top 3
            campaign_name = row.get("campaign_name", "Unknown Campaign")
            current_ctr = row.get("ctr", 0)
            current_message = row.get("creative_message", "")
            
            creatives.append({
                "campaign_name": campaign_name,
                "current_ctr": current_ctr,
                "current_creative_message": current_message,
                "creative_variations": [
                    {
                        "variation_id": 1,
                        "headline": "Experience Ultimate Comfort All Day Long",
                        "message": "Breathable, ultra-soft undergarments designed for active lifestyles. Say goodbye to discomfort and hello to confidence.",
                        "cta": "Shop Comfort Now",
                        "framework": "emotional",
                        "reasoning": "Emotional appeal to comfort addresses core product benefit. Low CTR suggests generic messaging needs differentiation."
                    },
                    {
                        "variation_id": 2,
                        "headline": "Premium Quality - Now 30% Off",
                        "message": "High-quality materials at unbeatable prices. Limited-time offer on our best-selling comfort collection. Free shipping over $50.",
                        "cta": "Claim Your Discount",
                        "framework": "logical",
                        "reasoning": "Value-conscious messaging with specific discount percentage. Price mentions typically increase CTR."
                    },
                    {
                        "variation_id": 3,
                        "headline": "Flash Sale Ends Tonight at Midnight",
                        "message": "Don't miss your chance to upgrade your essentials. Premium undergarments at prices that won't last. Limited stock available.",
                        "cta": "Shop Before Midnight",
                        "framework": "urgency",
                        "reasoning": "Creates time pressure to drive immediate action. Urgency-based creatives achieve higher CTR during promotions."
                    }
                ]
            })

        return creatives
