import React from 'react';
import { FileText } from 'lucide-react';

interface JobDescriptionInputProps {
  value: string;
  onChange: (value: string) => void;
}

const JobDescriptionInput: React.FC<JobDescriptionInputProps> = ({ value, onChange }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-5 mb-6 transition-all hover:shadow-lg">
      <div className="flex items-center mb-3">
        <FileText className="h-5 w-5 text-indigo-600 mr-2" />
        <h3 className="text-lg font-medium text-gray-800">Description de l'emploi</h3>
      </div>
      <textarea
        className="w-full h-48 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none transition-all"
        placeholder="Copiez-collez ici la description complète du poste..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
};

export default JobDescriptionInput;