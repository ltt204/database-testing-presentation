import json
import html

with open('req7/postman_collection.json', 'r') as f:
    data = json.load(f)

html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #ff7f00; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .success { color: green; }
        .fail { color: red; }
        .method { font-weight: bold; }
        .POST { color: orange; }
        .GET { color: blue; }
        .PUT { color: blue; }
        .DELETE { color: red; }
    </style>
</head>
<body>
    <h1>OrangeHRM API Test Plan Report</h1>
    <p>Generated from Postman Collection</p>
"""

for folder in data['item']:
    if 'item' in folder: # It's a folder (Recruitment, Performance)
        html_content += f"<h2>{folder['name']} Tests</h2>"
        html_content += "<table><tr><th>ID</th><th>Test Case Name</th><th>Method</th><th>Endpoint</th><th>Expected Status</th></tr>"
        
        for i, request in enumerate(folder['item']):
            name = request['name']
            method = request['request']['method']
            url = request['request']['url']['raw']
            
            # Extract expected status from script
            expected_status = "Unknown"
            if 'event' in request:
                for event in request['event']:
                    if event['listen'] == 'test':
                        for line in event['script']['exec']:
                            if "pm.response.to.have.status" in line:
                                try:
                                    expected_status = line.split("(")[1].split(")")[0]
                                except:
                                    pass
            
            html_content += f"<tr><td>{i+1}</td><td>{name}</td><td class='method {method}'>{method}</td><td>{url}</td><td>{expected_status}</td></tr>"
        
        html_content += "</table>"

html_content += """
</body>
</html>
"""

with open('req7/test_report.html', 'w') as f:
    f.write(html_content)

print("Generated req7/test_report.html")
