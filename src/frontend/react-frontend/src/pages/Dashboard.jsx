import { useState, useEffect } from 'react';

function Dashboard({ onLogout }) {
  const [dashboardData, setDashboardData] = useState({
    problems: [],
    recommendations: [],
    loading: false
  });

  useEffect(() => {
    // TODO: Fetch data from backend
    // fetch('http://your-backend-api/analyze', {
    //   method: 'GET',
    //   headers: {
    //     'Authorization': `Bearer ${authToken}`,
    //     'Content-Type': 'application/json'
    //   }
    // })
    // .then(response => response.json())
    // .then(data => {
    //   setDashboardData({
    //     problems: data.problems,
    //     recommendations: data.recommendations,
    //     loading: false
    //   });
    // })
  }, []);

  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'high': return 'text-red-400 border-red-500/30 bg-red-500/5';
      case 'medium': return 'text-yellow-400 border-yellow-500/30 bg-yellow-500/5';
      case 'low': return 'text-green-400 border-green-500/30 bg-green-500/5';
      default: return 'text-gray-400 border-gray-500/30 bg-gray-500/5';
    }
  };

  const getImpactColor = (impact) => {
    switch(impact) {
      case 'high': return 'text-green-400 border-green-500/30 bg-green-500/5';
      case 'medium': return 'text-blue-400 border-blue-500/30 bg-blue-500/5';
      case 'low': return 'text-gray-400 border-gray-500/30 bg-gray-500/5';
      default: return 'text-gray-400 border-gray-500/30 bg-gray-500/5';
    }
  };

  return (
    <div className="min-h-screen bg-black p-6">
      <div className="max-w-7xl mx-auto mb-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-green-500 mb-2">Code Analysis Dashboard</h1>
            <p className="text-gray-400">AI-Powered Code Review & Recommendations</p>
          </div>
          <button
            onClick={onLogout}
            className="px-6 py-2 bg-zinc-900 border border-green-500/30 text-green-500 rounded-lg hover:bg-zinc-800 transition duration-200"
          >
            Logout
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Problems Section */}
          <div className="bg-zinc-900 border border-red-500/30 rounded-lg p-6 shadow-xl shadow-red-500/10">
            <div className="flex items-center mb-6">
              <svg className="w-8 h-8 text-red-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <h2 className="text-2xl font-bold text-red-500">Code Issues</h2>
            </div>
            
            {dashboardData.problems.length === 0 ? (
              <div className="text-center py-12">
                <svg className="w-16 h-16 mx-auto text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p className="text-gray-400 mb-2">No code issues detected</p>
                <p className="text-gray-500 text-sm">Upload code for analysis</p>
              </div>
            ) : (
              <div className="space-y-4">
                {dashboardData.problems.map((problem) => (
                  <div 
                    key={problem.id}
                    className={`border rounded-lg p-4 ${getSeverityColor(problem.severity)}`}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-bold text-lg">{problem.title}</h3>
                      <span className={`text-xs px-2 py-1 rounded uppercase font-semibold`}>
                        {problem.severity}
                      </span>
                    </div>
                    <p className="text-gray-300 text-sm">{problem.description}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Recommendations Section */}
          <div className="bg-zinc-900 border border-green-500/30 rounded-lg p-6 shadow-xl shadow-green-500/10">
            <div className="flex items-center mb-6">
              <svg className="w-8 h-8 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h2 className="text-2xl font-bold text-green-500">AI Recommendations</h2>
            </div>
            
            {dashboardData.recommendations.length === 0 ? (
              <div className="text-center py-12">
                <svg className="w-16 h-16 mx-auto text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <p className="text-gray-400 mb-2">No recommendations yet</p>
                <p className="text-gray-500 text-sm">AI analysis will appear here</p>
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
                      <span className={`text-xs px-2 py-1 rounded uppercase font-semibold`}>
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