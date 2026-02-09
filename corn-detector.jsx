import React, { useState, useRef } from 'react';
import * as tf from '@tensorflow/tfjs';

const CornDiseaseDetector = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [modelLoaded, setModelLoaded] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);
  const modelRef = useRef(null);

  const CLASSES = {
    0: { name: 'Blight', fr: 'Mildiou', status: 'malade', emoji: '🍂', color: '#ef4444' },
    1: { name: 'Common_Rust', fr: 'Rouille Commune', status: 'malade', emoji: '🦠', color: '#f59e0b' },
    2: { name: 'Gray_Leaf_Spot', fr: 'Tache Grise', status: 'malade', emoji: '⚠️', color: '#f97316' },
    3: { name: 'Healthy', fr: 'Saine', status: 'saine', emoji: '✅', color: '#10b981' }
  };

  // Charger un modèle fictif (simulation)
  React.useEffect(() => {
    const loadModel = async () => {
      try {
        // Simulation de chargement de modèle
        await new Promise(resolve => setTimeout(resolve, 1000));
        setModelLoaded(true);
      } catch (error) {
        console.error('Erreur chargement modèle:', error);
      }
    };
    loadModel();
  }, []);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      handleImageSelect(file);
    }
  };

  const handleImageSelect = (file) => {
    setSelectedImage(file);
    const reader = new FileReader();
    reader.onload = (e) => {
      setImagePreview(e.target.result);
    };
    reader.readAsDataURL(file);
    setPrediction(null);
  };

  const handleFileInputChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleImageSelect(file);
    }
  };

  const analyzeImage = async () => {
    if (!selectedImage) return;

    setIsAnalyzing(true);
    
    // Simulation de l'analyse (remplacer par vrai modèle TensorFlow.js)
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Prédiction simulée (à remplacer par vraie prédiction)
    const predictedClass = Math.floor(Math.random() * 4);
    const confidence = 75 + Math.random() * 20; // 75-95%
    
    const probabilities = [0, 1, 2, 3].map(i => ({
      classIdx: i,
      className: CLASSES[i].fr,
      probability: i === predictedClass 
        ? confidence 
        : (100 - confidence) / 3 + Math.random() * 5
    }));

    setPrediction({
      classIdx: predictedClass,
      className: CLASSES[predictedClass].fr,
      status: CLASSES[predictedClass].status,
      emoji: CLASSES[predictedClass].emoji,
      color: CLASSES[predictedClass].color,
      confidence: confidence.toFixed(1),
      probabilities: probabilities.sort((a, b) => b.probability - a.probability)
    });

    setIsAnalyzing(false);
  };

  const resetAnalysis = () => {
    setSelectedImage(null);
    setImagePreview(null);
    setPrediction(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 p-4 md:p-8">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@400;500;600;700&display=swap');
        
        @keyframes slideUp {
          from { opacity: 0; transform: translateY(30px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
        
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
        
        @keyframes expandBar {
          from { width: 0; }
          to { width: var(--target-width); }
        }
        
        .animate-slideUp {
          animation: slideUp 0.6s ease-out;
        }
        
        .animate-fadeIn {
          animation: fadeIn 0.5s ease-out;
        }
        
        .animate-pulse {
          animation: pulse 2s ease-in-out infinite;
        }
        
        .animate-spin {
          animation: spin 1s linear infinite;
        }
        
        .prob-bar {
          animation: expandBar 0.8s ease-out forwards;
        }
        
        .title-font {
          font-family: 'Playfair Display', serif;
        }
        
        .body-font {
          font-family: 'Inter', sans-serif;
        }
        
        .glass-effect {
          background: rgba(255, 255, 255, 0.9);
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.5);
        }
        
        .drop-shadow-custom {
          filter: drop-shadow(0 20px 40px rgba(0, 0, 0, 0.1));
        }
      `}</style>

      <div className="max-w-5xl mx-auto">
        {/* En-tête */}
        <header className="text-center mb-12 animate-slideUp">
          <div className="inline-flex items-center gap-3 mb-4">
            <span className="text-6xl">🌽</span>
            <h1 className="title-font text-5xl md:text-7xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-600">
              CornScan
            </h1>
          </div>
          <p className="body-font text-xl md:text-2xl text-gray-600 max-w-2xl mx-auto">
            Détection instantanée des maladies du maïs par intelligence artificielle
          </p>
          <div className="mt-6 inline-flex items-center gap-2 px-4 py-2 rounded-full glass-effect">
            <span className={`w-2 h-2 rounded-full ${modelLoaded ? 'bg-emerald-500 animate-pulse' : 'bg-gray-400'}`}></span>
            <span className="body-font text-sm font-medium text-gray-700">
              {modelLoaded ? 'Modèle prêt' : 'Chargement...'}
            </span>
          </div>
        </header>

        {/* Zone principale */}
        <div className="glass-effect rounded-3xl shadow-2xl p-8 md:p-12 animate-slideUp drop-shadow-custom">
          {!prediction ? (
            <>
              {/* Zone d'upload */}
              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`
                  border-4 border-dashed rounded-2xl p-12 md:p-16 text-center cursor-pointer
                  transition-all duration-300 ease-out
                  ${isDragging 
                    ? 'border-emerald-500 bg-emerald-50 scale-105' 
                    : imagePreview
                    ? 'border-emerald-400 bg-gradient-to-br from-emerald-50 to-teal-50'
                    : 'border-gray-300 hover:border-emerald-400 hover:bg-gray-50'
                  }
                `}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleFileInputChange}
                  className="hidden"
                />

                {imagePreview ? (
                  <div className="animate-fadeIn">
                    <img 
                      src={imagePreview} 
                      alt="Preview" 
                      className="max-h-96 mx-auto rounded-xl shadow-lg mb-6"
                    />
                    <div className="inline-flex items-center gap-2 text-emerald-600 font-semibold">
                      <span className="text-2xl">✓</span>
                      <span>Image chargée • Prêt pour l'analyse</span>
                    </div>
                  </div>
                ) : (
                  <div className="animate-fadeIn">
                    <div className="text-8xl mb-6">📸</div>
                    <h3 className="title-font text-3xl font-bold text-gray-800 mb-3">
                      Déposez votre image ici
                    </h3>
                    <p className="body-font text-gray-600 text-lg mb-2">
                      ou cliquez pour sélectionner
                    </p>
                    <p className="body-font text-sm text-gray-400">
                      PNG, JPG, JPEG • Max 10MB
                    </p>
                  </div>
                )}
              </div>

              {/* Bouton analyser */}
              {imagePreview && (
                <button
                  onClick={analyzeImage}
                  disabled={isAnalyzing || !modelLoaded}
                  className={`
                    mt-8 w-full py-5 px-8 rounded-2xl font-bold text-lg text-white
                    transition-all duration-300 transform
                    ${isAnalyzing || !modelLoaded
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 hover:scale-105 shadow-lg hover:shadow-xl'
                    }
                  `}
                >
                  {isAnalyzing ? (
                    <span className="flex items-center justify-center gap-3">
                      <span className="w-5 h-5 border-3 border-white border-t-transparent rounded-full animate-spin"></span>
                      Analyse en cours...
                    </span>
                  ) : (
                    <span className="flex items-center justify-center gap-2">
                      <span className="text-2xl">🔬</span>
                      Analyser l'image
                    </span>
                  )}
                </button>
              )}
            </>
          ) : (
            /* Résultats */
            <div className="animate-fadeIn">
              {/* Image analysée */}
              <div className="mb-8">
                <img 
                  src={imagePreview} 
                  alt="Analysée" 
                  className="max-h-80 mx-auto rounded-2xl shadow-xl"
                />
              </div>

              {/* Résultat principal */}
              <div 
                className="rounded-2xl p-8 text-center text-white mb-8 shadow-xl"
                style={{ background: `linear-gradient(135deg, ${prediction.color} 0%, ${prediction.color}dd 100%)` }}
              >
                <div className="text-7xl mb-4">{prediction.emoji}</div>
                <h2 className="title-font text-4xl md:text-5xl font-black mb-3 uppercase">
                  Plante {prediction.status}
                </h2>
                <div className="text-2xl md:text-3xl font-semibold mb-2">
                  {prediction.className}
                </div>
                <div className="text-xl opacity-90">
                  Confiance: {prediction.confidence}%
                </div>
              </div>

              {/* Probabilités */}
              <div className="bg-white rounded-2xl p-8 mb-8 shadow-lg">
                <h3 className="title-font text-2xl font-bold mb-6 text-gray-800 flex items-center gap-2">
                  <span>📊</span>
                  Analyse détaillée
                </h3>
                <div className="space-y-4">
                  {prediction.probabilities.map((prob, idx) => (
                    <div key={idx}>
                      <div className="flex justify-between items-center mb-2">
                        <span className="body-font font-semibold text-gray-700">
                          {prob.className}
                        </span>
                        <span className="body-font font-bold text-gray-900">
                          {prob.probability.toFixed(1)}%
                        </span>
                      </div>
                      <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-gradient-to-r from-emerald-500 to-teal-500 rounded-full prob-bar"
                          style={{ 
                            '--target-width': `${prob.probability}%`,
                            width: `${prob.probability}%`
                          }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Bouton nouvelle analyse */}
              <button
                onClick={resetAnalysis}
                className="w-full py-5 px-8 rounded-2xl font-bold text-lg border-3 border-emerald-500 text-emerald-600 hover:bg-emerald-50 transition-all duration-300 transform hover:scale-105"
              >
                🔄 Analyser une nouvelle image
              </button>
            </div>
          )}
        </div>

        {/* Footer */}
        <footer className="text-center mt-12 animate-fadeIn">
          <p className="body-font text-gray-500 text-sm">
            Développé avec ❤️ pour aider les agriculteurs
          </p>
          <p className="body-font text-gray-400 text-xs mt-2">
            Powered by TensorFlow.js & React
          </p>
        </footer>
      </div>
    </div>
  );
};

export default CornDiseaseDetector;
