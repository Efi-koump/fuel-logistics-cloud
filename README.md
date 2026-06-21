# Fuel Logistics Cloud Native Platform

## Περιγραφή 

Αρχιτεκτονικός μετασχηματισμός της πλατφόρμας παρακολούθησης και διαχείρισης στόλου οχημάτων διανομής καυσίμων, δεξαμενών και αποθηκών από περιβάλλον Docker Compose σε κατανεμημένη υποδομή Kubernetes.

Οι 15 συσκευές (κατανεμημένες σε 3 Gas Stations) παράγουν τηλεμετρία και συναγερμούς (alarms). Οι συναγερμοί προωθούνται μέσω RabbitMQ, επεξεργάζονται στο Node-RED και αποθηκεύονται σε MinIO Object Storage, με multi-tenancy απομόνωση σε buckets ανά πελάτη.

## Αρχιτεκτονική Συστήματος

Το σύστημα βασίζεται σε αρχιτεκτονική microservices και υλοποιείται σε περιβάλλον Kubernetes (MicroK8s) με Stateless Deployments. 

Η διαχείριση του κύκλου ζωής γίνεται με GitOps Pipeline, χρησιμοποιώντας το Jenkins για το Continuous Integration (CI) και το ArgoCD για το Continuous Deployment (CD) με βάση τα manifests του αποθετηρίου[cite: 18].

## Τεχνολογίες 

- ThingsBoard (IoT Platform)
- RabbitMQ (Message Broker)
- Node-RED (Flow-based Processing)
- MinIO (Object Storage)
- Kubernetes & MicroK8s (Orchestration)
- Jenkins & ArgoCD (GitOps CI/CD)
- OpenTofu & Ansible (Declarative Automation Files)

## Σημείωση Υλοποίησης (Fallback Strategies)
Λόγω τεχνικών περιορισμών και hardware constraints στο περιβάλλον ανάπτυξης, η ζωντανή εκτέλεση του Knative runtime καθώς και των OpenTofu/Ansible playbooks δεν κατέστη δυνατή. Ως εναλλακτική λύση, τα αρχεία υποδομής (`main.tf`, `playbook.yml`) και ο Serverless κώδικας Python έχουν ενταχθεί declarative στο Monorepo (Deployment-Ready), ενώ η event-driven επεξεργασία των metadata προσομοιώνεται μέσω asynchronous ροών στο Node-RED.

## Εκκίνηση Συστήματος

Απαιτείται εγκατεστημένο περιβάλλον Kubernetes (MicroK8s) και ενεργοποιημένα τα απαραίτητα addons.

### Εφαρμογή Manifests

```bash
kubectl apply -f kubernetes/
```
Η εφαρμογή και ο συγχρονισμός των microservices μπορεί επίσης να γίνει αυτόματα μέσω του ArgoCD UI, συνδέοντας το παρόν Git αποθετήριο.

## Πρόσβαση σε Υπηρεσίες

Οι υπηρεσίες εκτίθενται μέσω NodePort Services του Kubernetes Cluster στις ακόλουθες διευθύνσεις:

- ThingsBoard: http://<Cluster-Node-IP>:30080
- Node-RED: http://<Cluster-Node-IP>:31880
- RabbitMQ Management: http://<Cluster-Node-IP>:31572
- MinIO Console: http://<Cluster-Node-IP>:30901

*Σημείωση:* Ο κωδικός πρόσβασης για το Stateless Jenkins Pod ανακτάται μέσω των logs με την εντολή: `kubectl logs deployment/jenkins -n jenkins`.

## Δοκιμή Σεναρίου & SLAs

Η σωστή λειτουργία και η ποιότητα υπηρεσίας επαληθεύτηκαν μέσω load test (`load_test.py`), ορίζοντας τα εξής επίπεδα SLA βάσει των CDF Percentiles:
1. **Gold Class (≤ 13 ms):** Κρίσιμα Alarms βυτιοφόρων και δεξαμενών.
2. **Silver Class (14 ms - 20 ms):** Τυπική τηλεμετρία και επιτήρηση αποθηκών.
3. **Bronze Class (> 20 ms):** Batch διεργασίες και metadata annotation.

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

### ArgoCD
- Username: admin
- Password: *Ανάκτηση μέσω του Kubernetes secret (argocd-initial-admin-secret)*

### Jenkins
- Username: admin
- Password: *Ανάκτηση μέσω των Kubernetes logs (initialAdminPassword)*