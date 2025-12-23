import { useState } from 'react';

function SignUp({ navigateTo }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: ''
  });

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSignUp = () => {
    console.log('Sign Up Data:', formData);
    // TODO: Add your sign up API call here
    // After successful signup, redirect to login
    navigateTo('login');
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-4">
      <div className="bg-zinc-900 border border-green-500/30 rounded-lg shadow-2xl shadow-green-500/20 p-8 w-full max-w-md">
        <div className="mb-6 text-center">
          <div className="inline-block mb-3">
            <div className="w-16 h-16 mx-auto bg-green-500/10 rounded-full flex items-center justify-center border border-green-500/30">
              <svg className="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
          </div>
          <h2 className="text-3xl font-bold text-green-500 mb-2">Sign Up</h2>
          <p className="text-gray-400 text-sm">Create your AI account</p>
        </div>
        
        <div className="space-y-4">
          <div>
            <label className="block text-green-400 text-sm font-semibold mb-2">
              Name
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              className="w-full px-4 py-2 bg-black border border-green-500/30 text-green-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent placeholder-gray-600"
              placeholder="Enter your name"
            />
          </div>
          
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
            onClick={handleSignUp}
            className="w-full bg-green-600 text-black py-2 rounded-lg font-bold hover:bg-green-500 transition duration-200 shadow-lg shadow-green-500/30"
          >
            Sign Up
          </button>
        </div>
        
        <p className="text-center text-gray-400 mt-6 text-sm">
          Already have an account?{' '}
          <button
            onClick={() => navigateTo('login')}
            className="text-green-500 hover:text-green-400 font-semibold"
          >
            Log In
          </button>
        </p>
      </div>
    </div>
  );
}

export default SignUp;