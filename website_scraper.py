import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import time
from typing import Dict, List, Optional
import logging
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WebsiteScraper:
    """
    A comprehensive web scraper to extract contact details, LinkedIn, emails, 
    and other information from websites.
    """
    
    def __init__(self, timeout: int = 10, delay: float = 2):
        """
        Initialize the scraper with headers to mimic a browser.
        
        Args:
            timeout: Request timeout in seconds
            delay: Delay between requests in seconds (be respectful!)
        """
        self.timeout = timeout
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch_website(self, url: str) -> Optional[str]:
        """
        Fetch the HTML content of a website.
        
        Args:
            url: Website URL
            
        Returns:
            HTML content or None if request fails
        """
        try:
            # Normalize URL
            if not url.startswith('http'):
                url = 'https://' + url
            
            logger.info(f"Fetching: {url}")
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout error while fetching {url}")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error while fetching {url}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_emails(self, content: str) -> List[str]:
        """
        Extract all email addresses from HTML content.
        
        Args:
            content: HTML content
            
        Returns:
            List of unique email addresses
        """
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, content)
        
        # Filter out common false positives and duplicates
        emails = [
            e.lower() for e in emails 
            if not any(x in e.lower() for x in ['example.com', 'test.com', 'sample.com'])
        ]
        
        return sorted(list(set(emails)))
    
    def extract_phone_numbers(self, content: str) -> List[str]:
        """
        Extract phone numbers from HTML content.
        
        Args:
            content: HTML content
            
        Returns:
            List of phone numbers
        """
        # Pattern for various phone formats
        phone_patterns = [
            r'\+?[1-9]\d{1,14}',  # International format
            r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}',  # (XXX) XXX-XXXX
            r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # XXX-XXX-XXXX
        ]
        
        phones = []
        for pattern in phone_patterns:
            found = re.findall(pattern, content)
            phones.extend(found)
        
        # Remove duplicates and filter short numbers
        phones = list(set([p for p in phones if len(re.sub(r'\D', '', p)) >= 10]))
        return sorted(phones)
    
    def extract_linkedin_url(self, content: str) -> Optional[str]:
        """
        Extract LinkedIn profile URL from HTML content.
        
        Args:
            content: HTML content
            
        Returns:
            LinkedIn URL or None
        """
        linkedin_patterns = [
            r'https?://(?:www\.)?linkedin\.com/company/[a-zA-Z0-9-]+/?',
            r'https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9-]+/?',
        ]
        
        for pattern in linkedin_patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(0)
        
        return None
    
    def extract_social_links(self, content: str) -> Dict[str, str]:
        """
        Extract various social media links from HTML content.
        
        Args:
            content: HTML content
            
        Returns:
            Dictionary of social media links
        """
        social_links = {}
        
        social_patterns = {
            'linkedin': r'https?://(?:www\.)?linkedin\.com/(?:company|in)/[^"]+|[^"]+',
            'twitter': r'https?://(?:www\.)?twitter\.com/[^"]+',
            'facebook': r'https?://(?:www\.)?facebook\.com/[^"]+',
            'instagram': r'https?://(?:www\.)?instagram\.com/[^"]+',
            'youtube': r'https?://(?:www\.)?youtube\.com/[^"]+',
            'github': r'https?://(?:www\.)?github\.com/[^"]+',
        }
        
        for platform, pattern in social_patterns.items():
            match = re.search(pattern, content)
            if match:
                social_links[platform] = match.group(0)
        
        return social_links
    
    def extract_contact_info(self, content: str) -> Dict[str, any]:
        """
        Extract address and contact information from HTML content.
        
        Args:
            content: HTML content
            
        Returns:
            Dictionary with contact information
        """
        soup = BeautifulSoup(content, 'html.parser')
        
        contact_info = {
            'email': None,
            'phone': None,
            'address': None
        }
        
        # Look for contact section
        contact_section = soup.find(
            ['div', 'section'], 
            {'class': re.compile('contact|footer', re.I)}
        )
        
        if contact_section:
            text = contact_section.get_text(separator=' ')
            
            # Extract emails from contact section
            emails = self.extract_emails(text)
            if emails:
                contact_info['email'] = emails
            
            # Extract phones from contact section
            phones = self.extract_phone_numbers(text)
            if phones:
                contact_info['phone'] = phones
        
        return contact_info
    
    def extract_meta_info(self, content: str, url: str) -> Dict[str, str]:
        """
        Extract meta information from HTML content.
        
        Args:
            content: HTML content
            url: Website URL
            
        Returns:
            Dictionary with meta information
        """
        soup = BeautifulSoup(content, 'html.parser')
        
        meta_info = {
            'title': None,
            'description': None,
            'keywords': None,
        }
        
        # Title
        title_tag = soup.find('title')
        if title_tag:
            meta_info['title'] = title_tag.get_text().strip()
        
        # Description
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag:
            meta_info['description'] = desc_tag.get('content', '').strip()
        
        # Keywords
        keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_tag:
            meta_info['keywords'] = keywords_tag.get('content', '').strip()
        
        return meta_info
    
    def scrape_website(self, website_name: str) -> Dict[str, any]:
        """
        Main method to scrape all details from a website.
        
        Args:
            website_name: Name or URL of the website
            
        Returns:
            Dictionary with all extracted information
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting scrape for: {website_name}")
        logger.info(f"{'='*60}")
        
        # Normalize URL
        if not website_name.startswith('http'):
            url = f"https://{website_name}"
        else:
            url = website_name
        
        # Fetch website content
        content = self.fetch_website(url)
        if not content:
            error_msg = f'Failed to fetch {website_name}'
            logger.error(error_msg)
            return {
                'website': website_name,
                'url': url,
                'status': 'failed',
                'error': error_msg,
                'timestamp': datetime.now().isoformat()
            }
        
        # Extract all information
        result = {
            'website': website_name,
            'url': url,
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'emails': self.extract_emails(content),
            'phone_numbers': self.extract_phone_numbers(content),
            'linkedin': self.extract_linkedin_url(content),
            'social_media': self.extract_social_links(content),
            'contact_info': self.extract_contact_info(content),
            'meta_info': self.extract_meta_info(content, url)
        }
        
        logger.info(f"Successfully scraped {website_name}")
        return result


def display_results(results: List[Dict]) -> None:
    """
    Display scraped results in a formatted way.
    
    Args:
        results: List of scrape results
    """
    for result in results:
        print(f"\n{'='*70}")
        print(f"WEBSITE: {result['website']}")
        print(f"URL: {result['url']}")
        print(f"Status: {result['status']}")
        
        if result['status'] == 'failed':
            print(f"Error: {result.get('error', 'Unknown error')}")
            print(f"{'='*70}")
            continue
        
        print(f"\nMETA INFORMATION:")
        print(f"  Title: {result['meta_info'].get('title', 'N/A')}")
        print(f"  Description: {result['meta_info'].get('description', 'N/A')[:100]}...")
        
        print(f"\nCONTACT DETAILS:")
        if result['emails']:
            print(f"  Emails: {', '.join(result['emails'][:5])}")
        else:
            print(f"  Emails: Not found")
        
        if result['phone_numbers']:
            print(f"  Phone Numbers: {', '.join(result['phone_numbers'][:5])}")
        else:
            print(f"  Phone Numbers: Not found")
        
        print(f"\nSOCIAL MEDIA & PROFESSIONAL:")
        if result['linkedin']:
            print(f"  LinkedIn: {result['linkedin']}")
        else:
            print(f"  LinkedIn: Not found")
        
        if result['social_media']:
            for platform, link in result['social_media'].items():
                print(f"  {platform.title()}: {link}")
        
        print(f"\nCONTACT INFO DETAILS:")
        contact = result['contact_info']
        if contact['email']:
            print(f"  Email(s): {', '.join(contact['email'][:3])}")
        if contact['phone']:
            print(f"  Phone(s): {', '.join(contact['phone'][:3])}")
        
        print(f"{'='*70}")


def save_results_to_json(results: List[Dict], filename: str = 'website_details.json') -> None:
    """
    Save scraped results to a JSON file.
    
    Args:
        results: List of scrape results
        filename: Output filename
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"Results saved to {filename}")
        print(f"\n✓ Results saved to {filename}")
    except IOError as e:
        logger.error(f"Error saving results to file: {e}")
        print(f"✗ Error saving results to file: {e}")


def main():
    """
    Main function to run the scraper.
    """
    print("\n" + "="*70)
    print("WEBSITE DETAILS SCRAPER")
    print("="*70)
    print("\nThis tool extracts contact information, LinkedIn, emails, and social")
    print("media links from websites.\n")
    
    # Get websites from user input
    print("Enter website names or URLs (comma-separated):")
    print("Examples: facebook.com, flipkart.com, github.com")
    print("Or: https://www.example.com, https://example2.com\n")
    
    user_input = input("Enter websites: ").strip()
    
    if not user_input:
        print("No websites provided. Using default examples...")
        websites = ['facebook.com', 'flipkart.com']
    else:
        websites = [site.strip() for site in user_input.split(',')]
    
    # Initialize scraper
    scraper = WebsiteScraper(timeout=15, delay=2)
    
    # Scrape websites
    results = []
    for idx, website in enumerate(websites, 1):
        if idx > 1:
            print(f"\nWaiting {scraper.delay} seconds before next request...")
            time.sleep(scraper.delay)
        
        result = scraper.scrape_website(website)
        results.append(result)
    
    # Display results
    display_results(results)
    
    # Save to JSON
    save_results_to_json(results)
    
    print("\n✓ Scraping completed!")


if __name__ == '__main__':
    main()