import pytest
import pandas as pd
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.data_agent import DataAgent


class TestEvaluatorAgent:
    """Test suite for EvaluatorAgent"""
    
    def test_evaluator_filters_low_confidence(self):
        """Test that evaluator rejects hypotheses below confidence threshold"""
        
        # Mock data
        df = pd.DataFrame({
            'campaign_name': ['A', 'B', 'C'],
            'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'roas': [2.5, 2.0, 1.8],
            'ctr': [0.03, 0.025, 0.02],
            'spend': [100, 120, 110]
        })
        
        # Mock insights with varying confidence
        insights = [
            {
                "hypothesis": "ROAS has decreased in recent days",
                "reasoning": "Trend shows decline",
                "confidence": 0.85,
                "evidence_metrics": ["roas", "date"]
            },
            {
                "hypothesis": "Random speculation without evidence",
                "reasoning": "Just guessing",
                "confidence": 0.3,  # Below threshold
                "evidence_metrics": []
            }
        ]
        
        evaluator = EvaluatorAgent(model=None)
        validated = evaluator.evaluate(df, insights)
        
        # Should filter out low-confidence insights
        assert len(validated) >= 1, "Should keep at least one high-confidence insight"
        assert all(i['confidence'] >= 0.6 for i in validated), "All validated insights should have confidence >= 0.6"
    
    def test_evaluator_validates_roas_decline(self):
        """Test ROAS decline validation with quantitative evidence"""
        
        df = pd.DataFrame({
            'campaign_name': ['A'] * 7,
            'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-06', '2024-01-07'],
            'roas': [3.0, 2.9, 2.7, 2.5, 2.3, 2.1, 1.9],  # Clear downward trend
            'ctr': [0.03] * 7,
            'spend': [100] * 7
        })
        
        insights = [
            {
                "hypothesis": "ROAS has decreased in recent days",
                "reasoning": "Declining trend observed",
                "confidence": 0.75,
                "evidence_metrics": ["roas"]
            }
        ]
        
        evaluator = EvaluatorAgent(model=None)
        validated = evaluator.evaluate(df, insights)
        
        assert len(validated) == 1, "Should validate ROAS decline hypothesis"
        assert validated[0]['confidence'] >= 0.85, "Strong downward trend should have high confidence"
        assert "dropped from" in validated[0]['validation_evidence'].lower(), "Evidence should mention specific values"
    
    def test_evaluator_validates_low_ctr(self):
        """Test CTR threshold validation"""
        
        df = pd.DataFrame({
            'campaign_name': ['A', 'B', 'C'],
            'date': ['2024-01-01'] * 3,
            'roas': [2.5, 2.0, 1.8],
            'ctr': [0.015, 0.018, 0.012],  # All below 0.02 threshold
            'spend': [100, 120, 110]
        })
        
        insights = [
            {
                "hypothesis": "Average CTR is below industry standard",
                "reasoning": "CTR is low",
                "confidence": 0.70,
                "evidence_metrics": ["ctr"]
            }
        ]
        
        evaluator = EvaluatorAgent(model=None)
        validated = evaluator.evaluate(df, insights)
        
        assert len(validated) == 1, "Should validate low CTR hypothesis"
        assert validated[0]['confidence'] >= 0.8, "Clear threshold violation should have high confidence"
        assert "0.02" in validated[0]['validation_evidence'], "Evidence should mention threshold"
    
    def test_evaluator_validates_platform_comparison(self):
        """Test platform performance comparison validation"""
        
        df = pd.DataFrame({
            'campaign_name': ['A', 'B', 'C', 'D'],
            'date': ['2024-01-01'] * 4,
            'platform': ['Instagram', 'Instagram', 'Facebook', 'Facebook'],
            'roas': [3.5, 3.3, 2.0, 2.2],  # Instagram clearly better
            'ctr': [0.03, 0.032, 0.02, 0.021],
            'spend': [100, 120, 110, 130]
        })
        
        insights = [
            {
                "hypothesis": "Instagram platform performs better than Facebook",
                "reasoning": "Higher ROAS on Instagram",
                "confidence": 0.75,
                "evidence_metrics": ["platform", "roas"]
            }
        ]
        
        evaluator = EvaluatorAgent(model=None)
        validated = evaluator.evaluate(df, insights)
        
        assert len(validated) == 1, "Should validate platform comparison"
        assert validated[0]['confidence'] >= 0.8, "Clear platform difference should have high confidence"
        assert "instagram" in validated[0]['validation_evidence'].lower(), "Evidence should mention platforms"
    
    def test_evaluator_confidence_threshold(self):
        """Test that confidence threshold is properly applied"""
        
        df = pd.DataFrame({
            'campaign_name': ['A'],
            'date': ['2024-01-01'],
            'roas': [2.5],
            'ctr': [0.03],
            'spend': [100]
        })
        
        # Create insights that should be rejected
        insights = [
            {
                "hypothesis": "Unrelated hypothesis",
                "reasoning": "No evidence",
                "confidence": 0.5,  # Below threshold
                "evidence_metrics": []
            }
        ]
        
        evaluator = EvaluatorAgent(model=None)
        validated = evaluator.evaluate(df, insights)
        
        # Should filter out all low-confidence results
        assert len(validated) == 0, "Should reject all insights below confidence threshold"
    
    def test_validation_methods(self):
        """Test that different validation methods are applied correctly"""
        
        df = pd.DataFrame({
            'campaign_name': ['A', 'B'],
            'date': ['2024-01-01', '2024-01-02'],
            'platform': ['Instagram', 'Facebook'],
            'roas': [3.0, 2.0],
            'ctr': [0.015, 0.018],
            'spend': [100, 120]
        })
        
        insights = [
            {
                "hypothesis": "ROAS decreased",
                "reasoning": "Trend",
                "confidence": 0.7,
                "evidence_metrics": ["roas"]
            },
            {
                "hypothesis": "CTR is low",
                "reasoning": "Below threshold",
                "confidence": 0.7,
                "evidence_metrics": ["ctr"]
            }
        ]
        
        evaluator = EvaluatorAgent(model=None)
        validated = evaluator.evaluate(df, insights)
        
        # Check that validation methods are assigned
        for insight in validated:
            assert 'validation_method' in insight, "Each insight should have validation_method"
            assert insight['validation_method'] in ['trend_confirmation', 'threshold_test', 'comparative_analysis', 'correlation', 'rule_based']


