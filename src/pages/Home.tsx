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
  // ... existing code ...

  const handleAnalyze = async () => {
    if (!jobDescription) {
      alert('Please paste the job description before continuing.');
      return;
    }

    if (files.length === 0) {
      alert('Please upload at least one resume.');
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
        throw new Error("Backend URL is not configured");
      }

      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          job_description: jobDescription,
          files: fileContents,
        }),
        credentials: 'include',
        signal: AbortSignal.timeout(30000), // 30 second timeout
      });

      if (!response.ok) {
        const errorText = await response.text();
        let errorMessage;
        try {
          const errorData = JSON.parse(errorText);
          errorMessage = errorData.detail || errorText;
        } catch {
          errorMessage = errorText;
        }
        throw new Error(`Analysis failed with status ${response.status}. Response: ${errorMessage}`);
      }

      const data = await response.json();
      
      if (data.candidates && Array.isArray(data.candidates)) {
        setCandidates(data.candidates);
      } else {
        console.error("Invalid response format:", data);
        throw new Error("Invalid response format from server");
      }
      
      if (data.errors && Array.isArray(data.errors)) {
        setErrors(data.errors);
      }

    } catch (error: any) {
      console.error('Error during analysis:', error);
      alert(`Error communicating with backend: ${error.message}`);
      setCandidates([]);
      setErrors([{
        filename: "system",
        error: error.message
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  // ... existing code ...

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
            {isLoading ? 'Analysis in progress...' : 'Analyze Resumes'}
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