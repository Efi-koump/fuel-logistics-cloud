import time
import requests
import concurrent.futures

# Η διεύθυνση του Node-RED ή του RabbitMQ σου 
URL = "http://localhost:15672" # Ή η θύρα του Node-RED που δέχεται τα HTTP posts
TOTAL_REQUESTS = 100  # Πόσα μηνύματα θα στείλουμε συνολικά
CONCURRENT = 10       # Πόσα μηνύματα θα φεύγουν ταυτόχρονα (φόρτος)

latencies = []

def send_alarm_request():
    payload = {
        "station_id": "Gas_Station_Athens_1",
        "alarm_type": "Critical_Fuel_Low",
        "timestamp": time.time()
    }
    
    start_time = time.time()
    try:
        # Προσομοίωση αποστολής μηνύματος
        response = requests.get(URL, timeout=5) # Αν έχεις HTTP endpoint άλλαξέ το σε requests.post
        end_time = time.time()
        
        latency = (end_time - start_time) * 1000 # Μετατροπή σε ms
        latencies.append(latency)
        print(self_heal_msg := f"Request success: {latency:.2f} ms")
    except Exception as e:
        print(f"Request failed: {e}")

print("🚀 Ξεκινάει το Load Testing της Cloud υποδομής...")
start_test = time.time()

# Τρέχουμε ταυτόχρονα τα requests για να ζορίσουμε το Kubernetes
with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT) as executor:
    executor.map(lambda f: send_alarm_request(), range(TOTAL_REQUESTS))

end_test = time.time()

# Υπολογισμός στατιστικών (SLAs)
latencies.sort()
avg_latency = sum(latencies) / len(latencies) if latencies else 0
p95_latency = latencies[int(len(latencies) * 0.95)] if latencies else 0
p99_latency = latencies[int(len(latencies) * 0.99)] if latencies else 0

print("\n📊 --- ΑΠΟΤΕΛΕΣΜΑΤΑ ΜΕΤΡΗΣΕΩΝ (SLAs) ---")
print(f" Συνολικός Χρόνος Δοκιμής: {end_test - start_test:.2f} δευτερόλεπτα")
print(f" Μέση Καθυστέρηση (Average Latency): {avg_latency:.2f} ms")
print(f" 95% των αιτημάτων απάντησαν κάτω από (95th Percentile): {p95_latency:.2f} ms")
print(f" 99% των αιτημάτων απάντησαν κάτω από (99th Percentile): {p99_latency:.2f} ms")

print("\n🏆 Ορισμός Κλάσεων Ποιότητας (Service Level Agreements):")
print(f"🥇 Gold Class  (Real-time Alarms): < {avg_latency * 0.8:.0f} ms")
print(f"🥈 Silver Class (Standard Processing): < {avg_latency * 1.2:.0f} ms")
print(f"🥉 Bronze Class (Batch/Log Analytics): > {avg_latency * 1.5:.0f} ms")