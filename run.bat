@echo off
title AI Stock 360 Institutional Suite
echo ================================================================
echo   AI STOCK 360 INSTITUTIONAL SUITE
echo   Sistem Analisis, Prediksi Saham & Pelindung Modal
echo ================================================================
echo.
echo Menjalankan aplikasi web dashboard di browser Anda...
echo.

py -m streamlit run app.py
if %ERRORLEVEL% NEQ 0 (
    python -m streamlit run app.py
)
if %ERRORLEVEL% NEQ 0 (
    streamlit run app.py
)

pause
