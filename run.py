from src.orchestrator.orchestrator import Orchestrator
import sys

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Analyze ROAS"
    Orchestrator().run(query)
    print("Analysis complete! Check the 'reports' folder for insights.json, creatives.json, and report.md")
