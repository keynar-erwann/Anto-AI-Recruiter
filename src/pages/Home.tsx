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

interface Error {
  filename: string;
  error: string;
}

const Home: React.FC = () => {
  const [jobDescription, setJobDescription] = useState('');
  const [files, setFiles] = useState<File[]>([]);
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [errors, setErrors] = useState<Error[]>([]);
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
    setCandidates([]);
    setErrors([]);

    try {
      const fileContents = await Promise.all(
        files.map(async (file) => ({
          name: file.name,
          content: await file.text(),
        }))
      );

      const backendUrl = "https://anto-ai-recruiter.vercel.app/analyze";
      if (!backendUrl) {
        throw new Error("L'URL du backend n'est pas configurée");
      }

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 50000);

      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          job_description: jobDescription,
          files: fileContents,
        }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        let errorMessage;
        try {
          const errorData = JSON.parse(errorText);
          errorMessage = errorData.detail || errorText;
        } catch {
          errorMessage = errorText;
        }
        throw new Error(`L'analyse a échoué avec le statut ${response.status}. Réponse: ${errorMessage}`);
      }

      const data = await response.json();
      
      if (data.candidates && Array.isArray(data.candidates)) {
        setCandidates(data.candidates);
      } else {
        console.error("Format de réponse invalide:", data);
        throw new Error("Format de réponse invalide du serveur");
      }
      
      if (data.errors && Array.isArray(data.errors)) {
        setErrors(data.errors);
      }

    } catch (error: any) {
      console.error('Erreur pendant l\'analyse:', error);
      let errorMessage = error.message;
      if (error.name === 'AbortError') {
        errorMessage = "L'analyse a pris trop de temps. Veuillez réessayer avec moins de CV ou des CV plus courts.";
      }
      alert(`Une erreur est survenue lors de la communication avec le backend : ${errorMessage}`);
      setCandidates([]);
      setErrors([{
        filename: "system",
        error: errorMessage
      }]);
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