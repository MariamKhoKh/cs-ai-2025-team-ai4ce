import json
import time
from datetime import datetime
from typing import List, Dict, Any
import statistics

# Import your agents
from src.backend.ai.agent import CodeMentorAgent  # Baseline
from src.backend.ai.optimized_agent import OptimizedCodeMentorAgent  # Optimized


# ==================== TEST QUERIES ====================

TEST_QUERIES = [
    # Recommendations (should be cached after first call)
    "What problem should I practice next?",
    "What problem should I practice next?",  # Cache hit expected
    "Recommend me an easy problem",
    "What should I work on to improve?",
    "What problem should I practice next?",  # Cache hit expected
    
    # Code analysis (more expensive)
    """Analyze this code:
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
""",
    
    # Progress tracking
    "Track my progress on two-sum problem",
    
    # More recommendations
    "Suggest a medium difficulty problem",
    "What problem should I practice next?",  # Cache hit expected
    "Recommend something for arrays",
]


# ==================== BENCHMARK RUNNER ====================

class Benchmark:
    """Run performance benchmarks"""
    
    def __init__(self, name: str, agent):
        self.name = name
        self.agent = agent
        self.results = []
    
    def run_query(self, query: str, query_id: int) -> Dict[str, Any]:
        """Run a single query and measure performance"""
        start_time = time.time()
        
        try:
            response = self.agent.send_message(query)
            latency = time.time() - start_time
            
            # Extract cost if available
            cost = 0.008  # Default estimate
            if hasattr(self.agent, 'cost_tracker'):
                cost = self.agent.cost_tracker.total_cost / max(1, self.agent.cost_tracker.call_count)
            
            return {
                "query_id": query_id,
                "query": query[:50] + "..." if len(query) > 50 else query,
                "latency_seconds": round(latency, 2),
                "cost": round(cost, 6),
                "success": True,
                "response_length": len(response) if isinstance(response, str) else 0
            }
        
        except Exception as e:
            return {
                "query_id": query_id,
                "query": query[:50] + "...",
                "latency_seconds": time.time() - start_time,
                "cost": 0.0,
                "success": False,
                "error": str(e)
            }
    
    def run_benchmark(self, queries: List[str], num_iterations: int = 5) -> Dict[str, Any]:
        """Run full benchmark suite"""
        print(f"\n{'='*60}")
        print(f"Running {self.name} Benchmark")
        print(f"{'='*60}\n")
        
        all_results = []
        
        # Run queries multiple times to get average
        for iteration in range(num_iterations):
            print(f"Iteration {iteration + 1}/{num_iterations}")
            
            for idx, query in enumerate(queries):
                query_id = iteration * len(queries) + idx + 1
                result = self.run_query(query, query_id)
                all_results.append(result)
                
                print(f"  Query {query_id}: {result['latency_seconds']:.2f}s | ${result['cost']:.6f}")
        
        self.results = all_results
        return self.compute_statistics()
    
    def compute_statistics(self) -> Dict[str, Any]:
        """Compute summary statistics"""
        successful_results = [r for r in self.results if r['success']]
        
        if not successful_results:
            return {"error": "No successful queries"}
        
        latencies = [r['latency_seconds'] for r in successful_results]
        costs = [r['cost'] for r in successful_results]
        
        # Sort for percentile calculations
        sorted_latencies = sorted(latencies)
        
        stats = {
            "benchmark_name": self.name,
            "measurement_date": datetime.now().isoformat(),
            "total_queries": len(self.results),
            "successful_queries": len(successful_results),
            "failed_queries": len(self.results) - len(successful_results),
            
            # Cost metrics
            "total_cost": round(sum(costs), 6),
            "average_cost": round(statistics.mean(costs), 6),
            "median_cost": round(statistics.median(costs), 6),
            
            # Latency metrics
            "average_latency": round(statistics.mean(latencies), 2),
            "median_latency": round(statistics.median(latencies), 2),
            "min_latency": round(min(latencies), 2),
            "max_latency": round(max(latencies), 2),
            "p95_latency": round(sorted_latencies[int(len(sorted_latencies) * 0.95)], 2),
            "p99_latency": round(sorted_latencies[int(len(sorted_latencies) * 0.99)], 2),
            
            # Additional metrics
            "latency_std_dev": round(statistics.stdev(latencies), 2) if len(latencies) > 1 else 0,
        }
        
        return stats
    
    def save_results(self, filename: str):
        """Save results to JSON file"""
        stats = self.compute_statistics()
        
        output = {
            "summary": stats,
            "detailed_results": self.results
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n Results saved to {filename}")


# ==================== COMPARISON ====================

def compare_benchmarks(baseline_stats: Dict, optimized_stats: Dict) -> Dict[str, Any]:
    """Compare baseline vs optimized performance"""
    
    cost_reduction = ((baseline_stats['average_cost'] - optimized_stats['average_cost']) / 
                     baseline_stats['average_cost'] * 100)
    
    latency_change = ((baseline_stats['average_latency'] - optimized_stats['average_latency']) / 
                     baseline_stats['average_latency'] * 100)
    
    comparison = {
        "cost_reduction_percent": round(cost_reduction, 1),
        "latency_improvement_percent": round(latency_change, 1),
        
        "baseline": {
            "cost_per_query": baseline_stats['average_cost'],
            "latency": baseline_stats['average_latency'],
            "p95_latency": baseline_stats['p95_latency']
        },
        
        "optimized": {
            "cost_per_query": optimized_stats['average_cost'],
            "latency": optimized_stats['average_latency'],
            "p95_latency": optimized_stats['p95_latency']
        },
        
        "monthly_projection": {
            "queries_per_month": 15000,
            "baseline_cost": round(baseline_stats['average_cost'] * 15000, 2),
            "optimized_cost": round(optimized_stats['average_cost'] * 15000, 2),
            "monthly_savings": round((baseline_stats['average_cost'] - optimized_stats['average_cost']) * 15000, 2)
        }
    }
    
    return comparison


# ==================== MAIN ====================

def main():
    """Run benchmarks and compare"""
    
    print(" CodeMentor Optimization Benchmark")
    print("=" * 60)
    
    # Step 1: Baseline
    print("\n Step 1: Running BASELINE benchmark...")
    baseline_agent = CodeMentorAgent()
    baseline_agent.start_conversation()
    
    baseline = Benchmark("Baseline (Gemini 2.0 Flash)", baseline_agent)
    baseline_stats = baseline.run_benchmark(TEST_QUERIES, num_iterations=5)
    baseline.save_results("baseline.json")
    
    # Step 2: Optimized
    print("\nStep 2: Running OPTIMIZED benchmark...")
    optimized_agent = OptimizedCodeMentorAgent()
    optimized_agent.start_conversation()
    
    optimized = Benchmark("Optimized (Caching + Token Reduction + Routing)", optimized_agent)
    optimized_stats = optimized.run_benchmark(TEST_QUERIES, num_iterations=5)
    optimized.save_results("optimized.json")
    
    # Step 3: Compare
    print("\nStep 3: Computing comparison...")
    comparison = compare_benchmarks(baseline_stats, optimized_stats)
    
    with open("comparison.json", 'w') as f:
        json.dump(comparison, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    
    print(f"\nCOST:")
    print(f"  Baseline:  ${baseline_stats['average_cost']:.6f} per query")
    print(f"  Optimized: ${optimized_stats['average_cost']:.6f} per query")
    print(f"  Savings:   {comparison['cost_reduction_percent']:.1f}%")
    
    print(f"\nLATENCY:")
    print(f"  Baseline:  {baseline_stats['average_latency']:.2f}s")
    print(f"  Optimized: {optimized_stats['average_latency']:.2f}s")
    print(f"  Improvement: {comparison['latency_improvement_percent']:.1f}%")
    
    print(f"\n MONTHLY PROJECTION:")
    print(f"  Baseline:  ${comparison['monthly_projection']['baseline_cost']:.2f}/month")
    print(f"  Optimized: ${comparison['monthly_projection']['optimized_cost']:.2f}/month")
    print(f"  Savings:   ${comparison['monthly_projection']['monthly_savings']:.2f}/month")
    
    print(f"\n Benchmark complete! Check baseline.json and optimized.json for details.")


if __name__ == "__main__":
    main()