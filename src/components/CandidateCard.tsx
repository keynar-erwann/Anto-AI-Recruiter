import React from 'react';
import ProgressRing from './ProgressRing';
import { UserCheck, Lightbulb, GraduationCap, Book } from 'lucide-react';

interface CandidateProps {
  filename: string;
  score: number;
  skills: number;
  experience: number;
  education: number;
  explanation: string;
  isTop?: boolean;
}

const CandidateCard: React.FC<CandidateProps> = ({
  filename,
  score,
  skills,
  experience,
  education,
  explanation,
  isTop = false,
}) => {
  // Extract just the filename without the extension
  const name = filename.split('.').slice(0, -1).join('.');
  
  // Determine the color scheme based on the score
  const getScoreColor = (score: number) => {
    if (score >= 90) return 'stroke-emerald-500';
    if (score >= 75) return 'stroke-indigo-600';
    if (score >= 60) return 'stroke-amber-500';
    return 'stroke-gray-500';
  };

  return (
    <div className={`bg-white rounded-lg shadow-md overflow-hidden transition-all hover:shadow-lg
      ${isTop ? 'border-l-4 border-emerald-500' : ''}`}>
      <div className="p-5">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4">
          <div>
            <h3 className="font-semibold text-gray-800 text-lg">{name}</h3>
            <p className="text-gray-500 text-sm">{filename}</p>
          </div>
          
          <div className="mt-3 sm:mt-0">
            <ProgressRing 
              progress={score} 
              size={56} 
              strokeWidth={5} 
              color={getScoreColor(score)}
              className="animate-fadeIn"
            />
          </div>
        </div>
        
        <div className="grid grid-cols-3 gap-2 mb-4">
          <div className="flex flex-col items-center p-2 bg-gray-50 rounded">
            <div className="flex items-center mb-1">
              <Lightbulb className="h-4 w-4 text-amber-500 mr-1" />
              <span className="text-xs text-gray-500">Compétences</span>
            </div>
            <span className="font-medium">{skills}%</span>
          </div>
          
          <div className="flex flex-col items-center p-2 bg-gray-50 rounded">
            <div className="flex items-center mb-1">
              <UserCheck className="h-4 w-4 text-blue-500 mr-1" />
              <span className="text-xs text-gray-500">Expérience</span>
            </div>
            <span className="font-medium">{experience}%</span>
          </div>
          
          <div className="flex flex-col items-center p-2 bg-gray-50 rounded">
            <div className="flex items-center mb-1">
              <GraduationCap className="h-4 w-4 text-indigo-500 mr-1" />
              <span className="text-xs text-gray-500">Formation</span>
            </div>
            <span className="font-medium">{education}%</span>
          </div>
        </div>
        
        <div className="border-t border-gray-100 pt-3">
          <div className="flex items-start">
            <Book className="h-5 w-5 text-gray-400 mr-2 mt-0.5 flex-shrink-0" />
            <p className="text-gray-600 text-sm">{explanation}</p>
          </div>
        </div>
        
        {isTop && (
          <div className="mt-4 bg-emerald-50 p-3 rounded-md flex items-center">
            <div className="bg-emerald-100 rounded-full p-1 mr-2">
              <UserCheck className="h-4 w-4 text-emerald-700" />
            </div>
            <p className="text-emerald-800 text-sm font-medium">Meilleur candidat pour ce poste</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default CandidateCard;