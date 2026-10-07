# Modular Subdomain Enumeration Tool

A lightweight Python tool for enumerating subdomains from multiple configurable sources.

## Features

* Multiple domains from a single input file
* Multiple configurable enumeration sources
* Automatic subdomain extraction
* Duplicate removal
* Alphabetically sorted output
* Simple CLI interface
* Built-in request delay and timeout

## Requirements

```bash
pip3 install requests
```

## Usage

Create a `domains.txt` file:

```text
wiseep.com
google.org
yahoo.net
```

Run:

```bash
python3 subdomain_enum.py --domains domains.txt --output subdomains.txt
```

The results are saved to:

```text
subdomains.txt
```

## Adding Sources

Enumeration sources can be added to `API_TEMPLATES`:

```python
API_TEMPLATES = [
    "https://crt.name/v1/search?apex={domain}",
    "https://app.agniops.in/v1/search?domain={domain}"
]
```

Use `{domain}` as the placeholder for the target domain.

## Output

The tool returns unique subdomains, for example:

```text
api.wiseep.com
app.wiseep.com
dev.wiseep.com
staging.wiseep.com
www.wiseep.com
```

## Use

Designed for authorized security assessments, penetration testing, bug bounty reconnaissance, and attack-surface discovery.

**Only use this tool against domains you own or have explicit permission to test.**
