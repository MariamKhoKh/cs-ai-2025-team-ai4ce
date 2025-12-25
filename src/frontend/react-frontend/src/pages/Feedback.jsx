import { useState, useEffect } from 'react';

function Feedback({ onLogout, submittedCode, problem, navigateTo }) {
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch AI-generated feedback from backend
    const fetchFeedback = async () => {
      try {
        const envBase = import.meta.env.VITE_API_URL;
        const fallback = window.__BACKEND_URL__ || window.location.origin || 'http://localhost:3000';
        const base = (envBase || fallback).replace(/\/$/, '');
        const submissionId = submittedCode?.submissionId;
        const url = `${base}/api/feedback/${submissionId}`;

        const response = await fetch(url, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch feedback: ${response.status}`);
        }

        const data = await response.json();
        // Backend should return AI-generated:
        // {
        //   score: number,
        //   correctedCode: string,
        //   issues: [...],
        //   strengths: [...],
        //   recommendations: [...],
        //   explanation: string
        // }
        setFeedback(data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching feedback:', err);
        setError('Failed to load AI feedback. Make sure backend is running or VITE_API_URL is set.');
        setLoading(false);
      }
    };

    if (submittedCode?.submissionId) {
      fetchFeedback();
    } else {
      setError('No submission found');
      setLoading(false);
    }
  }, [submittedCode]);

  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'high': return 'bg-red-500/10 border-red-500/30 text-red-400';
      case 'medium': return 'bg-yellow-500/10 border-yellow-500/30 text-yellow-400';
      case 'low': return 'bg-blue-500/10 border-blue-500/30 text-blue-400';
      default: return 'bg-gray-500/10 border-gray-500/30 text-gray-400';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-green-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <h2 className="text-2xl font-bold text-green-500 mb-2">AI is Analyzing Your Code...</h2>
          <p className="text-gray-400">Generating personalized feedback with LLM</p>
          <p className="text-gray-500 text-sm mt-2">This may take a few seconds</p>
        </div>
      </div>
    );
  }

  if (error || !feedback) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <svg className="w-20 h-20 text-red-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h2 className="text-2xl font-bold text-red-400 mb-4">{error || 'No Feedback Available'}</h2>
          <p className="text-gray-400 mb-6">Backend needs to be connected to generate AI feedback</p>
          <button
            onClick={() => navigateTo('dashboard')}
            className="px-6 py-2 bg-green-600 text-black rounded-lg font-bold hover:bg-green-500 transition duration-200"
          >
            Go to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-4xl font-bold text-green-500">AI-Generated Feedback</h1>
            <button
              onClick={() => navigateTo('dashboard')}
              className="px-6 py-2 bg-zinc-900 border border-green-500/30 text-green-500 rounded-lg hover:bg-zinc-800 transition duration-200"
            >
              Back to Dashboard
            </button>
          </div>
          {problem && (
            <p className="text-gray-400">Problem: <span className="text-green-400 font-semibold">{problem.title}</span></p>
          )}
        </div>

        {/* Score Card (AI-generated) */}
        {feedback.score !== undefined && (
          <div className="mb-8 bg-zinc-900 border border-green-500/30 rounded-lg p-6 shadow-xl shadow-green-500/10">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-green-500 mb-2">AI Score</h2>
                <p className="text-gray-400">Based on correctness, efficiency, and code quality</p>
              </div>
              <div className="text-center">
                <div className="text-6xl font-bold text-green-500">{feedback.score}</div>
                <div className="text-gray-400">/ 100</div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Issues Section (AI-generated) */}
          {feedback.issues && feedback.issues.length > 0 && (
            <div className="bg-zinc-900 border border-red-500/30 rounded-lg p-6 shadow-xl shadow-red-500/10">
              <div className="flex items-center mb-6">
                <svg className="w-8 h-8 text-red-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <h2 className="text-2xl font-bold text-red-500">Issues Found by AI</h2>
              </div>
              
              <div className="space-y-4">
                {feedback.issues.map((issue, index) => (
                  <div 
                    key={index}
                    className={`border rounded-lg p-4 ${getSeverityColor(issue.severity)}`}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-bold text-lg">{issue.title}</h3>
                      {issue.severity && (
                        <span className="text-xs px-2 py-1 rounded uppercase font-semibold bg-black/30">
                          {issue.severity}
                        </span>
                      )}
                    </div>
                    <p className="text-gray-300 text-sm mb-2">{issue.description}</p>
                    {issue.line && (
                      <span className="text-xs text-gray-500">Line {issue.line}</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Strengths Section (AI-generated) */}
          {feedback.strengths && feedback.strengths.length > 0 && (
            <div className="bg-zinc-900 border border-green-500/30 rounded-lg p-6 shadow-xl shadow-green-500/10">
              <div className="flex items-center mb-6">
                <svg className="w-8 h-8 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <h2 className="text-2xl font-bold text-green-500">What You Did Well</h2>
              </div>
              
              <ul className="space-y-3">
                {feedback.strengths.map((strength, index) => (
                  <li key={index} className="flex items-start">
                    <svg className="w-5 h-5 text-green-400 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-gray-300">{strength}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Explanation Section (AI-generated) */}
        {feedback.explanation && (
          <div className="mb-8 bg-zinc-900 border border-blue-500/30 rounded-lg p-6 shadow-xl shadow-blue-500/10">
            <div className="flex items-center mb-4">
              <svg className="w-8 h-8 text-blue-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h2 className="text-2xl font-bold text-blue-500">AI Explanation</h2>
            </div>
            <p className="text-gray-300 leading-relaxed whitespace-pre-line">{feedback.explanation}</p>
          </div>
        )}

        {/* Corrected Code Section (AI-generated) */}
        {feedback.correctedCode && (
          <div className="mb-8 bg-zinc-900 border border-green-500/30 rounded-lg p-6 shadow-xl shadow-green-500/10">
            <div className="flex items-center mb-4">
              <svg className="w-8 h-8 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
              <h2 className="text-2xl font-bold text-green-500">AI-Optimized Solution</h2>
            </div>
            <pre className="bg-black border border-green-500/20 rounded-lg p-4 overflow-x-auto">
              <code className="text-green-300 text-sm font-mono whitespace-pre">{feedback.correctedCode}</code>
            </pre>
          </div>
        )}

        {/* Recommendations Section (AI-generated) */}
        {feedback.recommendations && feedback.recommendations.length > 0 && (
          <div className="bg-zinc-900 border border-yellow-500/30 rounded-lg p-6 shadow-xl shadow-yellow-500/10">
            <div className="flex items-center mb-4">
              <svg className="w-8 h-8 text-yellow-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <h2 className="text-2xl font-bold text-yellow-500">AI Recommendations</h2>
            </div>
            <ul className="space-y-3">
              {feedback.recommendations.map((rec, index) => (
                <li key={index} className="flex items-start">
                  <svg className="w-5 h-5 text-yellow-400 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                  <span className="text-gray-300">{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default Feedback;
