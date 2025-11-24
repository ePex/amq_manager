import logging
import os
from amq_manager.ui.app import ActiveMQManagerApp

# Configure logging
LOG_FILE = "amq_manager.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting ActiveMQ Manager")
    app = ActiveMQManagerApp()
    app.run()
    logger.info("ActiveMQ Manager stopped")

if __name__ == "__main__":
    main()
