#!/usr/bin/env python3
"""
Test Personal Access Token authentication with Label Studio on port 8082
Based on official Label Studio documentation
"""
import requests
import json

def test_pat_authentication(pat_token):
    """Test PAT authentication following the official documentation"""
    
    base_url = "http://localhost:8082"
    
    print(f"Testing Label Studio PAT authentication on {base_url}")
    print(f"PAT Token: {pat_token[:20]}..." if len(pat_token) > 20 else f"PAT Token: {pat_token}")
    print("-" * 60)
    
    # Step 1: Test basic connectivity
    print("1. Testing basic connectivity...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   Health endpoint: {response.status_code}")
    except Exception as e:
        print(f"   Health check failed: {e}")
        try:
            response = requests.get(base_url, timeout=5)
            print(f"   Base URL: {response.status_code}")
        except Exception as e2:
            print(f"   ❌ Cannot connect to {base_url}: {e2}")
            return False
    
    # Step 2: Try PAT token refresh (official method)
    print("\n2. Testing PAT token refresh (official method)...")
    try:
        url = f"{base_url}/api/token/refresh"
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={"refresh": pat_token},
            timeout=10
        )
        
        print(f"   Refresh response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            access_token = data.get("access", "")
            if access_token:
                print(f"   ✅ Got access token: {access_token[:20]}...")
                
                # Test with the access token
                return test_with_access_token(base_url, access_token)
            else:
                print("   ❌ No access token in response")
        else:
            print(f"   ❌ Refresh failed: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Refresh error: {e}")
    
    # Step 3: Try direct PAT authentication (fallback)
    print("\n3. Testing direct PAT authentication (fallback)...")
    return test_direct_pat(base_url, pat_token)

def test_with_access_token(base_url, access_token):
    """Test API calls with the refreshed access token"""
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        params = {"page": 1, "page_size": 10}
        
        response = requests.get(f"{base_url}/api/projects/", headers=headers, params=params, timeout=10)
        
        print(f"   Projects API response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            project_count = len(data) if isinstance(data, list) else len(data.get('results', []))
            print(f"   ✅ SUCCESS! Found {project_count} projects")
            
            if project_count > 0:
                # Show first project
                first_project = data[0] if isinstance(data, list) else data.get('results', [{}])[0]
                title = first_project.get('title', 'No title')
                print(f"   First project: {title}")
            
            return True
        else:
            print(f"   ❌ Failed: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_direct_pat(base_url, pat_token):
    """Test direct PAT usage (some versions support this)"""
    methods = [
        ("Bearer (direct)", f"Bearer {pat_token}"),
        ("Token (legacy)", f"Token {pat_token}")
    ]
    
    for method_name, auth_header in methods:
        try:
            print(f"   Trying {method_name}...")
            headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json"
            }
            params = {"page": 1, "page_size": 10}
            
            response = requests.get(f"{base_url}/api/projects/", headers=headers, params=params, timeout=10)
            
            print(f"   Response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                project_count = len(data) if isinstance(data, list) else len(data.get('results', []))
                print(f"   ✅ SUCCESS with {method_name}! Found {project_count} projects")
                return True
            else:
                print(f"   ❌ Failed: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return False

if __name__ == "__main__":
    print("Label Studio Personal Access Token Tester")
    print("Based on: https://labelstud.io/guide/access_tokens")
    print("="*60)
    
    pat_token = input("Enter your Personal Access Token: ").strip()
    if not pat_token:
        print("❌ PAT token is required")
        exit(1)
    
    success = test_pat_authentication(pat_token)
    
    if success:
        print("\n🎉 Authentication successful!")
        print("You can now use this token in the main app.")
    else:
        print("\n❌ Authentication failed!")
        print("\nTroubleshooting:")
        print("1. Make sure Label Studio is running on port 8082")
        print("2. Verify your PAT token in Label Studio: Account & Settings → Access Token")
        print("3. Check if Personal Access Tokens are enabled for your organization")
        print("4. Try generating a new PAT token")
        print("5. Consider using Legacy Tokens instead if PAT doesn't work")