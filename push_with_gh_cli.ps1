# Push RAG Project to GitHub using GitHub CLI
# This script uploads files while preserving folder structure

$ghPath = 'C:\Github CLI 2.65\gh_2.65.0_windows_amd64\bin\gh.exe'
$repo = 'Ritish017/langchain-langgraph-rag'
$branch = 'main'
$projectPath = 'C:\python\GenAI\LangGraph\rag-poc'

Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     Pushing to GitHub: langchain-langgraph-rag            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Change to project directory
Set-Location $projectPath

# Helper: recursively get all files in the repo from GitHub API
function Get-RemoteFiles($path = "") {
    $apiPath = if ($path) { "repos/$repo/contents/$path?ref=$branch" } else { "repos/$repo/contents?ref=$branch" }
    try {
        $result = & $ghPath api $apiPath 2>$null | ConvertFrom-Json
        $files = @()
        foreach ($item in $result) {
            if ($item.type -eq "file") {
                $files += $item.path
            } elseif ($item.type -eq "dir") {
                $files += Get-RemoteFiles $item.path
            }
        }
        return $files
    } catch {
        return @()
    }
}

# Step 1: Check authentication
Write-Host "[1/4] Checking GitHub authentication..." -ForegroundColor Yellow
try {
    $authStatus = & $ghPath auth status 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ❌ Not authenticated. Please run:" -ForegroundColor Red
        Write-Host "   $ghPath auth login" -ForegroundColor Cyan
        exit 1
    }
    Write-Host "   ✓ Authenticated" -ForegroundColor Green
} catch {
    Write-Host "   ❌ GitHub CLI not working. Error: $_" -ForegroundColor Red
    exit 1
}

# Step 2: Delete old files from remote repo (optional - keeps README.md and .gitignore)
Write-Host "`n[2/4] Cleaning remote repository..." -ForegroundColor Yellow
$remoteFiles = Get-RemoteFiles
$deletedCount = 0

if ($remoteFiles.Count -gt 0) {
    foreach ($remoteFile in $remoteFiles) {
        # Keep README.md, LICENSE, .gitignore
        if ($remoteFile -notmatch "^(README\.md|LICENSE|\.gitignore)$") {
            try {
                Write-Host "   Deleting $remoteFile..." -ForegroundColor Gray
                # Get the file's SHA
                $fileInfo = & $ghPath api "repos/$repo/contents/$remoteFile?ref=$branch" 2>$null | ConvertFrom-Json
                if ($fileInfo.sha) {
                    $sha = $fileInfo.sha
                    & $ghPath api "repos/$repo/contents/$remoteFile" -X DELETE `
                        -F message="Delete $remoteFile for fresh upload" `
                        -F sha=$sha `
                        -F branch=$branch 2>$null | Out-Null
                    $deletedCount++
                }
            } catch {
                Write-Host "   ⚠ Could not delete $remoteFile (may not exist)" -ForegroundColor DarkGray
            }
        }
    }
    Write-Host "   ✓ Cleaned $deletedCount files" -ForegroundColor Green
} else {
    Write-Host "   ✓ Repository is empty or already clean" -ForegroundColor Green
}

# Step 3: Get local files to upload
Write-Host "`n[3/4] Preparing local files..." -ForegroundColor Yellow

# Files and folders to exclude
$excludePatterns = @(
    '\.git',
    '__pycache__',
    '\.venv',
    'venv',
    'chroma_db',
    '\.env$',
    '\.pkl$',
    '\.corrupt$',
    '\.bak$',
    '\.backup$',
    'app_fixed\.py',
    '\.vscode',
    '\.idea',
    'node_modules'
)

$files = Get-ChildItem -Recurse -File | Where-Object {
    $filePath = $_.FullName
    $shouldExclude = $false
    foreach ($pattern in $excludePatterns) {
        if ($filePath -match $pattern) {
            $shouldExclude = $true
            break
        }
    }
    -not $shouldExclude
}

Write-Host "   ✓ Found $($files.Count) files to upload" -ForegroundColor Green

# Step 4: Upload local files
Write-Host "`n[4/4] Uploading files to GitHub..." -ForegroundColor Yellow
$uploadedCount = 0
$failedCount = 0
$totalFiles = $files.Count
$currentFile = 0

foreach ($file in $files) {
    $currentFile++
    $relativePath = $file.FullName.Substring($projectPath.Length + 1) -replace "\\", "/"
    
    # Show progress
    $percent = [math]::Round(($currentFile / $totalFiles) * 100)
    Write-Host "   [$percent%] Uploading: $relativePath" -ForegroundColor Cyan
    
    try {
        # Read file and convert to base64
        $content = [Convert]::ToBase64String([IO.File]::ReadAllBytes($file.FullName))
        
        # Check if file exists on remote
        $fileExists = $false
        try {
            $existingFile = & $ghPath api "repos/$repo/contents/$relativePath?ref=$branch" 2>$null | ConvertFrom-Json
            $fileExists = $true
            $sha = $existingFile.sha
        } catch {
            $fileExists = $false
        }
        
        # Upload or update file
        if ($fileExists) {
            & $ghPath api "repos/$repo/contents/$relativePath" -X PUT `
                -F message="Update $relativePath" `
                -F content=$content `
                -F sha=$sha `
                -F branch=$branch 2>&1 | Out-Null
        } else {
            & $ghPath api "repos/$repo/contents/$relativePath" -X PUT `
                -F message="Add $relativePath" `
                -F content=$content `
                -F branch=$branch 2>&1 | Out-Null
        }
        
        if ($LASTEXITCODE -eq 0) {
            $uploadedCount++
        } else {
            Write-Host "      ⚠ Failed to upload $relativePath" -ForegroundColor Red
            $failedCount++
        }
        
        # Small delay to avoid rate limiting
        Start-Sleep -Milliseconds 100
        
    } catch {
        Write-Host "      ❌ Error uploading $relativePath : $_" -ForegroundColor Red
        $failedCount++
    }
}

# Summary
Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    Upload Complete!                       ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "📊 Summary:" -ForegroundColor Yellow
Write-Host "   ✓ Files uploaded: $uploadedCount" -ForegroundColor Green
if ($failedCount -gt 0) {
    Write-Host "   ⚠ Files failed: $failedCount" -ForegroundColor Red
}
Write-Host "   🗑️ Files deleted: $deletedCount" -ForegroundColor Gray

Write-Host "`n🔗 Repository URL:" -ForegroundColor Yellow
Write-Host "   https://github.com/$repo" -ForegroundColor Cyan

Write-Host "`n✨ Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Visit your repository to verify files" -ForegroundColor White
Write-Host "   2. Add repository description and topics" -ForegroundColor White
Write-Host "   3. Add MIT License (if not already added)" -ForegroundColor White
Write-Host "   4. Share on LinkedIn! 🚀" -ForegroundColor White

Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
