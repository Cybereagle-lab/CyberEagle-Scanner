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

# Function to crawl the website
def crawl_website(url, max_pages=10):
    if url in visited_urls or len(visited_urls) >= max_pages:
        return
    visited_urls.add(url)
    print(f"[*] Crawling: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract and follow links
        for link in soup.find_all("a", href=True):
            full_url = urljoin(url, link["href"])
            if urlparse(full_url).netloc == urlparse(url).netloc:  # Stay on the same domain
                crawl_website(full_url, max_pages)
    except Exception as e:
        with thread_lock:
            print(f"[-] Error crawling {url}: {e}")

# Main function
def main():
    display_banner()
    target_url = input("Enter the target URL (e.g., http://example.com): ").strip()
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

    print("\n[+] Crawling website...")
    crawl_website(target_url, max_pages=10)

    print("\n[+] Scan complete!")

if __name__ == "__main__":
    main()
