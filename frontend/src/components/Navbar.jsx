import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-surface-900/80 backdrop-blur-xl border-b border-primary-500/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center">
              <span className="text-white font-bold text-sm">AI</span>
            </div>
            <span className="text-lg font-bold gradient-text">Resume Analyzer</span>
          </Link>

          <div className="flex items-center gap-4">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="text-sm text-surface-300 hover:text-white transition-colors">Dashboard</Link>
                <Link to="/upload" className="text-sm text-surface-300 hover:text-white transition-colors">Upload</Link>
                {user?.is_admin && (
                  <Link to="/admin" className="text-sm text-accent-400 hover:text-accent-300 transition-colors">Admin</Link>
                )}
                <div className="flex items-center gap-3 ml-4 pl-4 border-l border-surface-800">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-400 to-accent-400 flex items-center justify-center">
                    <span className="text-white text-xs font-bold">{user?.name?.[0]?.toUpperCase()}</span>
                  </div>
                  <span className="text-sm text-surface-300 hidden sm:block">{user?.name}</span>
                  <button onClick={handleLogout} className="text-xs text-surface-500 hover:text-red-400 transition-colors">Logout</button>
                </div>
              </>
            ) : (
              <>
                <Link to="/login" className="btn-secondary text-sm py-2 px-4">Login</Link>
                <Link to="/register" className="btn-primary text-sm py-2 px-4">Sign Up</Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
