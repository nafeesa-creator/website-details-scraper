# Website Details Scraper

A Python web scraper to extract contact details, LinkedIn profiles, emails, and social media links from websites.

## Features

✅ Extract Email Addresses  
✅ Find Phone Numbers  
✅ Identify LinkedIn Profiles  
✅ Find Social Media Links (Twitter, Facebook, Instagram, YouTube, GitHub)  
✅ Extract Meta Information (Title, Description)  
✅ Contact Information Detection  
✅ Save Results to JSON  
✅ Error Handling & Logging  

## Quick Start

### 1. Install Python (if not already installed)
- Download from: https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Run the Scraper

**Option A: Full Featured Version**
```bash
python website_scraper.py
```

**Option B: Quick & Simple Version**
```bash
python quick_scraper.py
```

### 4. Enter Website URLs

When prompted, enter websites separated by commas:
```
facebook.com, flipkart.com, github.com
```

Or with full URLs:
```
https://www.facebook.com, https://www.flipkart.com
```

### 5. View Results

Results are displayed in the console and saved to `website_details.json` or `results.json`

## File Descriptions

- `website_scraper.py` - Full-featured scraper with detailed logging
- `quick_scraper.py` - Simple, lightweight version
- `requirements.txt` - Python dependencies
- `website_details.json` / `results.json` - Output files with scraped data

## Example Usage

```python
from website_scraper import WebsiteScraper

scraper = WebsiteScraper()
result = scraper.scrape_website('facebook.com')

print(result['emails'])
print(result['linkedin'])
print(result['social_media'])
```

## Output Format

```json
{
  "website": "facebook.com",
  "url": "https://facebook.com",
  "status": "success",
  "emails": ["contact@facebook.com", ...],
  "phone_numbers": ["+1-650-308-7300", ...],
  "linkedin": "https://linkedin.com/company/facebook",
  "social_media": {
    "twitter": "https://twitter.com/facebook",
    "instagram": "https://instagram.com/facebook"
  },
  "meta_info": {
    "title": "Facebook",
    "description": "..."
  }
}
```

## Important Notes

⚠️ **Legal & Ethical Considerations:**

1. Always check the website's `robots.txt` file
2. Respect the website's Terms of Service
3. Use this tool responsibly
4. Do not overload servers with requests
5. Consider using official APIs when available
6. This tool is for educational purposes only
7. Some websites may block scraping - this is normal

## Troubleshooting

**Problem: "ModuleNotFoundError: No module named 'requests'"**
- Solution: Run `pip install -r requirements.txt`

**Problem: "Connection refused" or "Timeout error"**
- The website might be blocking requests
- Try adding a larger delay in the code
- Check your internet connection

**Problem: No emails or phone numbers found**
- The website might not have this information on the homepage
- Try scraping a specific contact page URL

## License

This project is for educational purposes only.