"""
Regression Test Suite for CodeMentor AI

This test suite runs the golden set and validates that quality metrics
meet or exceed defined thresholds. Run this before every deployment to
catch quality degradation.

Usage:
    pytest test_regression.py -v
    
    Or run standalone:
    python test_regression.py
"""

import json
import time
import sys
import os
from pathlib import Path
from typing import Dict, List, Any
import statistics

# Add parent directory to path to import agent
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.backend.ai.optimized_agent import OptimizedCodeMentorAgent
except ImportError:
    print("Warning: Could not import OptimizedCodeMentorAgent, using baseline")
    from src.backend.ai.agent import CodeMentorAgent as OptimizedCodeMentorAgent


# Quality Thresholds - Adjust based on your baseline
THRESHOLDS = {
    "accuracy": 0.80,           # 80% of queries should succeed
    "avg_latency": 3.0,         # Average latency under 3 seconds
    "p95_latency": 5.0,         # 95th percentile under 5 seconds
    "avg_cost": 0.25,           # Average cost under $0.25 per query
    "error_rate": 0.05,         # Less than 5% error rate
    "min_response_length": 50,  # Responses should be substantial
}


class RegressionTester:
    """Runs golden set and validates quality metrics"""
    
    def __init__(self, golden_set_path: str = "golden_set.json"):
        """Initialize with path to golden set"""
        self.golden_set_path = Path(__file__).parent / golden_set_path
        self.results = []
        self.agent = None
        
    def load_golden_set(self) -> List[Dict]:
        """Load test queries from golden set"""
        with open(self.golden_set_path, 'r') as f:
            data = json.load(f)
            return data.get('golden_set', [])
    
    def initialize_agent(self):
        """Initialize the CodeMentor agent"""
        self.agent = OptimizedCodeMentorAgent()
        self.agent.start_conversation()
    
    def run_single_query(self, test_case: Dict) -> Dict[str, Any]:
        """Run a single test query and return result"""
        start_time = time.time()
        
        try:
            response = self.agent.send_message(test_case['query'])
            latency = time.time() - start_time
            
            # Estimate cost (use actual cost tracker if available)
            cost = 0.0
            if hasattr(self.agent, 'cost_tracker'):
                cost = self.agent.cost_tracker.total_cost
            
            return {
                "id": test_case['id'],
                "query": test_case['query'][:50] + "...",
                "category": test_case['category'],
                "difficulty": test_case['difficulty'],
                "success": True,
                "latency": round(latency, 3),
                "cost": round(cost, 6),
                "response_length": len(response) if isinstance(response, str) else 0,
                "response": response[:100] if isinstance(response, str) else str(response)[:100],
                "meets_quality": self._check_quality(test_case, response)
            }
        except Exception as e:
            latency = time.time() - start_time
            return {
                "id": test_case['id'],
                "query": test_case['query'][:50] + "...",
                "category": test_case['category'],
                "difficulty": test_case['difficulty'],
                "success": False,
                "latency": round(latency, 3),
                "cost": 0.0,
                "response_length": 0,
                "error": str(e),
                "meets_quality": False
            }
    
    def _check_quality(self, test_case: Dict, response: str) -> bool:
        """Check if response meets quality criteria"""
        if not response or not isinstance(response, str):
            return False
        
        # Check minimum length
        if len(response) < THRESHOLDS['min_response_length']:
            return False
        
        # Check for expected keywords if defined
        if 'expected_keywords' in test_case:
            keywords_found = sum(
                1 for kw in test_case['expected_keywords'] 
                if kw.lower() in response.lower()
            )
            # At least 50% of keywords should be present
            if keywords_found < len(test_case['expected_keywords']) * 0.5:
                return False
        
        return True
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests in golden set"""
        print(f"\n{'='*60}")
        print("CodeMentor AI Regression Test Suite")
        print(f"{'='*60}\n")
        
        # Load golden set
        golden_set = self.load_golden_set()
        print(f"Loaded {len(golden_set)} test queries")
        
        # Initialize agent
        print("Initializing agent...")
        self.initialize_agent()
        
        # Run tests
        print(f"\nRunning tests...\n")
        for i, test_case in enumerate(golden_set, 1):
            print(f"[{i}/{len(golden_set)}] Testing: {test_case['id']} ({test_case['difficulty']})...", end=" ")
            result = self.run_single_query(test_case)
            self.results.append(result)
            
            status = "✅ PASS" if result['success'] and result['meets_quality'] else "❌ FAIL"
            print(f"{status} ({result['latency']}s)")
        
        # Calculate metrics
        return self._calculate_metrics()
    
    def _calculate_metrics(self) -> Dict[str, Any]:
        """Calculate aggregate metrics from results"""
        successful = [r for r in self.results if r['success']]
        quality_pass = [r for r in self.results if r['meets_quality']]
        
        latencies = [r['latency'] for r in successful]
        costs = [r['cost'] for r in successful]
        
        sorted_latencies = sorted(latencies) if latencies else [0]
        
        metrics = {
            "total_tests": len(self.results),
            "successful": len(successful),
            "quality_pass": len(quality_pass),
            "failed": len(self.results) - len(successful),
            "accuracy": round(len(quality_pass) / len(self.results), 3),
            "error_rate": round((len(self.results) - len(successful)) / len(self.results), 3),
            "avg_latency": round(statistics.mean(latencies), 3) if latencies else 0,
            "median_latency": round(statistics.median(latencies), 3) if latencies else 0,
            "p95_latency": round(sorted_latencies[int(len(sorted_latencies) * 0.95) - 1], 3) if len(sorted_latencies) > 1 else (sorted_latencies[0] if sorted_latencies else 0),
            "p99_latency": round(sorted_latencies[int(len(sorted_latencies) * 0.99) - 1], 3) if len(sorted_latencies) > 1 else (sorted_latencies[0] if sorted_latencies else 0),
            "avg_cost": round(statistics.mean(costs), 6) if costs else 0,
            "total_cost": round(sum(costs), 6),
        }
        
        return metrics
    
    def validate_thresholds(self, metrics: Dict[str, Any]) -> Dict[str, bool]:
        """Validate that metrics meet thresholds"""
        validations = {
            "accuracy": metrics['accuracy'] >= THRESHOLDS['accuracy'],
            "avg_latency": metrics['avg_latency'] <= THRESHOLDS['avg_latency'],
            "p95_latency": metrics['p95_latency'] <= THRESHOLDS['p95_latency'],
            "avg_cost": metrics['avg_cost'] <= THRESHOLDS['avg_cost'],
            "error_rate": metrics['error_rate'] <= THRESHOLDS['error_rate'],
        }
        return validations
    
    def print_report(self, metrics: Dict[str, Any], validations: Dict[str, bool]):
        """Print test report"""
        print(f"\n{'='*60}")
        print("REGRESSION TEST RESULTS")
        print(f"{'='*60}\n")
        
        # Summary
        print("📊 SUMMARY")
        print(f"  Total Tests:     {metrics['total_tests']}")
        print(f"  Successful:      {metrics['successful']} ({metrics['successful']/metrics['total_tests']*100:.1f}%)")
        print(f"  Quality Pass:    {metrics['quality_pass']} ({metrics['accuracy']*100:.1f}%)")
        print(f"  Failed:          {metrics['failed']} ({metrics['error_rate']*100:.1f}%)")
        
        # Metrics
        print(f"\n⏱️  LATENCY")
        print(f"  Average:         {metrics['avg_latency']}s")
        print(f"  Median:          {metrics['median_latency']}s")
        print(f"  P95:             {metrics['p95_latency']}s")
        print(f"  P99:             {metrics['p99_latency']}s")
        
        print(f"\n💰 COST")
        print(f"  Per Query:       ${metrics['avg_cost']}")
        print(f"  Total:           ${metrics['total_cost']}")
        
        # Validations
        print(f"\n✅ THRESHOLD VALIDATION")
        all_pass = all(validations.values())
        
        for metric, passed in validations.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            threshold_val = THRESHOLDS[metric]
            actual_val = metrics[metric]
            
            if 'latency' in metric or 'cost' in metric or 'error_rate' in metric:
                # Lower is better
                print(f"  {metric:20} {status:8} (actual: {actual_val}, threshold: ≤ {threshold_val})")
            else:
                # Higher is better
                print(f"  {metric:20} {status:8} (actual: {actual_val}, threshold: ≥ {threshold_val})")
        
        print(f"\n{'='*60}")
        if all_pass:
            print("🎉 ALL CHECKS PASSED - System quality maintained!")
        else:
            print("⚠️  QUALITY REGRESSION DETECTED - Review failed checks")
        print(f"{'='*60}\n")
        
        return all_pass
    
    def save_results(self, metrics: Dict[str, Any], filename: str = "regression_results.json"):
        """Save results to file"""
        output = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "metrics": metrics,
            "thresholds": THRESHOLDS,
            "detailed_results": self.results
        }
        
        output_path = Path(__file__).parent / filename
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"Results saved to: {output_path}")


def main():
    """Main entry point for regression testing"""
    tester = RegressionTester()
    
    # Run tests
    metrics = tester.run_all_tests()
    
    # Validate against thresholds
    validations = tester.validate_thresholds(metrics)
    
    # Print report
    all_pass = tester.print_report(metrics, validations)
    
    # Save results
    tester.save_results(metrics)
    
    # Exit with appropriate code
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
