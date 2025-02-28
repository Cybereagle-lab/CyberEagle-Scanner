#!/usr/bin/env python3

import requests
import socket
import threading
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from pyfiglet import Figlet

# Global variables
visited_urls = set()
vulnerabilities = []
thread_lock = threading.Lock()

# Headers to mimic a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Function to display the CyberEagle banner
def display_banner():
    figlet = Figlet(font='slant')
    banner = figlet.renderText('CyberEagle')
    print(banner)
    print("Advanced Website Scanning Tool\n")

# Function to check for open ports
def port_scan(domain, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((domain, port))
        if result == 0:
            with thread_lock:
                print(f"[+] Port {port} is open on {domain}")
        sock.close()
    except Exception as e:
        with thread_lock:
            print(f"[-] Error scanning port {port}: {e}")

# Function to check for SQL injection vulnerability
def check_sql_injection(url):
    payloads = ["'", "\"", "' OR '1'='1", "\" OR \"1\"=\"1"]
    for payload in payloads:
        test_url = f"{url}{payload}"
        try:
            response = requests.get(test_url, headers=HEADERS, timeout=10)
            if "error" in response.text.lower() or "syntax" in response.text.lower():
                with thread_lock:
                    vulnerabilities.append(f"SQL Injection vulnerability found at: {test_url}")
                    print(f"[+] SQL Injection vulnerability found at: {test_url}")
                break
        except Exception as e:
            with thread_lock:
                print(f"[-] Error checking SQL Injection: {e}")

# Function to check for XSS vulnerability
def check_xss(url):
    payload = "<script>alert('XSS')</script>"
    test_url = f"{url}?q={payload}"
    try:
        response = requests.get(test_url, headers=HEADERS, timeout=10)
        if payload in response.text:
            with thread_lock:
                vulnerabilities.append(f"XSS vulnerability found at: {test_url}")
                print(f"[+] XSS vulnerability found at: {test_url}")
    except Exception as e:
        with thread_lock:
            print(f"[-] Error checking XSS: {e}")

# Function to check for insecure headers
def check_insecure_headers(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        headers = response.headers
        if "X-Frame-Options" not in headers:
            with thread_lock:
                vulnerabilities.append(f"Missing X-Frame-Options header at: {url}")
                print(f"[+] Missing X-Frame-Options header at: {url}")
        if "Content-Security-Policy" not in headers:
            with thread_lock:
                vulnerabilities.append(f"Missing Content-Security-Policy header at: {url}")
                print(f"[+] Missing Content-Security-Policy header at: {url}")
    except Exception as e:
        with thread_lock:
            print(f"[-] Error checking headers: {e}")

# Function to crawl the website
def crawl_website(url, max_pages=10):
    if url in visited_urls or len(visited_urls) >= max_pages:
        return
    visited_urls.add(url)
    print(f"[*] Crawling: {url}")

    try:
        # Ensure the URL has a scheme
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Check for vulnerabilities
        check_sql_injection(url)
        check_xss(url)
        check_insecure_headers(url)

        # Extract and follow links
        for link in soup.find_all("a", href=True):
            full_url = urljoin(url, link["href"])
            if urlparse(full_url).netloc == urlparse(url).netloc:  # Stay on the same domain
                crawl_website(full_url, max_pages)
    except Exception as e:
        with thread_lock:
            print(f"[-] Error crawling {url}: {e}")

# Function to save results to a file
def save_results(filename="scan_results.txt"):
    with open(filename, "w") as file:
        file.write("Website Scan Results:\n\n")
        file.write("Vulnerabilities Found:\n")
        for vuln in vulnerabilities:
            file.write(f"- {vuln}\n")
        file.write("\nVisited URLs:\n")
        for url in visited_urls:
            file.write(f"- {url}\n")
    print(f"[+] Results saved to {filename}")

# Main function
def main():
    display_banner()
    target_url = input("Enter the target URL (e.g., http://example.com): ").strip()

    # Ensure the URL has a scheme
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url

    target_domain = urlparse(target_url).netloc

    print("\n[+] Starting port scan...")
    ports = [80, 443, 8080, 22]  # Common ports to scan
    threads = []
    for port in ports:
        thread = threading.Thread(target=port_scan, args=(target_domain, port))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    print("\n[+] Crawling website and checking for vulnerabilities...")
    crawl_website(target_url, max_pages=10)

    print("\n[+] Saving results...")
    save_results()

    print("\n[+] Scan complete!")

if __name__ == "__main__":
    main()
