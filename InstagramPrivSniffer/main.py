"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission
"""

from core.accountDataFetcher import fetch_data 
from core.mediaDownloader import download_media
from lib.banner import printBanner
from utils.parser import getArguments

def main(args):

    if args.name:
        # printBanner()
        return fetch_data(args.name)
    elif args.dload:
        # printBanner()
        return download_media(args.dload)
    

if __name__ == "__main__":
    args = getArguments()
    main(args)