class TestDataAgent:
    """Test suite for DataAgent"""
    
    def test_data_summary_format(self):
        """Test that data summary includes all required fields"""
        
        agent = DataAgent(model=None)
        
        # Create sample dataframe
        df = pd.DataFrame({
            'campaign_name': ['Campaign_A', 'Campaign_B'],
            'date': ['2024-01-01', '2024-01-02'],
            'platform': ['Instagram', 'Facebook'],
            'spend': [100, 200],
            'revenue': [300, 400],
            'roas': [3.0, 2.0],
            'ctr': [0.03, 0.02],
            'purchases': [10, 15],
            'impressions': [1000, 2000],
            'clicks': [30, 40],
            'creative_type': ['image', 'video'],
            'creative_message': ['Message 1', 'Message 2'],
            'audience_type': ['broad', 'retargeting'],
            'adset_name': ['Adset_1', 'Adset_2'],
            'country': ['US', 'UK']
        })
        
        # Save to temp CSV
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            df.to_csv(f.name, index=False)
            temp_path = f.name
        
        try:
            loaded_df, summary = agent.load_and_summarize(temp_path)
            
            # Verify required fields
            assert 'date_range' in summary, "Summary should include date_range"
            assert 'total_campaigns' in summary, "Summary should include total_campaigns"
            assert 'total_spend' in summary, "Summary should include total_spend"
            assert 'total_revenue' in summary, "Summary should include total_revenue"
            assert 'overall_roas' in summary, "Summary should include overall_roas"
            assert 'avg_metrics' in summary, "Summary should include avg_metrics"
            assert 'platform_performance' in summary, "Summary should include platform_performance"
            assert 'roas_trend_7d' in summary, "Summary should include roas_trend_7d"
            
            # Verify calculations
            assert summary['total_spend'] == 300, "Total spend should be sum of all spend"
            assert summary['total_revenue'] == 700, "Total revenue should be sum of all revenue"
            assert abs(summary['overall_roas'] - (700/300)) < 0.01, "Overall ROAS should be revenue/spend"
        
        finally:
            # Clean up
            os.unlink(temp_path)


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
