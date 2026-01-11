import requests
import re
import sys

# Configuration
BASE_URL = "http://localhost:8080/web/index.php"
LOGIN_URL = f"{BASE_URL}/auth/login"
VALIDATE_URL = f"{BASE_URL}/auth/validate"
API_TEST_URL = f"{BASE_URL}/api/v2/performance/manage/reviews?limit=1"
USERNAME = "admin"
PASSWORD = "v*&3BSNES"

def get_authenticated_cookie():
    session = requests.Session()
    
    # 1. Get Login Page to fetch CSRF Token
    print(f"Fetching {LOGIN_URL}...")
    try:
        response = session.get(LOGIN_URL)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching login page: {e}")
        return None

    # Extract CSRF Token
    # Looking for :token="&quot;...&quot;"
    match = re.search(r':token="&quot;(.*?)&quot;"', response.text)
    if not match:
        print("Could not find CSRF token in login page.")
        # Fallback regex just in case
        match = re.search(r'name="_token" value="(.*?)"', response.text)
        if not match:
            print("Failed to extract CSRF token.")
            return None
    
    csrf_token = match.group(1)
    print(f"CSRF Token: {csrf_token[:10]}...")

    # 2. Perform Login
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "_token": csrf_token
    }
    
    print(f"Logging in to {VALIDATE_URL}...")
    try:
        # Don't follow redirects automatically so we can check for 302
        login_response = session.post(VALIDATE_URL, data=payload, allow_redirects=False)
    except Exception as e:
        print(f"Error during login POST: {e}")
        return None

    if login_response.status_code == 302:
        print("Login successful (302 Redirect).")
        location = login_response.headers.get('Location', '')
        print(f"Redirect Location: {location}")
    else:
        print(f"Login failed? Status Code: {login_response.status_code}")
        print(login_response.text[:500])
        # Sometimes it might return 200 if it renders the dashboard directly (unlikely for this app) or if it renders login page with error
        if "Invalid credentials" in login_response.text:
             print("Invalid credentials.")
             return None

    # 3. Extract Cookie
    cookies = session.cookies.get_dict()
    auth_cookie = cookies.get("_orangehrm")
    
    if not auth_cookie:
        print("No '_orangehrm' cookie found in session.")
        return None
    
    print(f"Extracted Cookie: {auth_cookie}")

    # 4. Verify Cookie
    print(f"Verifying cookie against API: {API_TEST_URL}")
    verify_response = session.get(API_TEST_URL)
    
    if verify_response.status_code == 200:
        print("Cookie verification SUCCESS (200 OK).")
        return auth_cookie
    else:
        print(f"Cookie verification FAILED. Status: {verify_response.status_code}")
        return None

if __name__ == "__main__":
    cookie = get_authenticated_cookie()
    if cookie:
        print(f"VALID_COOKIE:{cookie}")
    else:
        sys.exit(1)
