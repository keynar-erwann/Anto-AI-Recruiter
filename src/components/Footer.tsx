import React from 'react';
import { Heart } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-50 py-8 mt-12 border-t border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-gray-500 text-sm">
              © {new Date().getFullYear()} Anto - Recruteur IA. Tous droits réservés.
            </p>
          </div>
          
          <div className="flex items-center">
            <span className="text-gray-500 text-sm mr-2">Créé avec</span>
            <Heart className="h-4 w-4 text-red-500 animate-pulse" />
            <span className="text-gray-500 text-sm ml-2">et IA</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;