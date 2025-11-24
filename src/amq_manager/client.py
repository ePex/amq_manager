import requests
from requests.auth import HTTPBasicAuth
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ActiveMQClient:
    def __init__(self, host: str, port: int, user: str, password: str, ssl: bool = False, context_path: str = "/api/jolokia", timeout: int = 5):
        scheme = "https" if ssl else "http"
        # Ensure context_path starts with /
        if not context_path.startswith("/"):
            context_path = "/" + context_path
        self.base_url = f"{scheme}://{host}:{port}{context_path}"
        self.auth = HTTPBasicAuth(user, password)
        self.headers = {"Origin": f"{scheme}://{host}"}
        self.timeout = timeout

    def list_queues(self) -> List[Dict[str, Any]]:
        """
        List all queues and their stats.
        """
        payload = {
            "type": "read",
            "mbean": "org.apache.activemq:type=Broker,brokerName=localhost,destinationType=Queue,destinationName=*"
        }
        # Let exceptions propagate to the UI
        response = requests.post(self.base_url, json=payload, auth=self.auth, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        
        try:
            data = response.json()
        except ValueError as e:
            logger.error(f"Failed to decode JSON. Response content: {response.text[:1000]}") # Log first 1000 chars
            raise Exception(f"Invalid JSON response from server. Check logs for details. Error: {e}")
        
        if data.get("status") != 200:
            logger.error(f"Jolokia error listing queues: {data.get('status')}")
            raise Exception(f"Jolokia error: {data.get('status')}")
        
        queues = []
        value = data.get("value", {})
        for key, stats in value.items():
            # Extract queue name from the key or stats
            # Key format: org.apache.activemq:brokerName=localhost,destinationName=...,destinationType=Queue,type=Broker
            queue_name = stats.get("Name")
            queues.append(stats)
        
        return queues

    def browse_messages(self, queue_name: str) -> List[Dict[str, Any]]:
        """
        Browse messages in a specific queue.
        """
        # Jolokia exec operation to browse messages
        # Operation: browse() on the Queue MBean
        mbean = f"org.apache.activemq:type=Broker,brokerName=localhost,destinationType=Queue,destinationName={queue_name}"
        payload = {
            "type": "exec",
            "mbean": mbean,
            "operation": "browse()"
        }
        try:
            response = requests.post(self.base_url, json=payload, auth=self.auth, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != 200:
                print(f"Jolokia error browsing queue {queue_name}: {data.get('status')}")
                return []
            
            # The value is a list of CompositeData, which are dicts
            return data.get("value", [])
        except Exception as e:
            print(f"Error browsing queue {queue_name}: {e}")
            return []

    def move_message(self, message_id: str, source_queue: str, target_queue: str) -> bool:
        """
        Move a message from one queue to another.
        """
        # Operation: moveMessageTo(String messageId, String destinationName) on the Queue MBean
        mbean = f"org.apache.activemq:type=Broker,brokerName=localhost,destinationType=Queue,destinationName={source_queue}"
        payload = {
            "type": "exec",
            "mbean": mbean,
            "operation": "moveMessageTo(java.lang.String,java.lang.String)",
            "arguments": [message_id, target_queue]
        }
        try:
            response = requests.post(self.base_url, json=payload, auth=self.auth, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("status") == 200 and data.get("value") is True
        except Exception as e:
            print(f"Error moving message {message_id}: {e}")
            return False

    def delete_message(self, message_id: str, queue_name: str) -> bool:
        """
        Delete (remove) a message from a queue.
        """
        # Operation: removeMessage(String messageId) on the Queue MBean
        mbean = f"org.apache.activemq:type=Broker,brokerName=localhost,destinationType=Queue,destinationName={queue_name}"
        payload = {
            "type": "exec",
            "mbean": mbean,
            "operation": "removeMessage(java.lang.String)",
            "arguments": [message_id]
        }
        try:
            response = requests.post(self.base_url, json=payload, auth=self.auth, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("status") == 200 and data.get("value") is True
        except Exception as e:
            print(f"Error deleting message {message_id}: {e}")
            return False
