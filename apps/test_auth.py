#!/usr/bin/env python3
"""
Test script to debug Label Studio authentication issues
"""
import requests
import json
import sys

def test_label_studio_auth(base_url, api_key):
    """Test different authentication methods with Label Studio"""
    
    # Clean up the base URL
    base_url = base_url.rstrip('/')
    
    print(f"Testing Label Studio connection to: {base_url}")
    print(f"API Key: {api_key[:10]}..." if len(api_key) > 10 else f"API Key: {api_key}")
    print("-" * 50)
    
    # Test endpoints to try
    endpoints = [
        "/api/projects/",
        "/api/projects",
        "/api/dm/projects/",  # Some versions use dm (data manager)
    ]
    
    # Auth formats to try
    auth_formats = [
        ("Bearer", f"Bearer {api_key}"),
        ("Token", f"Token {api_key}"),
        ("API-Key", api_key),  # Some systems use this
    ]
    
    success = False
    
    for endpoint in endpoints:
        print(f"\nTesting endpoint: {endpoint}")
        
        for auth_name, auth_header in auth_formats:
            print(f"  Trying {auth_name} authentication...")
            
            try:
                url = f"{base_url}{endpoint}"
                headers = {"Authorization": auth_header}
                
                response = requests.get(url, headers=headers, timeout=10)
                
                print(f"    Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        print(f"    ✅ SUCCESS! Found {len(data)} projects")
                    elif isinstance(data, dict) and 'results' in data:
                        print(f"    ✅ SUCCESS! Found {len(data['results'])} projects")
                    else:
                        print(f"    ✅ SUCCESS! Response: {type(data)}")
                    
                    # Show first project if available
                    if isinstance(data, list) and data:
                        print(f"    First project: {data[0].get('title', 'No title')}")
                    elif isinstance(data, dict) and data.get('results'):
                        print(f"    First project: {data['results'][0].get('title', 'No title')}")
                    
                    success = True
                    return auth_name, endpoint, True
                    
                elif response.status_code == 401:
                    print(f"    ❌ 401 Unauthorized")
                elif response.status_code == 403:
                    print(f"    ❌ 403 Forbidden")
                elif response.status_code == 404:
                    print(f"    ❌ 404 Not Found")
                else:
                    print(f"    ❌ {response.status_code}: {response.text[:100]}")
                    
            except requests.exceptions.ConnectionError:
                print(f"    ❌ Connection failed - check if Label Studio is running")
            except requests.exceptions.Timeout:
                print(f"    ❌ Request timed out")
            except Exception as e:
                print(f"    ❌ Error: {e}")
    
    if not success:
        print("\n" + "="*50)
        print("❌ ALL AUTHENTICATION ATTEMPTS FAILED")
        print("\nTroubleshooting steps:")
        print("1. Check if Label Studio is running at the URL")
        print("2. Verify your API token is correct and not expired")
        print("3. Make sure you have the right permissions")
        print("4. Try generating a new API token in Label Studio")
        
    return None, None, False

def check_label_studio_version(base_url):
    """Try to get Label Studio version info"""
    try:
        # Try version endpoint (no auth needed usually)
        response = requests.get(f"{base_url.rstrip('/')}/version", timeout=5)
        if response.status_code == 200:
            version_info = response.json()
            print(f"Label Studio version: {version_info}")
            return version_info
    except:
        pass
    
    try:
        # Try health check
        response = requests.get(f"{base_url.rstrip('/')}/health", timeout=5)
        if response.status_code == 200:
            print("Label Studio health check: OK")
            return {"status": "healthy"}
    except:
        pass
    
    print("Could not determine Label Studio version")
    return None

if __name__ == "__main__":
    print("Label Studio Authentication Tester")
    print("=" * 40)
    
    # Get connection details
    base_url = input("Enter Label Studio URL (e.g., http://localhost:8080): ").strip()
    if not base_url:
        base_url = "http://localhost:8080"
    
    api_key = input("Enter your API key: ").strip()
    if not api_key:
        print("❌ API key is required")
        sys.exit(1)
    
    # Check version first
    print("\nChecking Label Studio status...")
    check_label_studio_version(base_url)
    
    # Test authentication
    auth_method, working_endpoint, success = test_label_studio_auth(base_url, api_key)
    
    if success:
        print(f"\n✅ Working configuration:")
        print(f"   URL: {base_url}")
        print(f"   Endpoint: {working_endpoint}")
        print(f"   Auth method: {auth_method}")
    else:
        print(f"\n❌ No working configuration found")