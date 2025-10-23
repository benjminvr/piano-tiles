# 🎵 Instalación Sistema de Audio Musical para Piano Tiles

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🎵 Piano Tiles - Sistema de Audio Musical" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Actualizar pip
Write-Host "📦 Paso 1/4: Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ pip actualizado`n" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Error actualizando pip (continuando...)`n" -ForegroundColor Yellow
}

# Instalar pygame
Write-Host "📦 Paso 2/4: Instalando pygame..." -ForegroundColor Yellow
pip install pygame
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ pygame instalado`n" -ForegroundColor Green
} else {
    Write-Host "   ❌ Error instalando pygame`n" -ForegroundColor Red
    exit 1
}

# Instalar numpy
Write-Host "📦 Paso 3/4: Instalando numpy..." -ForegroundColor Yellow
pip install numpy
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ numpy instalado`n" -ForegroundColor Green
} else {
    Write-Host "   ❌ Error instalando numpy`n" -ForegroundColor Red
    exit 1
}

# Verificar instalación
Write-Host "🔍 Paso 4/4: Verificando instalación..." -ForegroundColor Yellow
$verification = python -c "import pygame; import numpy; print('OK')" 2>&1
if ($verification -match "OK") {
    Write-Host "   ✅ Todas las dependencias instaladas correctamente`n" -ForegroundColor Green
} else {
    Write-Host "   ❌ Error en la verificación`n" -ForegroundColor Red
    exit 1
}

# Mostrar canciones disponibles
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎼 Canciones Disponibles" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

python audio_config.py

# Instrucciones finales
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ ¡Instalación Completa!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "📖 Próximos pasos:`n" -ForegroundColor Yellow

Write-Host "   1. 🎮 Jugar con audio musical:" -ForegroundColor White
Write-Host "      python app.py`n" -ForegroundColor Gray

Write-Host "   2. 🎹 Demo interactivo (prueba las canciones):" -ForegroundColor White
Write-Host "      python audio_demo.py`n" -ForegroundColor Gray

Write-Host "   3. 🎵 Cambiar canción:" -ForegroundColor White
Write-Host "      Edita audio_config.py" -ForegroundColor Gray
Write-Host "      Cambia ACTIVE_SONG = 'c_major' a otra opción`n" -ForegroundColor Gray

Write-Host "   4. 📚 Documentación completa:" -ForegroundColor White
Write-Host "      - AUDIO_README.md (documentación detallada)" -ForegroundColor Gray
Write-Host "      - QUICK_START_AUDIO.md (guía rápida)`n" -ForegroundColor Gray

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎹 ¡Disfruta creando música!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan
