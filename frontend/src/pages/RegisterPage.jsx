import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { registerUser } from '../services/api';
import { toast } from 'react-toastify';

export default function RegisterPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password.length < 6) { toast.error('Password must be at least 6 characters'); return; }
    setLoading(true);
    try {
      const { data } = await registerUser({ name, email, password });
      login(data.user, data.access_token);
      toast.success('Account created successfully!');
      navigate('/upload');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="absolute top-20 right-1/4 w-64 h-64 bg-accent-500/10 rounded-full blur-3xl" />
      <div className="absolute bottom-20 left-1/4 w-80 h-80 bg-primary-500/10 rounded-full blur-3xl" />
      
      <div className="glass-card w-full max-w-md animate-fade-in relative">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-accent-500 to-primary-500 flex items-center justify-center mx-auto mb-4">
            <span className="text-white text-2xl">🚀</span>
          </div>
          <h1 className="text-2xl font-bold text-white">Create Account</h1>
          <p className="text-surface-400 text-sm mt-1">Start analyzing your resume</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-sm text-surface-300 mb-1 block">Full Name</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)}
              className="input-field" placeholder="John Doe" required />
          </div>
          <div>
            <label className="text-sm text-surface-300 mb-1 block">Email</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)}
              className="input-field" placeholder="you@example.com" required />
          </div>
          <div>
            <label className="text-sm text-surface-300 mb-1 block">Password</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)}
              className="input-field" placeholder="••••••••" required minLength={6} />
          </div>
          <button type="submit" disabled={loading} className="btn-primary w-full py-3">
            {loading ? <span className="flex items-center justify-center gap-2"><div className="spinner w-5 h-5" /> Creating...</span> : 'Create Account'}
          </button>
        </form>

        <p className="text-center text-sm text-surface-400 mt-6">
          Already have an account? <Link to="/login" className="text-primary-400 hover:text-primary-300">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
