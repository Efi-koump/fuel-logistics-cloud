# 1. Ξεκινάμε από το επίσημο image του Node-RED
FROM nodered/node-red:latest

# 2. Εγκαθιστούμε αυτόματα τα πρόσθετα που χρειάζεται η εργασία σου (RabbitMQ και MinIO)
RUN npm install @meowwolf/node-red-contrib-amqp
RUN npm install @reggae_ulli/node-red-contrib-minio-all-fix

# 3. Αντιγράφουμε το αρχείο με τις ροές σου (Retry + Circuit Breaker) μέσα στο image
COPY flows.json /data/flows.json