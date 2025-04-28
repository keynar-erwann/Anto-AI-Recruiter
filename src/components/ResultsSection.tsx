import React from 'react';
import CandidateCard from './CandidateCard';
import { Users, AlertTriangle } from 'lucide-react';

interface Candidate {
  filename: string;
  score: number;
  skills: number;
  experience: number;
  education: number;
  explanation: string;
  error?: string;
}

interface ResultsSectionProps {
  candidates: Candidate[];
  errors: Candidate[];
  isLoading: boolean;
}

const ResultsSection: React.FC<ResultsSectionProps> = ({ candidates, errors, isLoading }) => {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 text-center">
        <div className="animate-spin h-10 w-10 border-4 border-indigo-500 border-t-transparent rounded-full mx-auto mb-4"></div>
        <p className="text-gray-600">Analyse des CVs en cours...</p>
      </div>
    );
  }

  if (candidates.length === 0 && errors.length === 0) {
    return null;
  }

  const sortedCandidates = [...candidates].sort((a, b) => b.score - a.score);
  const bestCandidates = sortedCandidates.filter(c => c.score >= 70);

  return (
    <div className="space-y-6 animate-fadeIn">
      {bestCandidates.length > 0 && (
        <div className="bg-indigo-50 p-5 rounded-lg border border-indigo-100">
          <div className="flex items-center mb-4">
            <div className="bg-indigo-100 p-2 rounded-full">
              <Users className="h-6 w-6 text-indigo-700" />
            </div>
            <h3 className="ml-3 text-lg font-semibold text-indigo-900">
              {bestCandidates.length === 1 
                ? "Meilleur candidat identifié" 
                : `${bestCandidates.length} meilleurs candidats identifiés`}
            </h3>
          </div>
          
          <p className="text-indigo-800 mb-3">
            {bestCandidates.length === 1 
              ? "D'après mon analyse, ce candidat est particulièrement adapté pour ce poste."
              : "D'après mon analyse, ces candidats sont particulièrement adaptés pour ce poste."}
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {bestCandidates.map((candidate, index) => (
              <CandidateCard
                key={index}
                filename={candidate.filename}
                score={candidate.score}
                skills={candidate.skills}
                experience={candidate.experience}
                education={candidate.education}
                explanation={candidate.explanation}
                isTop={true}
              />
            ))}
          </div>
        </div>
      )}

      {sortedCandidates.length > bestCandidates.length && (
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Autres candidats</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {sortedCandidates
              .filter(c => c.score < 70)
              .map((candidate, index) => (
                <CandidateCard
                  key={index}
                  filename={candidate.filename}
                  score={candidate.score}
                  skills={candidate.skills}
                  experience={candidate.experience}
                  education={candidate.education}
                  explanation={candidate.explanation}
                />
              ))}
          </div>
        </div>
      )}

      {errors.length > 0 && (
        <div className="mt-8">
          <div className="flex items-center mb-4">
            <AlertTriangle className="h-5 w-5 text-amber-500 mr-2" />
            <h3 className="text-lg font-semibold text-gray-800">Problèmes détectés</h3>
          </div>
          
          <div className="bg-amber-50 rounded-lg p-4 border border-amber-100">
            <p className="text-amber-800 mb-3">Certains fichiers n'ont pas pu être analysés :</p>
            <ul className="list-disc pl-5 space-y-1">
              {errors.map((error, index) => (
                <li key={index} className="text-gray-700">
                  <span className="font-medium">{error.filename}</span>: {error.error}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsSection;