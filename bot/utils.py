import logging
import os
import csv
import json
from datetime import datetime
from config.settings import REPORTS_DIR

logger = logging.getLogger(__name__)


class ReportGenerator:
    def __init__(self):
        self.reports_dir = REPORTS_DIR
        self._ensure_reports_dir()

    def _ensure_reports_dir(self):
        """Create reports directory if it doesn't exist"""
        try:
            os.makedirs(self.reports_dir, exist_ok=True)
            logger.info(f"Reports directory ready: {self.reports_dir}")
        except Exception as e:
            logger.error(f"Error creating reports directory: {e}")

    def export_to_csv(self, accounts):
        """Export accounts to CSV file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.reports_dir}matching_accounts_{timestamp}.csv"
            
            if not accounts:
                logger.warning("No accounts to export to CSV")
                return filename
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'username', 'full_name', 'url', 'follower_count',
                    'is_israeli', 'is_relevant_topic', 'is_inactive',
                    'analysis_date'
                ])
                writer.writeheader()
                
                for account in accounts:
                    writer.writerow({
                        'username': account.get('username'),
                        'full_name': account.get('full_name'),
                        'url': account.get('url'),
                        'follower_count': account.get('follower_count'),
                        'is_israeli': account.get('is_israeli'),
                        'is_relevant_topic': account.get('is_relevant_topic'),
                        'is_inactive': account.get('is_inactive'),
                        'analysis_date': account.get('analysis_date'),
                    })
            
            logger.info(f"CSV report saved: {filename}")
            return filename

        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            return None

    def export_to_json(self, accounts):
        """Export accounts to JSON file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.reports_dir}matching_accounts_{timestamp}.json"
            
            if not accounts:
                logger.warning("No accounts to export to JSON")
                return filename
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(accounts, f, indent=2, ensure_ascii=False)
            
            logger.info(f"JSON report saved: {filename}")
            return filename

        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            return None

    def generate_summary_report(self, accounts):
        """Generate a summary report"""
        try:
            summary = f"""
=== INSTAGRAM BOT SCAN SUMMARY ===
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Matching Accounts: {len(accounts)}

Matching Accounts:
{'-' * 80}
"""
            
            for account in accounts:
                summary += f"""
Username: {account.get('username')}
Full Name: {account.get('full_name', 'N/A')}
Followers: {account.get('follower_count', 0):,}
URL: {account.get('url', 'N/A')}
Analysis Date: {account.get('analysis_date', 'N/A')}
---"""
            
            summary += f"""
{'-' * 80}

Reports saved to: {self.reports_dir}
"""
            
            logger.info(summary)
            return summary

        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return None
