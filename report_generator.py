from jinja2 import Template
import os

def generate_html_report(scan_results, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nmap Scan Results</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }
            h1 { color: #333; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f4f4f4; font-weight: bold; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
        <h1>Scan Results</h1>
        {% for ip, data in results.items() %}
            <h2>Scan for: {{ ip }}</h2>
            <table>
                <thead>
                    <tr>
                        <th>Port</th>
                        <th>State</th>
                        <th>Service Version</th>
                    </tr>
                </thead>
                <tbody>
                    {% for port, state, service_version in data %}
                    <tr>
                        <td>{{ port }}</td>
                        <td>{{ state }}</td>
                        <td>{{ service_version }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% endfor %}
    </body>
    </html>
    """

    structured_results = {}
    for ip, raw_result in scan_results.items():
        structured_results[ip] = []
        for line in raw_result.splitlines():
            if "/tcp" in line or "/udp" in line:
                parts = line.split()
                if len(parts) >= 3:
                    port_state = parts[0].split('/')[0]
                    state = parts[1]
                    service_version = " ".join(parts[2:])
                    structured_results[ip].append((port_state, state, service_version))
    
    template = Template(html_template)
    report_html = template.render(results=structured_results)

    output_file = os.path.join(output_dir, "scan_report.html")
    with open(output_file, 'w') as f:
        f.write(report_html)
    return output_file
