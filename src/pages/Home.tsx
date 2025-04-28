import React, { useState } from 'react';
import Introduction from '../components/Introduction';
import JobDescriptionInput from '../components/JobDescriptionInput';
import FileUploader from '../components/FileUploader';
import ResultsSection from '../components/ResultsSection';

interface Candidate {
  filename: string;
  score: number;
  skills: number;
  experience: number;
  education: number;
  explanation: string;
  error?: string;
}

const Home: React.FC = () => {
  const [jobDescription, setJobDescription] = useState('');
  const [files, setFiles] = useState<File[]>([]);
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [errors, setErrors] = useState<Candidate[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isAnalyzed, setIsAnalyzed] = useState(false);

  const handleAnalyze = async () => {
    if (!jobDescription) {
      alert('Veuillez coller la description de l\'emploi avant de continuer.');
      return;
    }

    if (files.length === 0) {
      alert('Veuillez téléverser au moins un CV.');
      return;
    }

    setIsLoading(true);
    setIsAnalyzed(true);

    try {
      // Convert files to base64
      const fileContents = await Promise.all(
        files.map(async (file) => ({
          name: file.name,
          content: await file.text()
        }))
      );

      const response = await fetch(`${import.meta.env.VITE_SUPABASE_URL}/functions/v1/analyze`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${import.meta.env.VITE_SUPABASE_ANON_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          job_description: jobDescription,
          files: fileContents,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze CVs');
      }

      const data = await response.json();
      setCandidates(data.candidates || []);
      setErrors(data.errors || []);
    } catch (error) {
      console.error('Error:', error);
      alert('Une erreur est survenue lors de l\'analyse des CVs.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex-grow px-4 sm:px-6 py-8">
      <div className="max-w-7xl mx-auto">
        <Introduction />
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <JobDescriptionInput 
            value={jobDescription} 
            onChange={setJobDescription} 
          />
          
          <FileUploader 
            onFilesSelected={setFiles} 
          />
        </div>
        
        <div className="mt-8 flex justify-center">
          <button 
            onClick={handleAnalyze}
            disabled={isLoading}
            className={`
              px-6 py-3 rounded-lg font-semibold text-white
              transition-all transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-2
              ${isLoading 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-gradient-to-r from-indigo-600 to-indigo-800 shadow-md hover:shadow-lg focus:ring-indigo-500'
              }
            `}
          >
            {isLoading ? 'Analyse en cours...' : 'Analyser les CVs'}
          </button>
        </div>
        
        {isAnalyzed && (
          <div className="mt-10">
            <ResultsSection 
              candidates={candidates} 
              errors={errors} 
              isLoading={isLoading} 
            />
          </div>
        )}
      </div>
    </main>
  );
};

export default Home;