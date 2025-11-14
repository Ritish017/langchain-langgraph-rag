# Quick Push Script for GitHub
# Run this after Git is installed

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Push to GitHub - langchain-langgraph-rag" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Set-Location "c:\python\GenAI\LangGraph\rag-poc"

try {
    Write-Host "[1/6] Initializing Git repository..." -ForegroundColor Yellow
    git init
    
    Write-Host "[2/6] Adding all files..." -ForegroundColor Yellow
    git add .
    
    Write-Host "[3/6] Creating commit..." -ForegroundColor Yellow
    git commit -m "Initial commit: Production-ready RAG system with LangGraph"
    
    Write-Host "[4/6] Setting branch to main..." -ForegroundColor Yellow
    git branch -M main
    
    Write-Host "[5/6] Adding remote repository..." -ForegroundColor Yellow
    git remote add origin https://github.com/Ritish017/langchain-langgraph-rag.git 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   Remote already exists, skipping..." -ForegroundColor Gray
    }
    
    Write-Host "[6/6] Pushing to GitHub..." -ForegroundColor Yellow
    git push -u origin main
    
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "  ✓ Push Complete!" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Green
    
    Write-Host "Visit: https://github.com/Ritish017/langchain-langgraph-rag`n" -ForegroundColor Cyan
    
} catch {
    Write-Host "`n❌ Error: $_" -ForegroundColor Red
    Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Make sure Git is installed: winget install Git.Git" -ForegroundColor Gray
    Write-Host "2. Restart PowerShell after installing Git" -ForegroundColor Gray
    Write-Host "3. Check PUSH_TO_GITHUB.md for detailed instructions`n" -ForegroundColor Gray
}

Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
