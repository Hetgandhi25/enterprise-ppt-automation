import requests
from bs4 import BeautifulSoup
import re

URL = "http://27.54.160.8/devops/uatPortal/index.php/sessions/login"
USERNAME = "Shah.Manank"
PASSWORD = "Apr@2025"

session = requests.Session()

try:
    print("[*] Fetching login page...")
    r = session.get(URL, timeout=10)
    print(f"Status: {r.status_code}")
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    login_data = {}
    for input_tag in soup.find_all('input', type='hidden'):
        if input_tag.get('name'):
            login_data[input_tag.get('name')] = input_tag.get('value', '')
            
    user_input = soup.find('input', type='text') or soup.find('input', {'name': re.compile('user', re.I)})
    pass_input = soup.find('input', type='password')
    
    print(f"[*] Submitting AJAX login...")
    
    post_url = f"http://27.54.160.8/devops/uatPortal/index.php/sessions/login_check/?cmd=login&ref={USERNAME}&ip_add="
    
    # Send data as form-urlencoded which is what $.post does
    r2 = session.post(post_url, data={'user': USERNAME, 'pass': PASSWORD}, timeout=10)
    print(f"[*] Post Login Status: {r2.status_code}")
    print(f"[*] Response: {r2.text}")
    
    # 3. Analyze the dashboard
    print("[*] Fetching dashboard...")
    # typically after login_check, it redirects or you just go to the main page
    r3 = session.get("http://27.54.160.8/devops/uatPortal/index.php/home", timeout=10)
    
    with open("d:/CustPPTAutomation/backend/scratch/home_page.html", "w", encoding="utf-8") as f:
        f.write(r3.text)
        
    print("[*] Saved home page to home_page.html")
    print("[+] Login Successful!")
    dash_soup = BeautifulSoup(r3.text, 'html.parser')
    
    print("\n--- Dashboard Navigation Links ---")
    for a in dash_soup.find_all('a', href=True):
        if "javascript:" not in a['href'] and "#" != a['href']:
            print(f"{a.text.strip()}: {a['href']}")
            
    print("\n--- Customer Lists or Tables ---")
    for table in dash_soup.find_all('table'):
        print("Found a table:")
        headers = [th.text.strip() for th in table.find_all('th')]
        print(f"Headers: {headers}")
        rows = table.find_all('tr')[:5] 
        for row in rows:
            cols = [td.text.strip() for td in row.find_all('td')]
            if cols:
                print(cols)

except Exception as e:
    print(f"Error: {e}")
