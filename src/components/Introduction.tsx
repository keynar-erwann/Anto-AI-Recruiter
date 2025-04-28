import React from 'react';
import { MessageCircle } from 'lucide-react';

const Introduction: React.FC = () => {
  return (
    <div className="bg-white rounded-lg shadow-md p-5 mb-8 border-l-4 border-indigo-500 animate-fadeIn">
      <div className="flex items-start">
        <div className="bg-indigo-100 p-3 rounded-full mr-4">
          <MessageCircle className="h-6 w-6 text-indigo-700" />
        </div>
        <div>
          <h2 className="text-lg font-semibold text-gray-800 mb-2">
            Bonjour ! Je suis <span className="text-indigo-600">Anto</span>, votre recruteur IA
          </h2>
          <p className="text-gray-600">
            Transférez une <strong>description de l'emploi</strong> ainsi que quelques <strong>CVs</strong> (PDF, Word ou images)
            et je vous dirai <strong>quel(s) candidat(s)</strong> sont le mieux adaptés pour ce poste.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Introduction;