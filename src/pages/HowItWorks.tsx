import React from 'react';
import { FileText, Upload, Brain, CheckCircle, Clock } from 'lucide-react';

const steps = [
  {
    icon: FileText,
    title: "1. Décrivez votre offre",
    description: "Collez la description du poste ou les critères de recrutement dans l'espace prévu. Plus votre description est précise, meilleure sera l'analyse !"
  },
  {
    icon: Upload,
    title: "2. Transférez les CVs",
    description: "Déposez les CVs des candidats (formats PDF, Word ou image). Anto est capable d'extraire automatiquement les informations, même depuis des fichiers scannés."
  },
  {
    icon: Brain,
    title: "3. Analyse intelligente",
    description: "Anto lit tous les CVs, évalue les compétences, l'expérience, la formation et d'autres critères clés pour établir un score de correspondance."
  },
  {
    icon: CheckCircle,
    title: "4. Recommandation personnalisée",
    description: "Anto vous indique quel(s) candidat(s) correspond(ent) le mieux au poste, avec une explication en langage naturel pour justifier son choix."
  },
  {
    icon: Clock,
    title: "5. Décidez rapidement",
    description: "Vous gagnez un temps précieux pour prendre vos décisions de recrutement en toute confiance."
  }
];

const HowItWorks: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-12">
        <div className="bg-white rounded-lg shadow-md p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-12 text-center">
            Comment ça marche
          </h1>
          
          <div className="space-y-12">
            {steps.map((step, index) => (
              <div key={index} className="flex items-start">
                <div className="bg-indigo-100 p-3 rounded-full mr-6">
                  <step.icon className="h-6 w-6 text-indigo-600" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900 mb-2">
                    {step.title}
                  </h2>
                  <p className="text-gray-700 leading-relaxed">
                    {step.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default HowItWorks;