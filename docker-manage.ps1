# Giziku Docker Management Script
# Usage: .\docker-manage.ps1 [build|up|down|logs|logs-api|logs-db|clean|restart]

param(
    [string]$Action = "up"
)

$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$appDir = Join-Path $rootDir "app"

function Build {
    Write-Host "🔨 Building Docker images..." -ForegroundColor Cyan
    Set-Location $appDir
    docker-compose build
    Set-Location $rootDir
}

function Up {
    Write-Host "🚀 Starting services..." -ForegroundColor Green
    Set-Location $appDir
    docker-compose up
    Set-Location $rootDir
}

function UpBackground {
    Write-Host "🚀 Starting services in background..." -ForegroundColor Green
    Set-Location $appDir
    docker-compose up -d
    Set-Location $rootDir
    Start-Sleep -Seconds 2
    docker-compose ps
}

function Down {
    Write-Host "🛑 Stopping services..." -ForegroundColor Yellow
    Set-Location $appDir
    docker-compose down
    Set-Location $rootDir
}

function Logs {
    Write-Host "📋 Showing all logs..." -ForegroundColor Cyan
    Set-Location $appDir
    docker-compose logs -f
    Set-Location $rootDir
}

function LogsApi {
    Write-Host "📋 Showing API logs..." -ForegroundColor Cyan
    Set-Location $appDir
    docker-compose logs -f api
    Set-Location $rootDir
}

function LogsDb {
    Write-Host "📋 Showing Database logs..." -ForegroundColor Cyan
    Set-Location $appDir
    docker-compose logs -f mysql
    Set-Location $rootDir
}

function Clean {
    Write-Host "🧹 Cleaning up containers and volumes..." -ForegroundColor Yellow
    Set-Location $appDir
    docker-compose down -v
    Set-Location $rootDir
    Write-Host "✅ Cleanup complete!" -ForegroundColor Green
}

function Restart {
    Write-Host "🔄 Restarting services..." -ForegroundColor Cyan
    Set-Location $appDir
    docker-compose restart
    Set-Location $rootDir
}

function Status {
    Write-Host "📊 Container status:" -ForegroundColor Cyan
    Set-Location $appDir
    docker-compose ps
    Set-Location $rootDir
}

function Shell {
    Write-Host "🐚 Opening API container shell..." -ForegroundColor Cyan
    Set-Location $appDir
    docker-compose exec api /bin/bash
    Set-Location $rootDir
}

function Help {
    Write-Host @"
Giziku Docker Management Script

Usage: .\docker-manage.ps1 [action]

Actions:
  build         - Build Docker images
  up            - Start services (foreground)
  up-bg         - Start services (background)
  down          - Stop services
  logs          - Show all logs (follow)
  logs-api      - Show API logs (follow)
  logs-db       - Show Database logs (follow)
  status        - Show container status
  clean         - Stop and remove all containers, networks, and volumes
  restart       - Restart all services
  shell         - Open API container shell
  help          - Show this help message

Examples:
  .\docker-manage.ps1 build       # Build images
  .\docker-manage.ps1 up-bg       # Start in background
  .\docker-manage.ps1 logs-api    # Watch API logs
  .\docker-manage.ps1 clean       # Clean everything

"@ -ForegroundColor Magenta
}

# Execute action
switch ($Action.ToLower()) {
    "build" { Build }
    "up" { Up }
    "up-bg" { UpBackground }
    "down" { Down }
    "logs" { Logs }
    "logs-api" { LogsApi }
    "logs-db" { LogsDb }
    "status" { Status }
    "clean" { Clean }
    "restart" { Restart }
    "shell" { Shell }
    "help" { Help }
    default { Help }
}
