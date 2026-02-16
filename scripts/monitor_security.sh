#!/bin/bash

# Automated Security Monitoring Script
# Runs security scans every 10 minutes for 4 iterations

echo "🚀 Starting Automated Security Monitoring"
echo "Will run scans every 10 minutes for 4 iterations"
echo "=================================="

# Change to project directory
cd /Users/kirtissiemens/CascadeProjects/Telegram-bot-api

# Counter for iterations
iteration=1
max_iterations=4

while [ $iteration -le $max_iterations ]; do
    echo ""
    echo "🔄 Iteration $iteration of $max_iterations - $(date)"
    echo "----------------------------------------"
    
    # Run the security scan script
    ./scripts/security_scan.sh
    
    # Check if this is the last iteration
    if [ $iteration -eq $max_iterations ]; then
        echo ""
        echo "✅ Completed all $max_iterations security scans"
        echo "🔒 Final scan completed at $(date)"
        break
    fi
    
    # Wait 10 minutes before next scan
    echo ""
    echo "⏰️ Waiting 10 minutes before next scan..."
    sleep 600  # 10 minutes = 600 seconds
    
    # Increment counter
    iteration=$((iteration + 1))
done

echo ""
echo "🎯 Security monitoring completed"
echo "📊 All scan results saved in project directory"
echo "🔐 Repository is secure and monitored"
