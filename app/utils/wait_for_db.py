import time
import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_db():
    """Wait for database to be available."""
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        logger.error("DATABASE_URL environment variable not set!")
        return False
    
    logger.info(f"Waiting for database connection...")
    engine = create_engine(db_url)
    
    for i in range(60):  # try for 60 seconds
        try:
            connection = engine.connect()
            connection.close()
            logger.info("Database is available!")
            return True
        except OperationalError:
            logger.info(f"Database unavailable, waiting {i+1}/60 seconds...")
            time.sleep(1)
    
    logger.error("Could not connect to database after 60 seconds!")
    return False

if __name__ == "__main__":
    wait_for_db() 