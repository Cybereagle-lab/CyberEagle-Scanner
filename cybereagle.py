#!/usr/bin/env python3

import requests
import socket
import threading
import ssl
import argparse
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from pyfiglet import Figlet
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import pdfkit

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

# Function to check SSL/TLS vulnerabilities
def check_ssl_tls(url):
    try:
        hostname = urlparse(url).netloc
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                print(f"[+] SSL/TLS Certificate Info for {hostname}:")
                print(cert)
    except Exception as e:
        with thread_lock:
            print(f"[-] Error checking SSL/TLS for {url}: {e}")

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

# Function to enumerate subdomains
def enumerate_subdomains(domain, wordlist):
    print(f"[*] Enumerating subdomains for {domain}...")
    with open(wordlist, "r") as file:
        subdomains = file.read().splitlines()

    with ThreadPoolExecutor(max_workers=10) as executor:
        for subdomain in subdomains:
            full_domain = f"{subdomain}.{domain}"
            executor.submit(check_subdomain, full_domain)

def check_subdomain(subdomain):
    try:
        ip = socket.gethostbyname(subdomain)
        with thread_lock:
            print(f"[+] Found subdomain: {subdomain} -> {ip}")
    except socket.error:
        pass

# Function to bruteforce directories and files
def bruteforce_directories(url, wordlist):
    print(f"[*] Bruteforcing directories on {url}...")
    with open(wordlist, "r") as file:
        directories = file.read().splitlines()

    with ThreadPoolExecutor(max_workers=10) as executor:
        for directory in directories:
            full_url = urljoin(url, directory)
            executor.submit(check_directory, full_url)

def check_directory(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            with thread_lock:
                print(f"[+] Found directory: {url}")
    except Exception as e:
        with thread_lock:
            print(f"[-] Error checking directory {url}: {e}")

# Function to generate an HTML report
def generate_html_report(filename="report.html"):
    with open(filename, "w") as file:
        file.write("<h1>CyberEagle Scanner Report</h1>\n")
        file.write("<h2>Vulnerabilities Found</h2>\n<ul>\n")
        for vuln in vulnerabilities:
            file.write(f"<li>{vuln}</li>\n")
        file.write("</ul>\n<h2>Visited URLs</h2>\n<ul>\n")
        for url in visited_urls:
            file.write(f"<li>{url}</li>\n")
        file.write("</ul>\n")
    print(f"[+] HTML report saved to {filename}")

# Function to generate a PDF report
def generate_pdf_report(filename="report.pdf"):
    html_report = "report.html"
    generate_html_report(html_report)
    pdfkit.from_file(html_report, filename)
    print(f"[+] PDF report saved to {filename}")

# Main function
def main():
    display_banner()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="CyberEagle Scanner - Advanced Website Scanning Tool")
    parser.add_argument("target", help="Target URL or domain (e.g., http://example.com or example.com)")
    parser.add_argument("--subdomains", help="Path to subdomain wordlist file", default=None)
    parser.add_argument("--directories", help="Path to directory wordlist file", default=None)
    parser.add_argument("--report", help="Generate report in HTML or PDF format", choices=["html", "pdf"], default=None)
    args = parser.parse_args()

    target_url = args.target
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

    print("\n[+] Checking SSL/TLS configuration...")
    check_ssl_tls(target_url)

    if args.subdomains:
        print("\n[+] Enumerating subdomains...")
        enumerate_subdomains(target_domain, args.subdomains)

    if args.directories:
        print("\n[+] Bruteforcing directories...")
        bruteforce_directories(target_url, args.directories)

    print("\n[+] Crawling website and checking for vulnerabilities...")
    crawl_website(target_url, max_pages=10)

    if args.report:
        if args.report == "html":
            generate_html_report()
        elif args.report == "pdf":
            generate_pdf_report()

    print("\n[+] Scan complete!")

if __name__ == "__main__":
    main()
