#!/usr/bin/env python3
"""
Quick Label Studio API test for port 8082
"""
import requests
import json

def test_label_studio_8082(api_key):
    """Test Label Studio on port 8082 with different auth methods"""
    
    base_url = "http://localhost:8082"
    
    print(f"Testing Label Studio on {base_url}")
    print(f"API Key: {api_key[:10]}..." if len(api_key) > 10 else f"API Key: {api_key}")
    print("-" * 50)
    
    # Test basic connectivity
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"Health check: {response.status_code}")
    except Exception as e:
        print(f"Health check failed: {e}")
        try:
            response = requests.get(base_url, timeout=5)
            print(f"Base URL check: {response.status_code}")
        except Exception as e2:
            print(f"Base URL failed: {e2}")
            return False
    
    # Test different auth methods
    auth_methods = [
        ("Bearer", f"Bearer {api_key}"),
        ("Token", f"Token {api_key}"),
    ]
    
    endpoints = ["/api/projects/", "/api/projects"]
    
    for endpoint in endpoints:
        print(f"\nTesting {endpoint}")
        for auth_name, auth_header in auth_methods:
            try:
                url = f"{base_url}{endpoint}"
                headers = {
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                }
                params = {"page": 1, "page_size": 10}
                
                print(f"  {auth_name}: ", end="")
                response = requests.get(url, headers=headers, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    project_count = len(data) if isinstance(data, list) else len(data.get('results', []))
                    print(f"✅ SUCCESS! {project_count} projects")
                    return True
                else:
                    print(f"❌ {response.status_code} - {response.text[:100]}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
    
    print("\n" + "="*50)
    print("❌ All authentication methods failed!")
    print("\nDebugging tips:")
    print("1. Check if Label Studio is actually running on port 8082")
    print("2. Try accessing http://localhost:8082 in your browser")
    print("3. Verify your API token in Label Studio settings")
    print("4. Check if you have the right permissions")
    return False

if __name__ == "__main__":
    # You can set your API key here for quick testing
    api_key = input("Enter your API key: ").strip()
    if api_key:
        test_label_studio_8082(api_key)
    else:
        print("API key required")