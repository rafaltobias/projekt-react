# Migracja do shadcn/ui

## Przegląd zmian

Aplikacja została pomyślnie zmigrowała z czystego Tailwind CSS na shadcn/ui dla bardziej spójnej i profesjonalnej biblioteki komponentów.

## Zainstalowane zależności

### Core Dependencies
- `@radix-ui/react-slot` - Podstawowy komponent slot dla kompozycji
- `@radix-ui/react-select` - Komponenty select/dropdown
- `class-variance-authority` - CVA dla wariantów komponentów
- `clsx` - Utility do łączenia klas CSS
- `tailwind-merge` - Merge'owanie klas Tailwind
- `lucide-react` - Biblioteka ikon
- `tailwindcss-animate` - Plugin animacji dla Tailwind

## Utworzone komponenty shadcn/ui

### `/src/components/ui/`
1. **button.tsx** - Komponenty przycisków z różnymi wariantami
   - Variants: default, destructive, outline, secondary, ghost, link
   - Sizes: default, sm, lg, icon

2. **card.tsx** - Komponenty kart
   - Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter

3. **input.tsx** - Stylowane pola input

4. **textarea.tsx** - Stylowane pola textarea

5. **select.tsx** - Kompleksowe komponenty select z Radix UI

### Utility functions
- `/src/lib/utils.ts` - Funkcja `cn()` do łączenia klas CSS

## Konfiguracja

### Tailwind CSS (`tailwind.config.js`)
- Dodano obsługę dark mode
- Rozszerzono palette kolorów z CSS variables
- Dodano animations i border radius variables
- Skonfigurowano plugin `tailwindcss-animate`

### CSS Variables (`src/input.css`)
- Dodano kompletny zestaw CSS custom properties dla:
  - Kolory (background, foreground, primary, secondary, etc.)
  - Border radius variables
  - Light/dark mode support

### TypeScript (`tsconfig.json`)
- Skonfigurowano path aliases (`@/*` -> `./src/*`)
- Uwaga: W Create React App aliasy wymagają relatywnych ścieżek

### shadcn/ui Config (`components.json`)
- Style: default
- CSS variables: true
- Base color: slate
- Aliases skonfigurowane dla komponentów i utils

## Zmigrowane komponenty

### 1. TagForm.tsx
**Przed:** Surowe HTML z Tailwind classes
```tsx
<div className="bg-white p-8 rounded-xl shadow-lg">
  <input className="w-full px-4 py-3 border..." />
  <button className="w-full bg-gradient-to-r...">
```

**Po:** shadcn/ui komponenty
```tsx
<Card className="hover:shadow-xl transition-shadow duration-200">
  <CardHeader>
    <CardTitle>Create New Tag</CardTitle>
  </CardHeader>
  <CardContent>
    <Input placeholder="Enter a name for your tag..." />
    <Button>Create Tag</Button>
  </CardContent>
</Card>
```

### 2. StatsDisplay.tsx (częściowo)
- Zmigrowany header i podstawowe karty na shadcn/ui Card komponenty
- Zachowano wykresy Chart.js bez zmian
- Zamieniono button na shadcn Button

## Korzyści migracji

### 1. **Spójność designu**
- Jednolity system designu w całej aplikacji
- Przygotowane warianty komponentów
- Konsystentne spacing i typography

### 2. **Accessibility**
- Komponenty Radix UI mają wbudowaną dostępność
- Proper ARIA attributes
- Keyboard navigation support

### 3. **Developer Experience**
- TypeScript support out of the box
- IntelliSense dla props komponentów
- Komponenty gotowe do użycia

### 4. **Customization**
- Łatwe dostosowywanie przez CSS variables
- Class Variance Authority dla wariantów
- Możliwość override'owania stylów

### 5. **Dark mode ready**
- Wbudowana obsługa dark mode
- CSS variables automatycznie przełączają kolory

## Następne kroki

### Komponenty do zmigrowania:
1. **TagList.tsx** - Zamienić na Card komponenty
2. **Navbar.tsx** - Dodać shadcn navigation componenty
3. **ConsentPopup.tsx** - Zamienić na shadcn Dialog
4. **TrackingDashboard.tsx** - Użyć Card i innych komponentów

### Dodatkowe komponenty shadcn/ui do rozważenia:
- **Dialog/Modal** - Dla popup'ów i modali
- **Table** - Dla tabel danych
- **Badge** - Dla tagów i statusów
- **Alert** - Dla komunikatów
- **Tabs** - Dla nawigacji zakładek
- **Form** - Dla formularzy z validacją

### Performance optimizations:
- Implementacja lazy loading komponentów
- Tree shaking unused Radix components
- Bundle size optimization

## Struktura plików po migracji

```
src/
├── components/
│   ├── ui/              # shadcn/ui komponenty
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── select.tsx
│   │   └── textarea.tsx
│   ├── TagForm.tsx      # ✅ Zmigrowane
│   ├── StatsDisplay.tsx # 🔄 Częściowo zmigrowane
│   └── ...             # Pozostałe do migracji
├── lib/
│   └── utils.ts         # Utility functions
└── ...
```

## Komendy build'u

```bash
# Development
npm run build:css  # Rebuild Tailwind CSS
npm start         # Start dev server

# Production
npm run build     # Production build
```

Aplikacja została pomyślnie zmigrowała na shadcn/ui z zachowaniem wszystkich funkcjonalności!
