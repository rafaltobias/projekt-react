import React, { useState, useEffect } from 'react';

interface ConsentPopupProps {
  onConsentDecision?: (granted: boolean) => void;
}

const ConsentPopup: React.FC<ConsentPopupProps> = ({ onConsentDecision }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Check if consent decision has already been made
    const consentStatus = localStorage.getItem('data_sharing_consent');
    if (!consentStatus) {
      // Show popup after a short delay
      const timer = setTimeout(() => {
        setIsVisible(true);
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleAccept = () => {
    localStorage.setItem('data_sharing_consent', 'granted');
    localStorage.setItem('consent_timestamp', new Date().toISOString());
    setIsVisible(false);
    if (onConsentDecision) {
      onConsentDecision(true);
    }
    // Reload to enable tracking
    window.location.reload();
  };

  const handleDecline = () => {
    localStorage.setItem('data_sharing_consent', 'denied');
    localStorage.setItem('consent_timestamp', new Date().toISOString());
    setIsVisible(false);
    if (onConsentDecision) {
      onConsentDecision(false);
    }
  };

  if (!isVisible) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black bg-opacity-50"></div>
      
      {/* Popup */}
      <div className="relative bg-white rounded-2xl shadow-2xl max-w-lg mx-4 p-8 border border-gray-200">
        {/* Header with Icon */}
        <div className="flex items-center mb-6">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center mr-4">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900">Udostępnienie danych</h2>
        </div>

        {/* Content */}
        <div className="mb-8">
          <p className="text-gray-700 leading-relaxed mb-4">
            Ta strona zbiera dane o odwiedzinach w celach <strong>pracy inżynierskiej</strong>. 
            Zebrane informacje będą wykorzystane wyłącznie do analizy ruchu na stronie 
            i przygotowania pracy dyplomowej.
          </p>
          
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
            <h4 className="font-semibold text-blue-900 mb-2">Co zbieramy:</h4>
            <ul className="text-blue-800 text-sm space-y-1">
              <li>• URL odwiedzanych stron</li>
              <li>• Typ przeglądarki i systemu operacyjnego</li>
              <li>• Typ urządzenia (desktop/mobile/tablet)</li>
              <li>• Podstawowe informacje o sesji</li>
            </ul>
          </div>

          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h4 className="font-semibold text-green-900 mb-2">Gwarancje prywatności:</h4>
            <ul className="text-green-800 text-sm space-y-1">
              <li>• Brak zbierania danych osobowych</li>
              <li>• Dane używane tylko do celów naukowych</li>
              <li>• Zgodność z przepisami RODO</li>
              <li>• Możliwość cofnięcia zgody</li>
            </ul>
          </div>
        </div>

        {/* Buttons */}
        <div className="flex flex-col sm:flex-row gap-3">
          <button
            onClick={handleAccept}
            className="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl"
          >
            <div className="flex items-center justify-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Wyrażam zgodę
            </div>
          </button>
          
          <button
            onClick={handleDecline}
            className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-3 px-6 rounded-lg transition-all duration-200 border border-gray-300"
          >
            <div className="flex items-center justify-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
              Nie wyrażam zgody
            </div>
          </button>
        </div>

        {/* Footer note */}
        <p className="text-xs text-gray-500 mt-4 text-center">
          Decyzję można zmienić w każdej chwili poprzez wyczyszczenie danych przeglądarki
        </p>
      </div>
    </div>
  );
};

export default ConsentPopup;
