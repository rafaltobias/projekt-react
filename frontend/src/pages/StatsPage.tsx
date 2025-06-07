import React from 'react';
import StatsDisplay from '../components/StatsDisplay';

const StatsPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Header Section */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl mb-6">
            <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
            </svg>
          </div>          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Statystyki <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-emerald-600">Wizyt</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Kompleksowa analityka i wgląd w odwiedzających Twoją stronę internetową, 
            w tym wykresy, trendy i szczegółowe zestawienia wzorców wizyt.
          </p>
        </div>

        {/* Statistics Display */}
        <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
          <div className="bg-gradient-to-r from-green-500 to-emerald-600 p-6">            <h2 className="text-2xl font-bold text-white flex items-center">
              <svg className="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" />
              </svg>
              Pulpit analityczny
            </h2>
            <p className="text-green-100 mt-2">
              Interaktywne wykresy i szczegółowe statystyki odwiedzających
            </p>
          </div>
          
          <div className="p-8">
            <StatsDisplay />
          </div>
        </div>

        {/* Additional Info */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">            <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
              <svg className="w-5 h-5 mr-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
              </svg>
              Dane w czasie rzeczywistym
            </h3>
            <p className="text-gray-600">
              Wszystkie statystyki są aktualizowane w czasie rzeczywistym wraz z rejestrowaniem nowych wizyt. 
              Wykresy i grafy odzwierciedlają najnowsze dane o odwiedzających.
            </p>
          </div>
          
          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">            <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
              <svg className="w-5 h-5 mr-2 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0-7a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0-7a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
              </svg>
              Opcje eksportu
            </h3>
            <p className="text-gray-600">
              Eksportuj dane o odwiedzających jako pliki CSV do dalszej analizy 
              w zewnętrznych narzędziach lub systemach raportowania.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatsPage;
