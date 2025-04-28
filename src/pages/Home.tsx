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
    setCandidates([]); // Clear previous results
    setErrors([]); // Clear previous errors

    try {
      // Prepare file content (assuming backend expects text content)
      const fileContents = await Promise.all(
        files.map(async (file) => ({
          name: file.name,
          content: await file.text(), // Reads file as text
        }))
      );

      // Use the Vercel backend URL from environment variables
      const backendUrl = import.meta.env.VITE_BACKEND_URL;
      if (!backendUrl) {
        throw new Error("Backend URL is not configured. Set VITE_BACKEND_URL environment variable in Netlify.");
      }

      // Fetch data from the Vercel backend
      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: {
          // Remove Supabase-specific Authorization if not needed by Vercel backend
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          job_description: jobDescription,
          // Assuming Vercel backend now accepts 'files' like Supabase did
          files: fileContents,
        }),
      });

      if (!response.ok) {
        // Handle potential errors from the Vercel backend
        const errorData = await response.text(); // Get more details on error
        console.error("Backend error response:", errorData);
        throw new Error(`L'analyse a échoué avec le statut ${response.status}. Réponse: ${errorData}`);
      }

      // Assuming the backend returns an object like { candidates: [], errors: [] }
      const data = await response.json();
      setCandidates(data.candidates || []); // Use candidates array from response
      setErrors(data.errors || []); // Use errors array from response

    } catch (error: any) {
      console.error('Error during analysis:', error);
      // Update the alert message for better feedback
      alert(`Une erreur est survenue lors de la communication avec le backend : ${error.message}`);
      setCandidates([]); // Clear results on error
      setErrors([]);
    } finally {
      setIsLoading(false);
    }
  };

  // The rest of the component remains the same as in your provided code snippet
  // (Introduction, JobDescriptionInput, FileUploader, ResultsSection rendering logic)
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