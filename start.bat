@echo off
echo Starting Frontend and Backend servers...

start cmd /k "cd c:\projekt-react\backend && python -m pip install -r requirements.txt && python app.py"
start cmd /k "cd c:\projekt-react\frontend && npm start"

echo Servers started! Frontend will be available at http://localhost:3000
