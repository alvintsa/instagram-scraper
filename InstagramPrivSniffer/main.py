"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission
"""

from core.accountDataFetcher import fetch_data 
from core.mediaDownloader import download_media
from lib.banner import printBanner
from utils.parser import getArguments

args = getArguments()

if args.name:
    printBanner()
    post_links = fetch_data(args.name)
    
    with open(f"{args.name}.txt", "w") as file:
        for link in post_links:
            file.write(link + "\n")
    
    
elif args.dload:
    printBanner()
    download_media(args.dload)