from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def process_minio_event():
    # Το MinIO στέλνει ένα event σε μορφή JSON όταν ανεβαίνει αρχείο
    event_data = request.get_json()
    
    print("🚀 Serverless Function Triggered by MinIO!")
    
    try:
        # Διάβασμα των πληροφοριών του αρχείου από το event
        records = event_data.get('Records', [])
        for record in records:
            bucket = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']
            print(f"📦 New Alarm File Detected -> Bucket: {bucket}, File: {object_key}")
            
        return jsonify({"status": "success", "message": "Alarm processed by Serverless Function"}), 200
    except Exception as e:
        print(f"❌ Error processing event: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)