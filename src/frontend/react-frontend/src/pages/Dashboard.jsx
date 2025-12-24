import { useState, useEffect } from 'react';

function Dashboard({ onLogout, onProblemSelect, userData }) {
  const [dashboardData, setDashboardData] = useState({
    problems: [],
    recommendations: [],
    loading: true,
    progress: 0,
    problemsSolved: 0,
    totalProblems: 0
  });

  useEffect(() => {
    // Fetch data from backend
    const fetchDashboardData = async () => {
      try {
        // TODO: Replace with your actual backend URL
        const response = await fetch('http://localhost:5000/api/dashboard', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${userData?.token}`,
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          throw new Error('Failed to fetch dashboard data');
        }

        const data = await response.json();
        
        setDashboardData({
          problems: data.problems || [],
          recommendations: data.recommendations || [],
          progress: data.progress || 0,
          problemsSolved: data.problemsSolved || 0,
          totalProblems: data.totalProblems || 0,
          loading: false
        });
      } catch (error) {
        console.error('Error fetching dashboard:', error);
        // Keep empty state if backend not connected
        setDashboardData({
          ...dashboardData,
          loading: false
        });
      }
    };

    fetchDashboardData();
  }, [userData]);

  const getDifficultyColor = (difficulty) => {
    switch(difficulty?.toLowerCase()) {
      case 'easy': return 'text-green-400 bg-green-500/10 border-green-500/30';
      case 'medium': return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30';
      case 'hard': return 'text-red-400 bg-red-500/10 border-red-500/30';
      default: return 'text-gray-400 bg-gray-500/10 border-gray-500/30';
    }
  };

  const getImpactColor = (impact) => {
    switch(impact?.toLowerCase()) {
      case 'high': return 'text-green-400 border-green-500/30 bg-green-500/5';
      case 'medium': return 'text-blue-400 border-blue-500/30 bg-blue-500/5';
      case 'low': return 'text-gray-400 border-gray-500/30 bg-gray-500/5';
      default: return 'text-gray-400 border-gray-500/30 bg-gray-500/5';
    }
  };

  return (
    <div className="min-h-screen bg-black p-6">
      <div className="max-w-7xl mx-auto">
        {/* Progress Section */}
        <div className="mb-8 bg-zinc-900 border border-green-500/30 rounded-lg p-6 shadow-xl shadow-green-500/10">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold text-green-500">Your Progress</h2>
            <span className="text-gray-400 text-sm">
              {dashboardData.problemsSolved} / {dashboardData.totalProblems} problems solved
            </span>
          </div>
          
          {/* Progress Bar */}
          <div className="relative w-full h-8 bg-zinc-800 rounded-lg overflow-hidden border border-green-500/20">
            <div
              className="absolute top-0 left-0 h-full bg-gradient-to-r from-green-600 to-green-400 transition-all duration-500 ease-out flex items-center justify-center"
              style={{ width: `${dashboardData.progress}%` }}
            >
              {dashboardData.progress > 0 && (
                <span className="text-black font-bold text-sm">{dashboardData.progress}%</span>
              )}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Problems Section */}
          <div className="bg-zinc-900 border border-green-500/30 rounded-lg p-6 shadow-xl shadow-green-500/10">
            <div className="flex items-center mb-6">
              <svg className="w-8 h-8 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <h2 className="text-2xl font-bold text-green-500">Recommended Problems</h2>
            </div>
            
            {dashboardData.loading ? (
              <div className="text-center py-12">
                <div className="w-12 h-12 border-4 border-green-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                <div className="text-green-500 text-lg">Loading problems from AI...</div>
              </div>
            ) : dashboardData.problems.length === 0 ? (
              <div className="text-center py-12">
                <svg className="w-16 h-16 mx-auto text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p className="text-gray-400 mb-2">No problems available yet</p>
                <p className="text-gray-500 text-sm">AI is generating personalized problems for you</p>
                <p className="text-gray-600 text-xs mt-2">Make sure backend is running</p>
              </div>
            ) : (
              <div className="space-y-3">
                {dashboardData.problems.map((problem) => (
                  <button
                    key={problem.id}
                    onClick={() => onProblemSelect(problem)}
                    className="w-full text-left border rounded-lg p-4 bg-zinc-800 border-green-500/20 hover:border-green-500/50 hover:bg-zinc-800/80 transition duration-200"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-bold text-lg text-green-400">{problem.title}</h3>
                      <span className={`text-xs px-2 py-1 rounded border font-semibold ${getDifficultyColor(problem.difficulty)}`}>
                        {problem.difficulty}
                      </span>
                    </div>
                    <p className="text-gray-400 text-sm mb-2">{problem.description}</p>
                    {problem.category && (
                      <span className="text-green-500 text-xs font-semibold">{problem.category}</span>
                    )}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Recommendations Section */}
          <div className="bg-zinc-900 border border-blue-500/30 rounded-lg p-6 shadow-xl shadow-blue-500/10">
            <div className="flex items-center mb-6">
              <svg className="w-8 h-8 text-blue-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <h2 className="text-2xl font-bold text-blue-500">AI Recommendations</h2>
            </div>
            
            {dashboardData.loading ? (
              <div className="text-center py-12">
                <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                <div className="text-blue-500 text-lg">Analyzing your progress...</div>
              </div>
            ) : dashboardData.recommendations.length === 0 ? (
              <div className="text-center py-12">
                <svg className="w-16 h-16 mx-auto text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <p className="text-gray-400 mb-2">No recommendations yet</p>
                <p className="text-gray-500 text-sm">AI will analyze your performance and suggest improvements</p>
                <p className="text-gray-600 text-xs mt-2">Solve problems to get personalized feedback</p>
              </div>
            ) : (
              <div className="space-y-4">
                {dashboardData.recommendations.map((recommendation) => (
                  <div 
                    key={recommendation.id}
                    className={`border rounded-lg p-4 ${getImpactColor(recommendation.impact)}`}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-bold text-lg">{recommendation.title}</h3>
                      <span className="text-xs px-2 py-1 rounded uppercase font-semibold bg-black/30">
                        {recommendation.impact} impact
                      </span>
                    </div>
                    <p className="text-gray-300 text-sm">{recommendation.description}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
