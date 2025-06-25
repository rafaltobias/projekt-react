# Environment Configuration Setup

## Problem
Aplikacja miała hardkodowane URL-e API (`http://localhost:5000`) w wielu miejscach, co utrudniało wdrażanie na różnych środowiskach.

## Rozwiązanie

### Frontend (React)
1. **Utworzono plik konfiguracyjny**: `frontend/src/config/environment.ts`
   - Centralizuje konfigurację środowiskową
   - Używa zmiennych środowiskowych React (`REACT_APP_*`)
   - Zawiera helper funkcje do tworzenia endpointów

2. **Poprawiono pliki używające hardkodowanych URL-ów**:
   - `frontend/src/api/apiService.ts`
   - `frontend/src/api/trackingService.ts`
   - `frontend/src/pages/TrackingSetupPage.tsx`

3. **Konfiguracja środowiskowa**:
   - `frontend/.env` - zawiera `REACT_APP_API_URL=http://localhost:5000`
   - `frontend/.env.example` - przykład konfiguracji dla różnych środowisk

### Backend (Flask)
1. **Rozszerzono konfigurację**: `backend/config.py`
   - Dodano `API_BASE_URL` z możliwością konfiguracji przez zmienną środowiskową

2. **Dynamiczne serwowanie skryptów JavaScript**:
   - Zmodyfikowano endpointy w `backend/routes/tracking_routes.py`:
     - `/static/tracker.js`
     - `/static/tracker.min.js`
     - `/static/tracker-with-tags.min.js`
     - `/static/tag-manager.js`
     - `/tracking-example`
   
   - Skrypty są teraz serwowane z dynamicznie zastępowanymi URL-ami na podstawie konfiguracji

3. **Konfiguracja środowiskowa**:
   - `backend/.env` - zawiera `API_BASE_URL=http://localhost:5000`
   - `backend/.env.example` - przykład konfiguracji dla różnych środowisk

## Korzyści
- **Elastyczność wdrażania**: Łatwa zmiana URL-ów bez modyfikacji kodu
- **Bezpieczeństwo**: Wrażliwe dane w zmiennych środowiskowych
- **Maintainability**: Centralna konfiguracja zamiast rozproszonej po całym kodzie
- **Środowiska**: Łatwe przełączanie między dev/staging/production

## Użycie

### Development
Pozostaw domyślne wartości w plikach `.env`

### Production
Ustaw odpowiednie URL-e w zmiennych środowiskowych:
```bash
# Frontend
REACT_APP_API_URL=https://your-domain.com

# Backend
API_BASE_URL=https://your-domain.com
```

### Staging
```bash
# Frontend
REACT_APP_API_URL=https://staging.your-domain.com

# Backend
API_BASE_URL=https://staging.your-domain.com
```
