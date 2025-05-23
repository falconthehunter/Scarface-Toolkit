import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import subprocess

class Cloner:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.ssl_verify = True
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sites'))

    def clone_site(self, url, folder_name):
        """Core cloning functionality with proper directory structure"""
        try:
            # Create full output path
            output_dir = os.path.join(self.base_dir, folder_name)
            os.makedirs(output_dir, exist_ok=True)
            print(f"[*] Cloning: {url}")

            # Attempt cloning using wget first
            if self._try_wget_clone(url, output_dir):
                print(f"[+] Successfully cloned to: {output_dir}")
                return True

            # Fallback to Python-based cloning
            return self._python_clone_with_resources(url, output_dir)

        except Exception as e:
            print(f"[!] Error: {str(e)}")
            return False

    def _try_wget_clone(self, url, output_dir):
        """Wget cloning with proper directory handling"""
        try:
            cmd = [
                'wget',
                '--convert-links',
                '--adjust-extension',
                '--page-requisites',
                '--no-check-certificate' if not self.ssl_verify else '',
                '--no-host-directories',
                '--cut-dirs=1',
                '-U', self.user_agent,
                '-P', output_dir,
                url
            ]
            cmd = [arg for arg in cmd if arg]
            subprocess.run(cmd, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"[!] Error running wget: {str(e)}")
            return False

    def _python_clone_with_resources(self, url, output_dir):
        """Python-based cloning with resource handling"""
        try:
            req = requests.get(url, headers={'User-Agent': self.user_agent}, verify=self.ssl_verify)
            req.raise_for_status()
            soup = BeautifulSoup(req.text, 'html.parser')

            # Save main HTML
            main_file = os.path.join(output_dir, "index.html")
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print(f"[+] Main HTML saved as: {main_file}")

            # Download resources
            for tag, attr in [("link", "href"), ("script", "src"), ("img", "src")]:
                for resource in soup.find_all(tag):
                    resource_url = resource.get(attr)
                    if resource_url:
                        full_url = urljoin(url, resource_url)
                        self._download_resource(full_url, output_dir)

            return True
        except requests.RequestException as e:
            print(f"[!] Connection Error: {e}")
            return False

    def _download_resource(self, resource_url, output_dir):
        """Resource downloader with path handling"""
        try:
            response = requests.get(resource_url, 
                                   headers={'User-Agent': self.user_agent},
                                   verify=self.ssl_verify,
                                   stream=True)
            response.raise_for_status()

            # Create proper filename
            parsed_url = urlparse(resource_url)
            filename = os.path.basename(parsed_url.path) or "resource"
            filepath = os.path.join(output_dir, filename)

            # Ensure directory exists for nested resources
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"[+] Downloaded: {filename}")
        except requests.RequestException as e:
            print(f"[!] Failed to download: {resource_url} ({e})")

def main():
    print(r"""
                     __
 ___  ___ __ _ _ __ / _| __ _  ___ ___
/ __|/ __/ _` | '__| |_ / _` |/ __/ _ \
\__ \ (_| (_| | |  |  _| (_| | (_|  __/
|___/\___\__,_|_|  |_|  \__,_|\___\___|
    """)
    
    url = input("\nEnter target URL: ").strip()
    folder_name = input("Enter folder name (in sites/): ").strip()

    cloner = Cloner()
    if cloner.clone_site(url, folder_name):
        final_path = os.path.join(cloner.base_dir, folder_name)
        print(f"\n[+] Clone successful! Saved to: {final_path}")
    else:
        print("\n[!] Cloning failed")

if __name__ == "__main__":
    main()
