# PowerShell script to remove JavaScript files that have TypeScript equivalents
# This script removes .js files that have .ts or .tsx counterparts

# App Files
Remove-Item -Path "c:\projekt-react\frontend\src\App.js" -Force
Remove-Item -Path "c:\projekt-react\frontend\src\App.test.js" -Force
Remove-Item -Path "c:\projekt-react\frontend\src\index.js" -Force
Remove-Item -Path "c:\projekt-react\frontend\src\reportWebVitals.js" -Force
Remove-Item -Path "c:\projekt-react\frontend\src\setupTests.js" -Force

# Components
Remove-Item -Path "c:\projekt-react\frontend\src\components\Layout.js" -Force
Remove-Item -Path "c:\projekt-react\frontend\src\components\Navbar.js" -Force
Remove-Item -Path "c:\projekt-react\frontend\src\components\StatsDisplay.js" -Force
Remove-Item -Path "c:\projekt-react\frontend\src\components\TagForm.js" -Force
Remove-Item -Path "c:\projekt-react\frontend\src\components\TagList.js" -Force
Remove-Item -Path "c:\projekt-react\frontend\src\components\TrackingDashboard.js" -Force
Remove-Item -Path "c:\projekt-react\frontend\src\components\VisitTracker.js" -Force

# Pages
Remove-Item -Path "c:\projekt-react\frontend\src\pages\AnalyticsPage.js" -Force
Remove-Item -Path "c:\projekt-react\frontend\src\pages\HomePage.js" -Force
Remove-Item -Path "c:\projekt-react\frontend\src\pages\StatsPage.js" -Force
Remove-Item -Path "c:\projekt-react\frontend\src\pages\TagsPage.js" -Force
Remove-Item -Path "c:\projekt-react\frontend\src\pages\TrackingPage.js" -Force
Remove-Item -Path "c:\projekt-react\frontend\src\pages\TrackingSetupPage.js" -Force

# API Services
Remove-Item -Path "c:\projekt-react\frontend\src\api\apiService.js" -Force
Remove-Item -Path "c:\projekt-react\frontend\src\api\trackingService.js" -Force

Write-Host "All JavaScript files with TypeScript equivalents have been removed."
