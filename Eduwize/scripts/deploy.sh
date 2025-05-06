#!/bin/bash

# Exit on error
set -e

# Variables
DEPLOY_DIR="/home/eduwize/app"
BACKUP_DIR="/home/eduwize/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/pre_deploy_backup_${TIMESTAMP}.sql.gz"
LOG_FILE="${DEPLOY_DIR}/logs/deploy_${TIMESTAMP}.log"

# Create log directory if it doesn't exist
mkdir -p "${DEPLOY_DIR}/logs"

# Start logging
exec > >(tee -a "${LOG_FILE}") 2>&1
echo "Starting deployment at $(date)"

# Check if we're in the right directory
if [ ! -f "${DEPLOY_DIR}/manage.py" ]; then
    echo "Error: manage.py not found. Make sure you're in the Django project directory."
    exit 1
fi

# Create backup directory if it doesn't exist
mkdir -p "${BACKUP_DIR}"

# Load environment variables
if [ -f "${DEPLOY_DIR}/.env" ]; then
    echo "Loading environment variables from .env file"
    source "${DEPLOY_DIR}/.env"
else
    echo "Error: .env file not found"
    exit 1
fi

# Backup database before deployment
echo "Creating database backup: ${BACKUP_FILE}"
pg_dump -h "${DB_HOST}" -U "${DB_USER}" -d "${DB_NAME}" | gzip > "${BACKUP_FILE}"
echo "Database backup created successfully"

# Pull latest code
echo "Pulling latest code from repository"
git pull origin main

# Install or update dependencies
echo "Installing/updating dependencies"
pip install -r requirements-prod.txt

# Run migrations
echo "Running database migrations"
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files"
python manage.py collectstatic --noinput

# Restart services
echo "Restarting services"
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# Check if services are running
echo "Checking services status"
systemctl status gunicorn | grep "Active:"
systemctl status nginx | grep "Active:"

# Test the application
echo "Testing application health"
curl -s http://localhost/health/ | grep "healthy"

echo "Deployment completed successfully at $(date)"
