#!/usr/bin/env python3
import psycopg2
import os
import sys
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_database_connection():
    """Check PostgreSQL database connectivity."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        logger.info("Database connection: OK")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

def check_disk_space():
    """Check available disk space."""
    import shutil
    total, used, free = shutil.disk_usage("/")
    free_percent = (free / total) * 100
    
    if free_percent < 10:
        logger.warning(f"Low disk space: {free_percent:.1f}% free")
        return False
    
    logger.info(f"Disk space: {free_percent:.1f}% free")
    return True

def main():
    """Run all health checks."""
    logger.info(f"Health check started at {datetime.now()}")
    
    checks = [
        check_database_connection(),
        check_disk_space()
    ]
    
    if all(checks):
        logger.info("All health checks passed")
        sys.exit(0)
    else:
        logger.error("Some health checks failed")
        sys.exit(1)

if __name__ == "__main__":
    main()