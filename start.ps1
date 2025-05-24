# Start backend
Write-Host "Starting backend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-Command `"cd c:\projekt-react\backend; python -m pip install -r requirements.txt; python app.py`""

# Wait a moment to ensure backend starts first
Start-Sleep -Seconds 2

# Start frontend
Write-Host "Starting frontend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-Command `"cd c:\projekt-react\frontend; npm start`""

Write-Host "Servers started! Frontend will be available at http://localhost:3000" -ForegroundColor Green
