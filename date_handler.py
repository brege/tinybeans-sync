#!/usr/bin/env python3
"""
Date handler orchestrator for Tinybeans downloads
"""
import argparse
from datetime import datetime, timedelta
from downloader import TinybeansDownloader
from history import DownloadHistory

class DateHandler:
    def __init__(self, config_path='config.yaml'):
        self.downloader = TinybeansDownloader(config_path)
        self.config = self.downloader.config
        # Use the same history instance as the downloader
        self.history = self.downloader.history
        
    def download_single_month(self, year, month):
        """Download all images for a single month"""
        print(f"Processing {year}-{month:02d}")
        return self.downloader.download_month(year, month)
    
    def download_date_range(self, start_date, end_date):
        """Download images for a date range (by months)"""
        print(f"Processing date range: {start_date} to {end_date}")
        
        current = start_date.replace(day=1)  # Start at beginning of month
        total_downloaded = 0
        
        while current <= end_date:
            year = current.year
            month = current.month
            
            print(f"\n{'='*50}")
            downloaded = self.download_single_month(year, month)
            total_downloaded += downloaded
            
            # Move to next month
            if month == 12:
                current = current.replace(year=year + 1, month=1)
            else:
                current = current.replace(month=month + 1)
        
        print(f"\n🎉 Total downloaded across all months: {total_downloaded}")
        return total_downloaded
    
    def get_from_last_date_range(self):
        """Get date range starting from last download timestamp"""
        latest = self.history.get_latest_timestamp()
        if latest is None:
            print("No download history found, starting from config dates")
            return None
        
        # Start from the day after the last download
        start_date = (latest + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
        
        print(f"Resuming from last download: {latest.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"New range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        return start_date, end_date
    
    def parse_date(self, date_str):
        """Parse date string in various formats"""
        formats = ['%Y-%m-%d', '%Y-%m', '%Y/%m/%d', '%m/%d/%Y']
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse date: {date_str}")

def main():
    parser = argparse.ArgumentParser(description='Tinybeans Date Handler - Download images by date range')
    parser.add_argument('--config', '-c', default='config.yaml', help='Config file path')
    parser.add_argument('--force', action='store_true', help='Ignore history and re-download everything')
    
    parser.add_argument('--from-last-date', action='store_true', help='Resume from last download')
    parser.add_argument('--after', metavar='DATE', help='Download on/after DATE (e.g., 2025-07-01)')
    parser.add_argument('--before', metavar='DATE', help='Download on/before DATE (e.g., 2025-08-31)')
    
    args = parser.parse_args()
    
    handler = DateHandler(args.config)
    
    # Pass force flag to downloader
    if args.force:
        handler.downloader.force = True
        print("🔄 Force mode: Ignoring download history")
    
    try:
        # Determine what dates to process
        if args.after:
            start_date = handler.parse_date(args.after)
            end_date = handler.parse_date(args.before) if args.before else datetime.now()
            handler.download_date_range(start_date, end_date)
            
        elif args.from_last_date:
            # Resume from last download
            date_range = handler.get_from_last_date_range()
            if date_range:
                start_date, end_date = date_range
                handler.download_date_range(start_date, end_date)
            else:
                print("No download history found. Use specific dates instead.")
                return 1
                
        else:
            # Use config defaults
            dates_config = handler.config.get('dates', {})
            
            if dates_config.get('from_last_date', False):
                # From last date mode
                date_range = handler.get_from_last_date_range()
                if date_range:
                    start_date, end_date = date_range
                    handler.download_date_range(start_date, end_date)
                else:
                    print("No download history found. Configure specific dates in config.yaml")
                    return 1
                    
            elif dates_config.get('single_date'):
                # Single date
                date_str = dates_config['single_date']
                if isinstance(date_str, str):
                    date_obj = handler.parse_date(date_str)
                    handler.download_single_month(date_obj.year, date_obj.month)
                    
            elif dates_config.get('after'):
                start_date = handler.parse_date(dates_config['after'])
                end_date_value = dates_config.get('before')
                end_date = handler.parse_date(end_date_value) if end_date_value else datetime.now()
                handler.download_date_range(start_date, end_date)
                
            else:
                print("No date configuration found. Use CLI arguments or configure dates in config.yaml")
                return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
