from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from datetime import datetime
import time, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BROKER = 'kafka-service:9092'
TOPIC = 'test-topic'

def main():
    # Initialize Kafka producer
    while True:
        logging.info("Connecting to Kafka..")
        try:
            producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER])
            logging.info("Connected to Kafka")
            break
        except NoBrokersAvailable as e:
            logging.error(f"No Broker error: {e}")
            time.sleep(1)
    message_count = 0

    try:
        while True:
            message = f"Message {message_count}".encode('utf-8')
            producer.send(TOPIC, value=message)
            logging.info(f"Sent message: {message}")
            message_count += 1
            time.sleep(1)  # wait for 1 second
    except KeyboardInterrupt:
        logging.warning("Shutting down producer...")
    finally:
        producer.close()

if __name__ == "__main__":
    main()
