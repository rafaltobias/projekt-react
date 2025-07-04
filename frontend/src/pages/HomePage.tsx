import React from 'react';
import { Link } from 'react-router-dom';

interface Feature {
  title: string;
  description: string;
  icon: React.ReactElement;
  link: string;
  linkText: string;
  bgGradient: string;
  hoverGradient: string;
}

interface AdditionalFeature {
  title: string;
  description: string;
  icon: string;
}

const HomePage: React.FC = () => {  const features: Feature[] = [
    {
      title: "Śledź wizyty",
      description: "Rejestruj wizyty na swoich stronach internetowych. Dodawaj opcjonalne tagi dla lepszej organizacji.",
      icon: (
        <svg className="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
        </svg>
      ),
      link: "/track",
      linkText: "Rozpocznij śledzenie",
      bgGradient: "from-blue-500 to-blue-600",
      hoverGradient: "from-blue-600 to-blue-700"
    },
    {
      title: "Zobacz statystyki",
      description: "Wizualizuj i analizuj swoje dane o wizytach za pomocą interaktywnych wykresów i grafów.",
      icon: (
        <svg className="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
          <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
        </svg>
      ),
      link: "/stats",
      linkText: "Zobacz statystyki",
      bgGradient: "from-green-500 to-green-600",
      hoverGradient: "from-green-600 to-green-700"
    },
    {
      title: "Zarządzaj tagami",
      description: "Twórz i organizuj tagi do kategoryzowania i segmentacji danych o wizytach.",
      icon: (
        <svg className="w-8 h-8 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M17.707 9.293a1 1 0 010 1.414l-7 7a1 1 0 01-1.414 0l-7-7A.997.997 0 012 10V5a3 3 0 013-3h5c.256 0 .512.098.707.293l7 7zM5 6a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
        </svg>
      ),
      link: "/tags",
      linkText: "Zarządzaj tagami",
      bgGradient: "from-purple-500 to-purple-600",
      hoverGradient: "from-purple-600 to-purple-700"
    }
  ];

  const additionalFeatures: AdditionalFeature[] = [
    {
      title: "Śledzenie wizyt",
      description: "Rejestruj i przechowuj informacje o wizytach",
      icon: "📊"
    },
    {
      title: "Zarządzanie tagami",
      description: "Organizuj wizyty za pomocą niestandardowych tagów",
      icon: "🏷️"
    },
    {
      title: "Analityka wizualna",
      description: "Wizualizuj dane za pomocą wykresów",
      icon: "📈"
    },
    {
      title: "Eksport danych",
      description: "Eksportuj swoje dane jako CSV",
      icon: "💾"
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 overflow-hidden">
        <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 lg:py-24">
          <div className="text-center">            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              <span className="block">Profesjonalny</span>
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">
                System Śledzenia Wizyt
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
              Śledź i analizuj wizyty na stronie internetowej z łatwością. Uzyskaj szczegółowe informacje o zachowaniu odwiedzających, 
              statystyki przeglądarek i metryki wydajności.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                to="/setup" 
                className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200"
              >
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.293l-3-3a1 1 0 00-1.414 1.414L10.586 9H7a1 1 0 100 2h3.586l-1.293 1.293a1 1 0 101.414 1.414l3-3a1 1 0 000-1.414z" clipRule="evenodd" />
                </svg>                Rozpocznij
              </Link>
              <Link 
                to="/analytics" 
                className="inline-flex items-center px-8 py-4 bg-white text-gray-700 font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200 border border-gray-200"
              >
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
                </svg>
                Zobacz analitykę
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Main Features Section */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Potężne funkcje
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Wszystko czego potrzebujesz do śledzenia, analizowania i zrozumienia odwiedzających Twoją stronę
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div 
                key={index}
                className="group relative bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 overflow-hidden border border-gray-100"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-gray-50 to-white opacity-50"></div>
                <div className="relative p-8">
                  <div className="flex items-center justify-center w-16 h-16 bg-gradient-to-br from-gray-100 to-gray-200 rounded-xl mb-6 group-hover:scale-110 transition-transform duration-200">
                    {feature.icon}
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-4">{feature.title}</h3>
                  <p className="text-gray-600 mb-8 leading-relaxed">{feature.description}</p>
                  <Link 
                    to={feature.link} 
                    className={`inline-flex items-center px-6 py-3 bg-gradient-to-r ${feature.bgGradient} hover:${feature.hoverGradient} text-white font-semibold rounded-lg shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200`}
                  >
                    {feature.linkText}
                    <svg className="w-4 h-4 ml-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Additional Features Section */}
      <div className="py-20 bg-gradient-to-br from-slate-50 to-blue-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Dodatkowe funkcje
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Kompleksowe narzędzia do pełnej analityki strony internetowej
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {additionalFeatures.map((item, index) => (
              <div 
                key={index}
                className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-1 border border-gray-100"
              >
                <div className="text-4xl mb-4">{item.icon}</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{item.title}</h3>
                <p className="text-gray-600 text-sm leading-relaxed">{item.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Stats Preview Section */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-3xl p-12 text-center text-white">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">
              Gotowy żeby zacząć?
            </h2>
            <p className="text-xl mb-8 max-w-2xl mx-auto opacity-90">
              Dołącz do tysięcy stron internetowych korzystających z naszej platformy analitycznej, aby lepiej zrozumieć swoich odwiedzających
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                to="/setup" 
                className="inline-flex items-center px-8 py-4 bg-white text-blue-600 font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200"
              >
                Konfiguruj śledzenie
              </Link>
              <a 
                href="http://localhost:5000/tracking-example"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center px-8 py-4 bg-transparent text-white font-semibold rounded-xl border-2 border-white hover:bg-white hover:text-blue-600 transition-all duration-200"              >
                Zobacz demo
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
