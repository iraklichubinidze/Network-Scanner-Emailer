import subprocess
import os
import ipaddress

# Configuration
NMAP_PING_SCAN_OPTIONS = ["-sn"]                            # Don't Change; Ping scan (no port scan)
NMAP_PORT_SCAN_OPTIONS = ["-v", "-sV", "--open", "-T4"]     # Aggressive scan for live services
NMAP_OUTPUT_FORMAT = "-oG"                                  # Grepable output for ping scan
NMAP_SAVE_FORMAT = "-oN"                                    # Normal output for port scan

FILTER_TCPWRAPPED = True           # Remove lines with 'tcpwrapped' from results
ALLOWED_SUBNET_SIZE = 4096         # Prevent scanning overly large subnets


def get_live_ips(network):
    try:
        if ipaddress.ip_network(network, strict=False).num_addresses > ALLOWED_SUBNET_SIZE:
            print(f"Skipping {network}: subnet too large")
            return []

        cmd = ["nmap", *NMAP_PING_SCAN_OPTIONS, network, NMAP_OUTPUT_FORMAT, "-"]
        print(f"Running Nmap ping scan for network: {network}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        live_ips = []
        for line in result.stdout.splitlines():
            if "Host:" in line and "Status: Up" in line:
                parts = line.split()
                ip = parts[1]
                live_ips.append(ip)

        return live_ips
    except Exception as e:
        print(f"Error discovering live hosts for network {network}: {e}")
        return []

def scan_ips(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    results = {}
    with open(input_file, 'r') as f:
        ips_or_networks = [line.strip() for line in f.readlines()]

    print(f"Loaded IPs/Networks from {input_file}: {ips_or_networks}")

    for item in ips_or_networks:
        if not item:
            print("Skipping empty entry.")
            continue
            
        print(f"Processing {item}...")

        live_ips = get_live_ips(item) if '/' in item else [item]
        print(f"Live IPs discovered for {item}: {live_ips}")

        for ip in live_ips:
            sanitized_ip = ip.replace("/", "_")
            output_file = os.path.join(output_dir, f"{sanitized_ip}.txt")

            cmd = ["nmap", ip, *NMAP_PORT_SCAN_OPTIONS, NMAP_SAVE_FORMAT, output_file]
            print(f"Running Nmap scan for IP: {ip}")
            subprocess.run(cmd, stdout=subprocess.DEVNULL)

            if os.path.exists(output_file):
                with open(output_file, 'r') as result_file:
                    lines = result_file.readlines()

                if FILTER_TCPWRAPPED:
                    lines = [line for line in lines if "tcpwrapped" not in line]

                with open(output_file, 'w') as result_file:
                    result_file.writelines(lines)

                with open(output_file, 'r') as result_file:
                    results[ip] = result_file.read()
            else:
                print(f"Scan for {ip} failed or no results saved.")

    return results
