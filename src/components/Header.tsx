import React from 'react';
import { Brain } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

const Header: React.FC = () => {
  const location = useLocation();
  
  return (
    <header className="bg-gradient-to-r from-indigo-900 to-indigo-700 text-white py-6 px-4 sm:px-6 shadow-md">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link to="/" className="flex items-center">
          <Brain className="h-8 w-8 mr-3" />
          <div>
            <h1 className="text-2xl font-bold">Anto</h1>
            <p className="text-indigo-200 text-sm">Recruteur IA</p>
          </div>
        </Link>
        <nav>
          <ul className="flex space-x-6">
            <li>
              <Link 
                to="/how-it-works" 
                className={`text-sm font-medium transition-opacity ${
                  location.pathname === '/how-it-works' 
                    ? 'opacity-100' 
                    : 'opacity-80 hover:opacity-100'
                }`}
              >
                Comment ça marche
              </Link>
            </li>
            <li>
              <Link 
                to="/about" 
                className={`text-sm font-medium transition-opacity ${
                  location.pathname === '/about' 
                    ? 'opacity-100' 
                    : 'opacity-80 hover:opacity-100'
                }`}
              >
                À propos
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;