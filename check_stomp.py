import time
import sys
import stomp
import ssl
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StompListener(stomp.ConnectionListener):
    def __init__(self):
        self.queues = set()

    def on_error(self, frame):
        logger.error('Received an error "%s"' % frame.body)

    def on_message(self, frame):
        # ActiveMQ Advisory messages for Queues have 'destination' in headers
        # or the body contains info. For Advisory.Queue, the body is often empty
        # but the headers contain the info.
        dest = frame.headers.get('destination')
        if dest:
            logger.info(f"Discovered destination: {dest}")
            self.queues.add(dest)
        else:
             # Sometimes info is in the body for other advisory types
             logger.info(f"Received message: {frame.body}")

def check_stomp(host, port, user, password, use_ssl=False):
    logger.info(f"Connecting to {host}:{port} (SSL: {use_ssl})...")
    
    try:
        conn = stomp.Connection([(host, port)])
        if use_ssl:
            conn.set_ssl([(host, port)])
        
        listener = StompListener()
        conn.set_listener('', listener)
        
        conn.connect(user, password, wait=True)
        logger.info("Connected via STOMP!")
        
        # Subscribe to Advisory topics to find queues
        # ActiveMQ.Advisory.Queue is the topic for queues
        logger.info("Subscribing to ActiveMQ.Advisory.Queue...")
        conn.subscribe(destination='ActiveMQ.Advisory.Queue', id=1, ack='auto')
        
        logger.info("Waiting 5 seconds for advisory messages...")
        time.sleep(5)
        
        logger.info(f"Found {len(listener.queues)} queues/destinations.")
        for q in listener.queues:
            print(f" - {q}")
            
        conn.disconnect()
        
    except Exception as e:
        logger.error(f"STOMP Connection failed: {e}")

if __name__ == "__main__":
    # You can hardcode credentials here for testing or pass them as args
    if len(sys.argv) < 5:
        print("Usage: python check_stomp.py <host> <port> <user> <password> [ssl]")
        print("Example: python check_stomp.py localhost 61613 admin admin false")
        sys.exit(1)
        
    host = sys.argv[1]
    port = int(sys.argv[2])
    user = sys.argv[3]
    password = sys.argv[4]
    use_ssl = sys.argv[5].lower() == "true" if len(sys.argv) > 5 else False
    
    check_stomp(host, port, user, password, use_ssl)
