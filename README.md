# CyberEagle Scanner 🦅


An advanced website scanning tool for ethical hacking and penetration testing.

---

## Features ✨

- **Port Scanning**: Scan for open ports on a target domain.
- **Vulnerability Detection**: Detect SQL Injection, XSS, and insecure headers.
- **Website Crawling**: Discover all pages and endpoints on a website.
- **Multi-Threading**: Fast and efficient scanning using multi-threading.
- **Easy to Use**: Simple command-line interface.

---

## Installation 🛠️

### Prerequisites
- Python 3.x
- `pip` package manager

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/CyberEagle-Scanner.git
   cd CyberEagle-Scanner
   pip install -r requirements.txt
   chmod +x cybereagle.py
   dos2unix cybereagle.py
   ## Install wkhtmltopdf (for PDF generation):
    ## pdfkit requires wkhtmltopdf to generate PDFs. Install it using:
        sudo apt install wkhtmltopdf
   
   ## Replace http://example.com with your target URL.

   ## Replace wordlist.txt with the path to your subdomain wordlist file.
   
        ./cybereagle.py http://example.com --subdomains subdomains.txt --directories directories.txt --report pdf
   
## Usage 🚀

Run the tool with the following command:

./cybereagle.py
          
## Example
Enter the target URL (e.g., http://example.com): http://example.com
CyberEagle-Scanner/
├── cybereagle.py
├── requirements.txt
├── README.md
├── subdomains.txt
├── directories.txt
└── report.pdf (generated after running the script)
## Contributing 🤝
We welcome contributions! Here's how you can help:

## Fork the repository.

Create a new branch:

## bash
git checkout -b feature/your-feature-name
Commit your changes:

## bash

git commit -m "Add your feature"
Push to the branch:

## bash
git push origin feature/your-feature-name
Open a pull request.

## License 📜
This project is licensed under the MIT License. See the LICENSE file for details.

## Support 💖
If you find this tool useful, consider giving it a ⭐ on GitHub!

## Contact 📧
For questions or feedback, feel free to reach out:

Email: eaglecyber9@gmail.com

GitHub Issues: Open an issue

Made with ❤️ by [Ubaid khan](https://github.com/Cybereagle-lab).  
If you have any questions, feel free to [Instagram](Cybereagle-lab).
