import React, { useState } from 'react';
import TagForm from '../components/TagForm';
import TagList from '../components/TagList';
import { Tag } from '../api/types';

const TagsPage: React.FC = () => {
  const [refreshFlag, setRefreshFlag] = useState<number>(0);

  const handleTagCreated = (tag?: Tag): void => {
    // Trigger refresh of the tag list
    setRefreshFlag(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header Section */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg flex items-center justify-center shadow-lg">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
            </div>
          </div>          <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 via-green-700 to-emerald-800 bg-clip-text text-transparent mb-4">
            Zarządzaj tagami
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Organizuj swoje dane śledzenia za pomocą niestandardowych tagów i kategorii, aby uzyskać lepszy wgląd
          </p>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Tag Form Section */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-xl border border-gray-100">
              {/* Form Header */}
              <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-t-2xl p-6">                <h2 className="text-xl font-bold text-white flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  Utwórz nowy tag
                </h2>
                <p className="text-green-100 text-sm mt-1">
                  Dodawaj tagi do kategoryzowania danych śledzenia
                </p>
              </div>
              
              {/* Form Content */}
              <div className="p-6">
                <TagForm onTagCreated={handleTagCreated} />
              </div>
            </div>

            {/* Tag Usage Tips */}
            <div className="mt-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">              <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                <svg className="w-5 h-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                Wskazówki dotyczące tagów
              </h3>
              <ul className="text-sm text-gray-600 space-y-2">
                <li className="flex items-start">
                  <span className="w-1.5 h-1.5 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  Używaj opisowych nazw dla lepszej organizacji
                </li>
                <li className="flex items-start">
                  <span className="w-1.5 h-1.5 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  Tagi pomagają filtrować i analizować dane o odwiedzających
                </li>
                <li className="flex items-start">
                  <span className="w-1.5 h-1.5 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  Spójne nazewnictwo poprawia raportowanie
                </li>
              </ul>
            </div>
          </div>
          
          {/* Tag List Section */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-2xl shadow-xl border border-gray-100">
              {/* List Header */}
              <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-t-2xl p-6">                <h2 className="text-xl font-bold text-white flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                  </svg>
                  Twoje tagi
                </h2>
                <p className="text-indigo-100 text-sm mt-1">
                  Zarządzaj i organizuj swoje istniejące tagi
                </p>
              </div>
              
              {/* List Content */}
              <div className="p-6">
                <TagList refreshFlag={refreshFlag} onRefresh={handleTagCreated} />
              </div>
            </div>
          </div>
        </div>

        {/* Additional Features */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-shadow duration-200">
            <div className="flex items-center mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-lg flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 4V2a1 1 0 011-1h4a1 1 0 011 1v2m-6 0h8m-8 0a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V6a2 2 0 00-2-2m-6 4h4" />
              </svg>
              </div>              <h3 className="text-lg font-semibold text-gray-900 ml-3">Operacje masowe</h3>
            </div>
            <p className="text-gray-600 text-sm">
              Zarządzaj wieloma tagami jednocześnie dzięki funkcjom masowej edycji, usuwania i organizacji
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-shadow duration-200">
            <div className="flex items-center mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-pink-400 to-red-500 rounded-lg flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>              <h3 className="text-lg font-semibold text-gray-900 ml-3">Szybkie akcje</h3>
            </div>
            <p className="text-gray-600 text-sm">
              Natychmiastowo stosuj tagi do danych śledzenia za pomocą akcji jednym kliknięciem i skrótów
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-shadow duration-200">
            <div className="flex items-center mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-indigo-400 to-blue-500 rounded-lg flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>              <h3 className="text-lg font-semibold text-gray-900 ml-3">Analityka tagów</h3>
            </div>
            <p className="text-gray-600 text-sm">
              Wyświetlaj szczegółową analitykę dla każdego tagu, aby zrozumieć wzorce zachowań odwiedzających
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TagsPage;
