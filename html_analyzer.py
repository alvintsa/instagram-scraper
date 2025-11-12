"""
Instagram HTML Structure Analyzer
Helps analyze Instagram's HTML to improve scraper selectors.
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from login import perform_instagram_login
from browser_setup import setup_browser, close_browser


def save_page_structure(driver, post_url):
    """Save Instagram page structure for analysis"""
    print("Saving Instagram page structure for analysis...")
    
    # Navigate to post
    driver.get(post_url)
    time.sleep(5)
    
    # Wait for page to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
    except:
        pass
    
    # Save full page source
    timestamp = int(time.time())
    
    # 1. Save complete HTML
    html_filename = f"instagram_structure_{timestamp}.html"
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print(f"Complete HTML saved to: {html_filename}")
    
    # 2. Save screenshot for visual reference
    screenshot_filename = f"instagram_visual_{timestamp}.png"
    driver.save_screenshot(screenshot_filename)
    print(f"Screenshot saved to: {screenshot_filename}")
    
    return html_filename


def analyze_comment_structure(driver):
    """Analyze comment-specific HTML patterns"""
    print("\nAnalyzing comment structures...")
    
    analysis = {
        'all_spans': [],
        'dir_auto_spans': [],
        'links': [],
        'comment_containers': [],
        'potential_selectors': []
    }
    
    # Get all spans
    all_spans = driver.find_elements(By.CSS_SELECTOR, "span")
    analysis['all_spans'] = [(span.get_attribute('outerHTML')[:100], span.text[:50]) for span in all_spans[:20]]
    
    # Get spans with dir='auto'
    dir_auto_spans = driver.find_elements(By.CSS_SELECTOR, "span[dir='auto']")
    analysis['dir_auto_spans'] = [(span.get_attribute('outerHTML')[:100], span.text[:50]) for span in dir_auto_spans[:20]]
    
    # Get all links
    links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/']")
    analysis['links'] = [(link.get_attribute('href'), link.text[:30]) for link in links[:20]]
    
    # Try different container selectors
    potential_selectors = [
        "div.x5yr21d.xw2csxc.x1odjw0f.x1n2onr6",  # Current primary
        "div[class*='x5yr21d']",
        "div[style*='overflow']",
        "div[role='button']",
        "article div div div",
        "div:has(span[dir='auto'])",  # Modern CSS
    ]
    
    for selector in potential_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            analysis['potential_selectors'].append({
                'selector': selector,
                'count': len(elements),
                'sample_html': elements[0].get_attribute('outerHTML')[:200] if elements else None
            })
        except:
            analysis['potential_selectors'].append({
                'selector': selector,
                'count': 0,
                'error': 'Invalid selector'
            })
    
    return analysis


def generate_analysis_report(html_filename, analysis):
    """Generate detailed analysis report"""
    report_filename = f"analysis_report_{int(time.time())}.txt"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("INSTAGRAM HTML STRUCTURE ANALYSIS REPORT\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"HTML Source: {html_filename}\n")
        f.write(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # All spans analysis
        f.write("ALL SPAN ELEMENTS (first 20):\n")
        f.write("-" * 30 + "\n")
        for i, (html, text) in enumerate(analysis['all_spans']):
            f.write(f"{i+1}. HTML: {html}\n")
            f.write(f"   TEXT: {text}\n\n")
        
        # Dir='auto' spans
        f.write("SPANS WITH dir='auto' (first 20):\n")
        f.write("-" * 30 + "\n")
        for i, (html, text) in enumerate(analysis['dir_auto_spans']):
            f.write(f"{i+1}. HTML: {html}\n")
            f.write(f"   TEXT: {text}\n\n")
        
        # Links analysis
        f.write("USER PROFILE LINKS (first 20):\n")
        f.write("-" * 30 + "\n")
        for i, (href, text) in enumerate(analysis['links']):
            f.write(f"{i+1}. HREF: {href}\n")
            f.write(f"   TEXT: {text}\n\n")
        
        # Selector analysis
        f.write("POTENTIAL CONTAINER SELECTORS:\n")
        f.write("-" * 30 + "\n")
        for selector_info in analysis['potential_selectors']:
            f.write(f"Selector: {selector_info['selector']}\n")
            f.write(f"Count: {selector_info['count']}\n")
            if 'sample_html' in selector_info and selector_info['sample_html']:
                f.write(f"Sample: {selector_info['sample_html']}\n")
            if 'error' in selector_info:
                f.write(f"Error: {selector_info['error']}\n")
            f.write("\n")
    
    print(f"Analysis report saved to: {report_filename}")
    return report_filename


def main():
    """Main analysis function"""
    if len(sys.argv) != 2:
        print("Usage: python html_analyzer.py <instagram_post_url>")
        print("Example: python html_analyzer.py https://www.instagram.com/reel/ABC123/")
        sys.exit(1)
    
    load_dotenv()
    post_url = sys.argv[1]
    
    # Setup browser
    driver, wait = setup_browser(headless=False)
    
    try:
        print("Instagram HTML Structure Analyzer")
        print("=" * 40)
        
        # Login
        print("1. Logging into Instagram...")
        if not perform_instagram_login(driver, max_attempts=3):
            print("Login failed!")
            return
        
        # Save page structure
        print("2. Saving page structure...")
        html_filename = save_page_structure(driver, post_url)
        
        # Analyze structure
        print("3. Analyzing comment patterns...")
        analysis = analyze_comment_structure(driver)
        
        # Generate report
        print("4. Generating analysis report...")
        report_filename = generate_analysis_report(html_filename, analysis)
        
        print("\nAnalysis Complete!")
        print(f"Files generated:")
        print(f"  - HTML Source: {html_filename}")
        print(f"  - Analysis Report: {report_filename}")
        print(f"  - Screenshot: instagram_visual_*.png")
        
        print("\nRecommended next steps:")
        print("1. Open the HTML file in a text editor")
        print("2. Search for comment patterns")
        print("3. Look for consistent class names or attributes")
        print("4. Test new selectors in browser dev tools")
        print("5. Update scraper with improved selectors")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        close_browser(driver)


if __name__ == "__main__":
    main()