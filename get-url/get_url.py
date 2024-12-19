import re
import requests

# Extract URLs from the file
def extract_urls(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    # Regular expression to find URLs
    urls = re.findall(r'https?://[^\s]+', content)
    return urls

# Fetch content and return HTTP error codes
def fetch_http_codes(urls):
    results = {}
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            results[url] = response.status_code
        except requests.RequestException as e:
            results[url] = str(e)
    return results

# Main execution
file_path = '/home/denis/Documentos/Projetos/python/globant-challenge/file.txt'
urls = extract_urls(file_path)

# Print located URLs
print("Located URLs:")
for url in urls:
    print(url)

# Fetch and print HTTP error codes
http_results = fetch_http_codes(urls)
print("\nHTTP Error Codes:")
for url, status in http_results.items():
    print(f"{url}: {status}")
