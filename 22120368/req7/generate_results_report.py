import json

with open('req7/newman_report.json', 'r') as f:
    data = json.load(f)

html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #ff7f00; }
        h2 { color: #333; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .pass { color: green; font-weight: bold; }
        .fail { color: red; font-weight: bold; }
        .summary { margin-bottom: 20px; font-size: 1.2em; }
    </style>
</head>
<body>
    <h1>OrangeHRM API Test Results</h1>
    <div class="summary">
"""

# Calculate Summary
total_tests = data['run']['stats']['requests']['total']
failed_tests = data['run']['stats']['requests']['failed']
passed_tests = total_tests - failed_tests
html_content += f"Total: {total_tests} | <span class='pass'>Passed: {passed_tests}</span> | <span class='fail'>Failed: {failed_tests}</span>"
html_content += """
    </div>
    <table>
        <tr>
            <th>Request Name</th>
            <th>Method</th>
            <th>Status Code</th>
            <th>Test Status</th>
        </tr>
"""

for execution in data['run']['executions']:
    name = execution['item']['name']
    method = execution['request']['method']
    
    status_code = "N/A"
    if 'response' in execution and execution['response']:
        status_code = execution['response']['code']
        
    # Check if assumptions failed
    has_fail = False
    if 'assertions' in execution:
        for assertion in execution['assertions']:
            if 'error' in assertion:
                has_fail = True
                break
    
    status_class = "fail" if has_fail else "pass"
    status_text = "FAIL" if has_fail else "PASS"
    
    html_content += f"<tr><td>{name}</td><td>{method}</td><td>{status_code}</td><td class='{status_class}'>{status_text}</td></tr>"

html_content += """
    </table>
</body>
</html>
"""

with open('req7/test_results.html', 'w') as f:
    f.write(html_content)

print("Generated req7/test_results.html")
