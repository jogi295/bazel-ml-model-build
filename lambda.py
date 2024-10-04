import json
import base64
import gzip
import requests
from requests.auth import HTTPBasicAuth

OPENSEARCH_URL = 'https://search-mydomain-56th3wgprivvl4bk5cmmog7ovy.aos.us-east-1.on.aws/_dashboards'
# USERNAME = 'admin'
# PASSWORD = 'password'

def lambda_handler(event, context):
    try:
        # Extract and decompress log data from CloudWatch
        cw_data = event['awslogs']['data']
        compressed_payload = base64.b64decode(cw_data)
        uncompressed_payload = gzip.decompress(compressed_payload)
        log_events = json.loads(uncompressed_payload)

        # Print the raw log events (for debugging purposes)
        print("Received Log Events:")
        print(json.dumps(log_events, indent=2))
        
        # Example of Filtering Logic - Extract only ERROR logs

        # ----------- write your custum filter logic here ----------------- 
        filtered_logs = [log_event for log_event in log_events['logEvents'] if 'ERROR' in log_event['message']]
        
        if filtered_logs:
            print("Filtered Logs (ERROR):")
            for log in filtered_logs:
                print(f"Timestamp: {log['timestamp']}, Message: {log['message']}")
            
            # Send the filtered logs to OpenSearch
            send_to_opensearch(filtered_logs)
        
        return {
            'statusCode': 200,
            'body': json.dumps(f"Filtered {len(filtered_logs)} ERROR log(s).")
        }

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Internal Server Error: {str(e)}")
        }

def send_to_opensearch(filtered_logs):
    try:
        bulk_data = ''
        for log in filtered_logs:
            bulk_data += f'{{ "index": {{ }} }}\n'
            bulk_data += json.dumps({
                "message": log['message'],
                "timestamp": log['timestamp'],
                "logStream": log['logStream'],
                "logGroup": log['logGroup']
            }) + '\n'

        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            OPENSEARCH_URL,
            data=bulk_data,
            headers=headers,
            # auth=HTTPBasicAuth(USERNAME, PASSWORD)
        )
        
        # Raise an exception if OpenSearch returns an error
        if response.status_code != 200:
            response.raise_for_status()
        
        print(f"Response from OpenSearch: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error sending logs to OpenSearch: {str(e)}")
        raise
