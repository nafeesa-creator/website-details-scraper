"""
Quick and Simple Website Scraper
Just run this file directly!
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import json

def scrape_website(website):
    """Simple function to scrape website details"""
    
    if not website.startswith('http'):
        website = 'https://' + website
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(website, headers=headers, timeout=10)
        content = response.text
        
        # Extract emails
        emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)))
        
        # Extract LinkedIn
        linkedin = re.search(r'https?://(?:www\.)?linkedin\.com/[^"]+', content)
        linkedin_url = linkedin.group(0) if linkedin else None
        
        # Extract social media
        twitter = re.search(r'https?://(?:www\.)?twitter\.com/[^"]+', content)
        facebook = re.search(r'https?://(?:www\.)?facebook\.com/[^"]+', content)
        
        # Get title
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find('title')
        title_text = title.get_text() if title else 'N/A'
        
        return {
            'website': website,
            'title': title_text,
            'emails': emails[:5],
            'linkedin': linkedin_url,
            'twitter': twitter.group(0) if twitter else None,
            'facebook': facebook.group(0) if facebook else None
        }
    
    except Exception as e:
        return {'website': website, 'error': str(e)}

# Main execution
if __name__ == '__main__':
    print("\n" + "="*60)
    print("QUICK WEBSITE SCRAPER")
    print("="*60 + "\n")
    
    websites = input("Enter websites (comma-separated): ").split(',')
    results = []
    
    for i, site in enumerate(websites):
        site = site.strip()
        if site:
            print(f"\nScraping {i+1}/{len(websites)}: {site}...")
            result = scrape_website(site)
            results.append(result)
            
            # Display result
            print(f"  Title: {result.get('title', 'N/A')}")
            print(f"  Emails: {len(result.get('emails', []))} found")
            print(f"  LinkedIn: {result.get('linkedin', 'Not found')}")
            print(f"  Twitter: {result.get('twitter', 'Not found')}")
            
            time.sleep(2)  # Be respectful
    
    # Save results
    with open('results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*60)
    print("✓ Results saved to results.json")
    print("="*60 + "\n")