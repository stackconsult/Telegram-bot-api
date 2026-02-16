#!/bin/bash

# Security Scan Script
# Runs security scans and reports results

echo "🔒 Starting Security Scan - $(date)"
echo "=================================="

# Change to project directory
cd /Users/kirtissiemens/CascadeProjects/Telegram-bot-api

# Run Safety scan
echo "📋 Running Safety CLI scan..."
python3 -m safety scan

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ Safety scan completed - No vulnerabilities found"
else
    echo "⚠️  Safety scan completed - Vulnerabilities detected"
fi

# Run Bandit security scan
echo "🛡️ Running Bandit security scan..."
python3 -m bandit -r telegram_api/ -f json -o bandit-report.json

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ Bandit scan completed - No security issues found"
else
    echo "⚠️  Bandit scan completed - Security issues detected"
fi

# Run basic tests to ensure functionality
echo "🧪 Running basic tests..."
python3 -m pytest tests/test_basic.py -v --tb=short

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ All tests passed"
else
    echo "❌ Some tests failed"
fi

echo "=================================="
echo "🔒 Security Scan Completed - $(date)"
echo ""
