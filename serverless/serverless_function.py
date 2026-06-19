# serverless_function.py - Serverless Κώδικας σε Python
import json

def lambda_handler(event, context):
    print("🚀 Η Knative Function ξύπνησε επειδή το MinIO την ειδοποίησε!")
    
    try:
        # Διαβάζει ποιο αρχείο ανέβηκε και σε ποιο φάκελο (bucket)
        bucket = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']
        
        print(f"📂 Βρέθηκε νέο αρχείο Alarm: {object_key}")
        
        # Φτιάχνει τα μεταδεδομένα (metadata) για να «μαρκάρει» το αρχείο
        metadata = {
            "status": "processed",
            "engine": "Knative-Python-v1",
            "annotated": True
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(metadata)
        }
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}