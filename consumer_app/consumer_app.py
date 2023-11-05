import logging, time
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from neo4j import GraphDatabase
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BROKER = 'kafka:9092'
ELASTICSEARCH_HOST = 'elasticsearch'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_USERNAME = os.environ.get('ELASTICSEARCH_USERNAME')
ELASTICSEARCH_PASS = os.environ.get('ELASTICSEARCH_PASS')

NEO4J_HOST = 'bolt://neo4j:7687'
NEO4J_USER = os.environ.get('NEO4J_USER')
NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD')
TOPIC = 'test-topic'


class Neo4jClient:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def insert_message(self, message):
        with self._driver.session() as session:
            session.write_transaction(self._create_message, message)

    @staticmethod
    def _create_message(tx, message):
        tx.run("CREATE (message:Message {content: $content})", content=message)


def main():
    while True:
        try:
            logging.info("Connecting to Kafka, ES, neo4j...")
            try:
                # Initialize Kafka consumer
                consumer = KafkaConsumer(TOPIC, bootstrap_servers=[KAFKA_BROKER])
                logging.info("Connected to Kafka")
            except Exception as e:
                logging.error(f"Error connecting to Kafka: {e}")
                time.sleep(1)
                continue

            try:
                # Initialize Elasticsearch client
                es = Elasticsearch(
                                    [
                                        {
                                            'host':str(ELASTICSEARCH_HOST),
                                            'port':str(ELASTICSEARCH_PORT),
                                            'scheme': "http"
                                        }
                                    ],
                                    http_auth=(str(ELASTICSEARCH_USERNAME), str(ELASTICSEARCH_PASS))
                                )
                logging.info("Connected to Elasticsearch")
            except Exception as e:
                logging.error(f"Error connecting to Elasticsearch: {e}")
                time.sleep(1)
                continue

            try:
                # Initialize Neo4j client
                neo4j_client = Neo4jClient(NEO4J_HOST, NEO4J_USER, NEO4J_PASSWORD)
                logging.info("Connected to Neo4j")
            except Exception as e:
                logging.error(f"Error connecting to Neo4j: {e}")
                time.sleep(1)
                continue

            break
        except Exception as e:
            logging.error(f"Connection Error: {e}")
            time.sleep(1)

    for msg in consumer:
        message = msg.value.decode('utf-8')
        logging.info(f"Received message: {message}")

        try:
            # Insert into Elasticsearch
            es.index(index='messages-test', body={'content': message+ "-" + str(datetime.now())})
            logging.info("Inserted into Elasticsearch")
        except Exception as e:
            logging.error(f"Error inserting into Elasticsearch: {e}")


        try:
            # Insert into Neo4j
            neo4j_client.insert_message(message)
            logging.info("Inserted into Neo4j")
        except Exception as e:
            logging.error(f"Error inserting into Neo4j: {e}")

    neo4j_client.close()


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as error:
            logger.error(f"Main function: {error}")
            time.sleep(20) # Wait for service to be up
            continue
