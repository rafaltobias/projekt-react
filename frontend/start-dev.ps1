# Start development with combined Tailwind CSS watcher and React server
Write-Host "Starting development environment (Tailwind CSS + React)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-Command `"cd c:\projekt-react\frontend; npm run dev`""

Write-Host "Development environment started!" -ForegroundColor Green
Write-Host "- Tailwind CSS is watching for changes" -ForegroundColor Green
Write-Host "- React frontend is available at http://localhost:3000" -ForegroundColor Green
