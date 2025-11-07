#!/bin/bash
# Digital Ocean deployment script

echo "🚀 Starting deployment..."

# Create logs directory
mkdir -p logs

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Database migration (if needed)
echo "🗄️ Running database migrations..."
# python run_migration.py  # Uncomment if you have migrations

# Collect static files (if needed)
# python -m flask collect-static

echo "✅ Deployment complete!"
echo "🔧 To start the server, run:"
echo "   gunicorn -c gunicorn_config.py app:app"
