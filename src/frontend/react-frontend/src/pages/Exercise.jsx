import { useState, useEffect } from 'react';

function Exercise({ onLogout }) {
  const [exerciseData, setExerciseData] = useState({
    title: '',
    description: '',
    difficulty: '',
    examples: [],
    constraints: [],
    loading: true
  });
  
  const [userCode, setUserCode] = useState('// Write your code here\n\n');

  useEffect(() => {
    // TODO: Fetch exercise from backend
    // fetch('http://your-backend-api/exercise', {
    //   method: 'GET',
    //   headers: {
    //     'Authorization': `Bearer ${authToken}`,
    //     'Content-Type': 'application/json'
    //   }
    // })
    // .then(response => response.json())
    // .then(data => {
    //   setExerciseData({
    //     title: data.title,
    //     description: data.description,
    //     difficulty: data.difficulty,
    //     examples: data.examples,
    //     constraints: data.constraints,
    //     loading: false
    //   });
    // })
    
    setExerciseData({
      ...exerciseData,
      loading: false
    });
  }, []);

  const handleRunCode = () => {
    console.log('Running code:', userCode);
    // TODO: Send code to backend for execution
  };

  const handleSubmitCode = () => {
    console.log('Submitting code:', userCode);
    // TODO: Send code to backend for validation
  };

  const getDifficultyColor = (difficulty) => {
    switch(difficulty?.toLowerCase()) {
      case 'easy': return 'text-green-400 bg-green-500/10 border-green-500/30';
      case 'medium': return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30';
      case 'hard': return 'text-red-400 bg-red-500/10 border-red-500/30';
      default: return 'text-gray-400 bg-gray-500/10 border-gray-500/30';
    }
  };

  return (
    <div className="h-screen bg-black flex flex-col">
      {/* Header */}
      <div className="bg-zinc-900 border-b border-green-500/30 px-6 py-4 flex justify-between items-center">
        <div className="flex items-center">
          <svg className="w-8 h-8 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
          </svg>
          <h1 className="text-2xl font-bold text-green-500">Code Exercise</h1>
        </div>
        <button
          onClick={onLogout}
          className="px-4 py-2 bg-zinc-800 border border-green-500/30 text-green-500 rounded-lg hover:bg-zinc-700 transition duration-200 text-sm"
        >
          Logout
        </button>
      </div>

      {/* Split Screen */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Side - Problem Description */}
        <div className="w-1/2 border-r border-green-500/30 overflow-y-auto p-6">
          {exerciseData.loading ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-green-500 text-xl">Loading exercise...</div>
            </div>
          ) : !exerciseData.title ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <svg className="w-20 h-20 text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h2 className="text-2xl font-bold text-gray-400 mb-2">No Exercise Loaded</h2>
              <p className="text-gray-500">Waiting for backend to provide exercise data</p>
            </div>
          ) : (
            <div>
              <div className="mb-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-3xl font-bold text-green-500">{exerciseData.title}</h2>
                  {exerciseData.difficulty && (
                    <span className={`px-3 py-1 rounded-lg text-sm font-semibold border ${getDifficultyColor(exerciseData.difficulty)}`}>
                      {exerciseData.difficulty}
                    </span>
                  )}
                </div>
                <p className="text-gray-300 leading-relaxed">{exerciseData.description}</p>
              </div>

              {exerciseData.examples && exerciseData.examples.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-xl font-bold text-green-400 mb-3">Examples</h3>
                  {exerciseData.examples.map((example, index) => (
                    <div key={index} className="bg-zinc-900 border border-green-500/20 rounded-lg p-4 mb-3">
                      <div className="mb-2">
                        <span className="text-gray-400 font-semibold">Input: </span>
                        <code className="text-green-300">{example.input}</code>
                      </div>
                      <div>
                        <span className="text-gray-400 font-semibold">Output: </span>
                        <code className="text-green-300">{example.output}</code>
                      </div>
                      {example.explanation && (
                        <div className="mt-2 text-gray-400 text-sm">
                          <span className="font-semibold">Explanation: </span>
                          {example.explanation}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {exerciseData.constraints && exerciseData.constraints.length > 0 && (
                <div>
                  <h3 className="text-xl font-bold text-green-400 mb-3">Constraints</h3>
                  <ul className="list-disc list-inside space-y-2">
                    {exerciseData.constraints.map((constraint, index) => (
                      <li key={index} className="text-gray-300">{constraint}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right Side - Code Editor */}
        <div className="w-1/2 flex flex-col">
          <div className="bg-zinc-900 border-b border-green-500/30 px-6 py-3 flex justify-between items-center">
            <h3 className="text-lg font-bold text-green-500">Code Editor</h3>
            <div className="flex gap-2">
              <button
                onClick={handleRunCode}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-500 transition duration-200 text-sm font-semibold"
              >
                Run Code
              </button>
              <button
                onClick={handleSubmitCode}
                className="px-4 py-2 bg-green-600 text-black rounded-lg hover:bg-green-500 transition duration-200 text-sm font-semibold shadow-lg shadow-green-500/30"
              >
                Submit
              </button>
            </div>
          </div>
          
          <textarea
            value={userCode}
            onChange={(e) => setUserCode(e.target.value)}
            className="flex-1 p-6 bg-black text-green-100 font-mono text-sm focus:outline-none resize-none"
            spellCheck="false"
            style={{ 
              fontFamily: "'Fira Code', 'Courier New', monospace",
              tabSize: 2
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default Exercise;