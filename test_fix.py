#!/usr/bin/env python3
"""
Test script to verify the Jinja2 template fix
"""

import requests
import time

def test_crossword_generation():
    """Test the crossword generation with a simple URL"""
    print("Testing crossword generation...")
    
    # Test URL
    url = "https://example.com"
    
    try:
        # Send POST request to generate crossword
        response = requests.post(
            'http://localhost:5000/generate',
            data={'url': url},
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            if "Your Crossword Puzzle" in content:
                print("✅ Success! Crossword puzzle generated without Jinja2 errors")
                return True
            elif "error" in content.lower():
                print("⚠️ Error in response (but no Jinja2 error):")
                print(content[:500])
                return False
            else:
                print("❌ Unexpected response format")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Jinja2 Template Fix")
    print("=" * 40)
    
    # Wait for Flask app to be ready
    print("Waiting for Flask app to be ready...")
    time.sleep(2)
    
    success = test_crossword_generation()
    
    if success:
        print("\n🎉 Test passed! The Jinja2 template error has been fixed.")
        print("The application should now work correctly.")
    else:
        print("\n❌ Test failed. There may still be issues.")
    
    print("\nTo use the application:")
    print("1. Open http://localhost:5000 in your browser")
    print("2. Enter a website URL")
    print("3. Generate a crossword puzzle") 