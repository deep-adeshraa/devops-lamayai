1. What this code does ?
- There are two main components in this application:
    1. **Producer**: Responsible for generating a sequence of messages (e.g., `Message 1, 2, etc.`) and sending them to a Kafka topic named `test-topic`.
    2. **Consumer**: Responsible for consuming messages from the `test-topic`. After consuming the message from the Kafka topic, the consumer performs two actions:
         - Inserts the record with datetime in an Elasticsearch index named `test-index`.
         - Inserts the message in a Neo4j graph database as a node.