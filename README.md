# Fuel Logistics Cloud Platform

## Περιγραφή 

Πλατφόρμα παρακολούθησης και διαχείρισης στόλου οχημάτων διανομής
καυσίμων, δεξαμενών και αποθηκών καυσίμων, ελαιολιπαντικών και ξυλείας.

Οι συσκευές (π.χ. βυτιοφόρα) καταχορούνται στο ThingsBoard και παράγουν
τηλεμετρία και συναγερμούς (alarms). Οι συναγερμοί προωθούνται μέσω RabbitMQ, επεξεργάζονται στο Node-Red και αποθηκεύονται σε Minio Object Storage για ιστορική ανάλυση και αρχειοθέτηση.

## Αρχιτεκτονική Συστήματος

Το σύστημα βασίζεται σε αρχιτεκτονική microservices και υλοποιείται εξ' ολοκλήρουσε Docker containers.

Το ThingsBoard λειτουργεί ως κεντρική πλατφόρμα ΙοΤ, ενώ το RabbitMQ χρησιμοποιείται για την ασύγχρονη μεταφορά συναγερμών. Το Node-Red αναλαμβάνει την επεξεργασία των μηνυμάτων και το MinIO χρησιμοποιείται ως Object Storage γαι ιστορική ανάλυση και αρχειοθέτηση.

Η επικοινωνία μεταξύ των επιμέρους υπηρεσιών πραγματοποιείται μέσω Docker internal

## Τεχνολογίες 

- ThingsBoard (IoT Platform)
- RabbitMQ (Message Broker)
- Node-Red (Flow-based Processing)
- MinIO (Object Storage)
- Docker & Docker Compose

## Εκκίνηση Συστήματος

Απαιτείται εγκατεστημένο Docker και Docker Compose.

### Windows / Linux / macOS

```bash
docker compose up -d

```md
Η εργασία έχει δοκιμαστεί σε Windows 11 με Docker Desktop.

## Πρόσβαση σε Υπηρεσίες

- ThingsBoard: http://localhost:8080
- Node-Red: http://localhost:1880
- RabbitMQ Management: http://localhost:15672
- MinIO: http://localhost:9001

## Δοκιμή Σεναρίου

1. Δημιουργία συσκευών στο ThingsBoard
2. Παραγωγή συναγερμού (π.χ. LOW FUEL)
3. Ο συναγερμός αποστέλλεται στο RabbitMQ
4. Το Node-Red επεξεργάζεται το μήνυμα
5. Το αρχείο αποθηκεύεται στο ΜinIO στο αντίστοιχο bucket του πελάτη
   που ανήκει η συσκευή

## Λογαριασμοί Δοκιμής

### ThingsBoard
- Username: ais25108@hua.gr
- Password: ais25108

### RabbitMQ
- Username: ais25108
- Password: ais25108

### MinIO
- Username: minioadmin
- Password: minioadmin