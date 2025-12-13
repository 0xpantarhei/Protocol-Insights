#!/usr/bin/env python3
"""
Batch replace pbs.twimg.com image links in markdown files with proxy links
Use https://images.weserv.nl/?url= as proxy service
"""

import os
import re
from pathlib import Path

# Proxy service prefix
PROXY_PREFIX = "https://images.weserv.nl/?url="

def fix_image_links(content: str) -> tuple[str, int]:
    """
    Replace pbs.twimg.com links in content that are not using proxy
    
    Returns:
        (modified content, replacement count)
    """
    count = 0
    
    # Match markdown image syntax: ![](https://pbs.twimg.com/...)
    # But don't match links that already use proxy
    pattern = r'!\[([^\]]*)\]\((https://pbs\.twimg\.com/[^\)]+)\)'
    
    def replace_link(match):
        nonlocal count
        alt_text = match.group(1)
        url = match.group(2)
        
        # If already a proxy link, skip
        if PROXY_PREFIX in url:
            return match.group(0)
        
        # Build proxy link
        proxy_url = PROXY_PREFIX + url
        count += 1
        return f'![{alt_text}]({proxy_url})'
    
    new_content = re.sub(pattern, replace_link, content)
    return new_content, count

def process_file(file_path: Path) -> int:
    """Process a single file, return replacement count"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, count = fix_image_links(content)
        
        if count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ {file_path.name}: Replaced {count} links")
        else:
            print(f"- {file_path.name}: No replacement needed")
        
        return count
    except Exception as e:
        print(f"✗ {file_path.name}: Processing failed - {e}")
        return 0

def main():
    """Main function"""
    # Get post directory
    post_dir = Path(__file__).parent / "post"
    
    if not post_dir.exists():
        print(f"Error: Directory not found {post_dir}")
        return
    
    # Get all markdown files
    md_files = list(post_dir.glob("*.md"))
    
    if not md_files:
        print("No markdown files found")
        return
    
    print(f"Found {len(md_files)} markdown files\n")
    
    total_count = 0
    for md_file in sorted(md_files):
        count = process_file(md_file)
        total_count += count
    
    print(f"\nDone! Replaced {total_count} image links in total")

if __name__ == "__main__":
    main()

