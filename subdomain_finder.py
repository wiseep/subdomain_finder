import argparse
import requests
import re
import os
import time

# --- CUSTOMIZABLE API TEMPLATES ---
# You can add new source URLs to this list by using {domain} as a placeholder.
API_TEMPLATES = [
    "https://crt.name/v1/search?apex={domain}",
    "https://app.agniops.in/v1/search?domain={domain}"
]

def extract_subdomains(text, base_domain):
    """
    Extracts all subdomains belonging to the base_domain from the response text using regex.
    """
    pattern = rf'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{{0,61}}[a-zA-Z0-9])?\.)+{re.escape(base_domain)}'
    found = re.findall(pattern, text, re.IGNORECASE)
    return set(found)

def main():
    # Define command line arguments
    parser = argparse.ArgumentParser(description="Modular Subdomain Enumeration Tool")
    parser.add_argument("--domains", required=True, help="Input txt file containing wildcard domains")
    parser.add_argument("--output", required=True, help="Output txt file to save unique subdomains")
    
    args = parser.parse_args()

    input_file = args.domains
    output_file = args.output

    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"[-] Error: File '{input_file}' not found!")
        return

    # Read domains from the input file
    with open(input_file, "r", encoding="utf-8") as f:
        domains = [line.strip() for line in f if line.strip()]

    if not domains:
        print(f"[-] The file '{input_file}' is empty.")
        return

    all_subdomains = set()

    print(f"[*] Starting to process a total of {domains} domains...\n".replace(str(domains), str(len(domains))))

    for domain_index, domain in enumerate(domains, 1):
        print(f"[+] [{domain_index}/{len(domains)}] Target Domain: {domain}")
        
        for template in API_TEMPLATES:
            url = template.format(domain=domain)
            print(f"    -> Querying: {url}")
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    subs = extract_subdomains(response.text, domain)
                    all_subdomains.update(subs)
                    print(f"       [Found]: {len(subs)} subdomains retrieved from this source.")
                else:
                    print(f"       [Warning]: HTTP Status Code {response.status_code}")
            except Exception as e:
                print(f"       [Error]: Could not connect -> {e}")

            # Wait for 5 seconds after each API request
            time.sleep(5)

        print("-" * 50)

    # Sort results alphabetically and write unique values to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        for sub in sorted(all_subdomains):
            f.write(sub + "\n")

    print(f"\n[✔] Process Completed!")
    print(f"[✔] Total unique subdomains found: {len(all_subdomains)}")
    print(f"[✔] Output saved to: {output_file}")

if __name__ == "__main__":
    main()
