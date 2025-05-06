#!/bin/bash

# Set variables
BACKUP_DIR="/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/eduwize_backup_${TIMESTAMP}.sql"
BACKUP_FILE_COMPRESSED="${BACKUP_FILE}.gz"

# Create backup directory if it doesn't exist
mkdir -p ${BACKUP_DIR}

# Backup database
echo "Creating database backup: ${BACKUP_FILE}"
pg_dump -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -d ${POSTGRES_DB} > ${BACKUP_FILE}

# Compress backup
echo "Compressing backup to: ${BACKUP_FILE_COMPRESSED}"
gzip ${BACKUP_FILE}

# Remove backups older than 7 days
echo "Removing backups older than 7 days"
find ${BACKUP_DIR} -name "eduwize_backup_*.sql.gz" -type f -mtime +7 -delete

echo "Backup completed successfully"

# List all backups
echo "Available backups:"
ls -lh ${BACKUP_DIR}
