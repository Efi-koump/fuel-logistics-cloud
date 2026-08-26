# frontend/app.py
from flask import Flask, render_template_string
from minio import Minio
import json
import os

app = Flask(__name__)

# 1. Ρύθμιση παραμέτρων σύνδεσης με το MinIO του Kubernetes
# Αν δεν βρει variables περιβάλλοντος, χρησιμοποιεί default τιμές
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio-service:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")

# 2. Αρχικοποίηση του MinIO Client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# 3. Οπτικό κομμάτι (HTML/CSS) με Bootstrap για καθαρή εμφάνιση
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <title>Fuel Logistics - Safety Monitor UI</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="h2 text-dark">⛽ Fuel Logistics & Safety Monitor</h1>
            <span class="badge bg-primary fs-6">Kubernetes Live Mode</span>
        </div>
        
        <div class="card shadow-sm mb-4">
            <div class="card-header bg-dark text-white">🟢 Καταγραφή Ιστορικών Συναγερμών (MinIO Alarms JSON)</div>
            <div class="card-body">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Πελάτης (Bucket)</th>
                            <th>Αρχείο Συμβάντος</th>
                            <th>Τύπος Συναγερμού</th>
                            <th>Συσκευή</th>
                            <th>Κατάσταση</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for alarm in alarms %}
                        <tr>
                            <td><span class="badge bg-secondary">{{ alarm.bucket }}</span></td>
                            <td><code>{{ alarm.object_name }}</code></td>
                            <td><span class="text-danger fw-bold">{{ alarm.data.alarm_type }}</span></td>
                            <td>{{ alarm.data.device }}</td>
                            <td><span class="badge bg-success">Archived</span></td>
                        </tr>
                        {% else %}
                        <tr>
                            <td colspan="5" class="text-center text-muted">Δεν βρέθηκαν καταγεγραμμένα alarms στα buckets.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
"""

# 4. Το Route (το endpoint) που φορτώνει όταν μπαίνουμε στον browser
@app.route('/')
def index():
    all_alarms = []
    try:
        # Ορίζουμε τα buckets των 3 Gas Stations που θέλουμε να διαβάσουμε
        buckets = ["customer01-bucket", "customer02-bucket", "customer03-bucket"]
        
        for bucket in buckets:
            # Έλεγχος αν το bucket υπάρχει στο MinIO
            if minio_client.bucket_exists(bucket):
                # Λίστα με όλα τα αρχεία (objects) μέσα στο bucket
                objects = minio_client.list_objects(bucket, recursive=True)
                for obj in objects:
                    # Λήψη του περιεχομένου του JSON αρχείου
                    response = minio_client.get_object(bucket, obj.object_name)
                    data = json.loads(response.data.decode('utf-8'))
                    
                    # Προσθήκη στη συνολική λίστα για εμφάνιση στο UI
                    all_alarms.append({
                        "bucket": bucket,
                        "object_name": obj.object_name,
                        "data": data
                    })
    except Exception as e:
        print(f"Σφάλμα κατά την ανάκτηση από το MinIO: {e}")
        
    return render_template_string(HTML_TEMPLATE, alarms=all_alarms)

if __name__ == '__main__':
    # Η εφαρμογή «ακούει» στην πόρτα 5000 για όλα τα εισερχόμενα IDs
    app.run(host='0.0.0.0', port=5000)