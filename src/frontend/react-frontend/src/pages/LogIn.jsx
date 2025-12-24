import { useState } from 'react';

function LogIn({ navigateTo, onLogin }) {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleLogIn = async () => {
    console.log('Log In Data:', formData);
    
    // TODO: Add login API call here
    // Example:
    // const response = await fetch('http://localhost:5000/api/login', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(formData)
    // });
    // const data = await response.json();
    
    // For now, simulating successful login with mock user data
    const mockUser = {
      id: 1,
      name: formData.email.split('@')[0], // Extract name from email
      email: formData.email,
      token: 'mock-jwt-token'
    };
    
    // After successful login, call onLogin with user data
    onLogin(mockUser);
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-4">
      <div className="bg-zinc-900 border border-green-500/30 rounded-lg shadow-2xl shadow-green-500/20 p-8 w-full max-w-md">
        <div className="mb-6 text-center">
          <div className="inline-block mb-3">
            <div className="w-16 h-16 mx-auto bg-green-500/10 rounded-full flex items-center justify-center border border-green-500/30">
              <svg className="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
              </svg>
            </div>
          </div>
          <h2 className="text-3xl font-bold text-green-500 mb-2">Log In</h2>
          <p className="text-gray-400 text-sm">Access your CodeMentor account</p>
        </div>
        
        <div className="space-y-4">
          <div>
            <label className="block text-green-400 text-sm font-semibold mb-2">
              Email
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              className="w-full px-4 py-2 bg-black border border-green-500/30 text-green-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent placeholder-gray-600"
              placeholder="Enter your email"
            />
          </div>
          
          <div>
            <label className="block text-green-400 text-sm font-semibold mb-2">
              Password
            </label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              className="w-full px-4 py-2 bg-black border border-green-500/30 text-green-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent placeholder-gray-600"
              placeholder="Enter your password"
            />
          </div>
          
          <button
            onClick={handleLogIn}
            className="w-full bg-green-600 text-black py-2 rounded-lg font-bold hover:bg-green-500 transition duration-200 shadow-lg shadow-green-500/30"
          >
            Log In
          </button>
        </div>
        
        <p className="text-center text-gray-400 mt-6 text-sm">
          Don't have an account?{' '}
          <button
            onClick={() => navigateTo('signup')}
            className="text-green-500 hover:text-green-400 font-semibold"
          >
            Sign Up
          </button>
        </p>
      </div>
    </div>
  );
}

export default LogIn;
