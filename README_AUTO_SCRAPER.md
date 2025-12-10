# Instagram Auto Scraper - Username Mode

These scripts automatically discover and scrape all posts from an Instagram username using InstagramPrivSniffer integration.

## Prerequisites

1. **InstagramPrivSniffer** installed at `C:\Users\alvin\Desktop\InstagramPrivSniffer` (Windows) or `~/Desktop/InstagramPrivSniffer` (Mac/Linux)
2. **Instagram Comment Scraper** (this project) 
3. **Conda environment** named `11_10_scraper` activated

## Usage

### Windows
Run the batch file:
```bash
auto_scrape_username.bat
```

### Mac/Linux
Run the shell script:
```bash
./auto_scrape_username.sh
```

## How It Works

1. **User Input**: Prompts you to enter an Instagram username (without the @ symbol)
2. **Post Discovery**: Uses InstagramPrivSniffer to fetch all recent posts/reels from that username
3. **Automatic Scraping**: Runs the comment scraper on each discovered post with:
   - 30 scroll iterations per post
   - Auto-generated filenames: `{username}_1.csv`, `{username}_2.csv`, etc.
4. **Logging**: Creates a log file `auto_scrape_{username}_log.txt` with detailed progress

## Example

```
Enter Instagram username (without @): doobydobap
```

This will:
- Fetch all posts from @doobydobap
- Scrape comments from each post
- Save as: `doobydobap_1.csv`, `doobydobap_2.csv`, `doobydobap_3.csv`, etc.
- Log everything to: `auto_scrape_doobydobap_log.txt`

## Output Files

- **CSV files**: `{username}_{number}.csv` - Contains comments with metadata
- **Log file**: `auto_scrape_{username}_log.txt` - Contains execution details
- **Location**: `ig_Scraper/new_outputs/` directory

## Features

- ✅ Automatic post discovery
- ✅ Batch processing of all user posts
- ✅ Error handling and logging
- ✅ Cross-platform support (Windows/Mac/Linux)
- ✅ Post metadata extraction (caption, date, likes)
- ✅ Comment like counts extraction
- ✅ Automatic filename generation

## Troubleshooting

### "Failed to fetch posts from InstagramPrivSniffer"
- Ensure InstagramPrivSniffer is properly installed
- Check that the path to InstagramPrivSniffer is correct
- Make sure you have proper Instagram access

### "Conda environment activation failed"
- Ensure conda is installed and in PATH
- Verify the environment name is `11_10_scraper`
- Run: `conda activate 11_10_scraper` manually first

### "Could not find directory"
- Verify InstagramPrivSniffer is at the expected path
- Verify ig_Scraper is at the expected path
- Adjust paths in the script if needed