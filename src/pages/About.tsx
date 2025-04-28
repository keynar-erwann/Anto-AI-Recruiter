import React from 'react';
import { Bot } from 'lucide-react';

const About: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-12">
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="flex items-center mb-8">
            <div className="bg-indigo-100 p-3 rounded-full mr-4">
              <Bot className="h-8 w-8 text-indigo-600" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900">
              Anto, votre recruteur IA personnalisé
            </h1>
          </div>
          
          <div className="prose prose-lg prose-indigo max-w-none">
            <p className="text-gray-700 leading-relaxed">
              Anto est une intelligence artificielle conçue pour vous aider à sélectionner rapidement les meilleurs candidats pour vos offres d'emploi. Grâce à l'analyse intelligente de CVs en formats PDF, Word ou même images, Anto vous fournit en quelques secondes une recommandation claire et argumentée.
            </p>
            
            <p className="text-gray-700 leading-relaxed">
              Fini les longues heures à trier manuellement des candidatures : Anto lit, comprend, compare et vous propose les meilleurs profils en fonction de vos besoins.
            </p>
            
            <p className="text-gray-700 leading-relaxed">
              Simple, rapide, efficace — Anto est votre assistant recrutement nouvelle génération.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default About;