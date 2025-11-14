@echo off
REM Quick Push Script for GitHub
REM Run this after Git is installed

echo ========================================
echo   Push to GitHub - langchain-langgraph-rag
echo ========================================
echo.

cd /d "c:\python\GenAI\LangGraph\rag-poc"

echo [1/6] Initializing Git repository...
git init

echo [2/6] Adding all files...
git add .

echo [3/6] Creating commit...
git commit -m "Initial commit: Production-ready RAG system with LangGraph"

echo [4/6] Setting branch to main...
git branch -M main

echo [5/6] Adding remote repository...
git remote add origin https://github.com/Ritish017/langchain-langgraph-rag.git

echo [6/6] Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo   Push Complete!
echo ========================================
echo.
echo Visit: https://github.com/Ritish017/langchain-langgraph-rag
echo.
pause
