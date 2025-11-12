# Instagram HTML Analysis Guide

## Quick Analysis Methods

### 1. Use the HTML Analyzer Tool
```bash
python html_analyzer.py https://www.instagram.com/reel/DPPr8SID-Dd/
```
This will generate:
- Complete HTML source file
- Analysis report with all selectors
- Screenshot for visual reference

### 2. Manual Browser Analysis

#### Step-by-Step Process:
1. **Open Instagram in Chrome/Firefox**
2. **Log in and navigate to a post with comments**
3. **Right-click on a comment → "Inspect Element"**
4. **Look for patterns in the HTML structure**

#### What to Look For:

##### Comment Container Patterns:
```html
<!-- Look for divs that contain both username and comment -->
<div class="x1234567 x8901234">  <!-- Container classes -->
    <a href="/username/"><span dir="auto">username</span></a>
    <span dir="auto">comment text</span>
</div>
```

##### Username Link Patterns:
```html
<!-- Username links usually look like this -->
<a href="/actual_username/" role="link">
    <span dir="auto">actual_username</span>
</a>
```

##### Comment Text Patterns:
```html
<!-- Comment text is typically in spans -->
<span dir="auto">This is the actual comment text</span>
```

### 3. Key Attributes to Investigate

#### Class Names:
- `x5yr21d`, `xw2csxc`, `x1odjw0f`, `x1n2onr6` (current container)
- Look for consistent patterns across multiple comments
- Instagram uses obfuscated class names that change periodically

#### Attributes:
- `dir="auto"` - User-generated content
- `role="button"` - Interactive elements  
- `aria-label` - Accessibility labels
- `data-*` - Custom data attributes

#### Structure Patterns:
- Parent-child relationships
- Sibling elements
- Nesting levels

### 4. Testing New Selectors

#### In Browser Console:
```javascript
// Test selectors in browser dev tools
document.querySelectorAll('span[dir="auto"]').length
document.querySelectorAll('div.x5yr21d').length

// Test specific patterns
document.querySelectorAll('div:has(a[href*="/"][href*="/"])')
```

#### In Python (Add to scraper for testing):
```python
# Test different selectors
test_selectors = [
    "span[dir='auto']",
    "div[class*='x5yr21d']", 
    "a[href*='/'][href!='#']",
    "div:has(span[dir='auto'])"  # Modern browsers only
]

for selector in test_selectors:
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        print(f"{selector}: {len(elements)} elements found")
    except Exception as e:
        print(f"{selector}: Error - {e}")
```

### 5. Common Instagram Patterns to Exploit

#### Text Directionality:
- `dir="auto"` = User content (comments, usernames)
- `dir="ltr"` = Interface text (buttons, labels)
- No `dir` = Static content

#### Link Patterns:
- User profiles: `/username/`
- Hashtags: `/explore/tags/hashtag/`
- Locations: `/explore/locations/`

#### Content Structure:
- Comments are usually nested 2-4 levels deep
- Username links precede comment text
- Timestamps follow comments
- Action buttons (Like/Reply) are siblings

### 6. Reliability Strategies

#### Fallback Selectors:
```python
selectors_hierarchy = [
    "div.x5yr21d.xw2csxc.x1odjw0f.x1n2onr6",  # Primary
    "div[class*='x5yr21d']",                    # Partial match
    "div[style*='overflow']",                   # Style-based
    "article div div",                          # Structure-based
]
```

#### Multi-Method Extraction:
1. **Container-based** (current method)
2. **Pattern matching** (consecutive spans)
3. **DOM traversal** (parent-child relationships)
4. **Text analysis** (natural language processing)

### 7. Monitoring Changes

#### Track Selector Success Rate:
```python
def test_selector_reliability(driver, selector):
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        return len(elements), True
    except:
        return 0, False

# Log results to track Instagram changes
```

#### Set Up Alerts:
- Monitor when extraction drops below threshold
- Test on multiple posts regularly  
- Compare results across different post types

### 8. Advanced Techniques

#### Dynamic Content Analysis:
- Wait for lazy-loaded comments
- Analyze AJAX requests for API endpoints
- Monitor network traffic for data patterns

#### Machine Learning Approach:
- Train on HTML patterns
- Classify elements as username/comment/noise
- Adapt to structural changes automatically

## Recommended Workflow

1. **Run html_analyzer.py** on multiple posts
2. **Compare patterns** across different post types  
3. **Identify most stable selectors**
4. **Test new selectors** in browser console
5. **Implement gradually** with fallbacks
6. **Monitor performance** over time
7. **Update when Instagram changes**

The key is to find multiple reliable patterns and have good fallback strategies!