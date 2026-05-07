import logging
import sys
from datetime import datetime
from bot.instagram_client import InstagramClient
from bot.account_analyzer import AccountAnalyzer
from bot.database import Database
from bot.utils import ReportGenerator
from config.settings import TOPIC_KEYWORDS, ISRAELI_INDICATORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)
logger = logging.getLogger(__name__)


class InstagramBot:
    def __init__(self):
        self.client = InstagramClient()
        self.analyzer = AccountAnalyzer()
        self.database = Database()
        self.report_generator = ReportGenerator()

    def run(self):
        """Main bot execution"""
        logger.info("=== Starting Instagram Bot ===")
        
        # Step 1: Login
        if not self.client.login():
            logger.error("Failed to login. Exiting.")
            return False
        
        # Step 2: Search for potential accounts
        logger.info("Searching for potential accounts...")
        search_queries = [
            'ישראל חדשות',
            'israel news',
            'פוליטיקה ישראל',
            'relevant_il',
        ]
        
        accounts_to_analyze = []
        
        for query in search_queries:
            logger.info(f"Searching for: {query}")
            results = self.client.search_user(query)
            accounts_to_analyze.extend(results)
        
        logger.info(f"Found {len(accounts_to_analyze)} accounts to analyze")
        
        # Step 3: Get detailed info and analyze
        matching_accounts = []
        analyzed_count = 0
        
        for user in accounts_to_analyze:
            try:
                username = user.username if hasattr(user, 'username') else str(user)
                logger.info(f"Analyzing: {username}")
                
                user_info = self.client.get_user_info(username)
                if not user_info:
                    continue
                
                analyzed_count += 1
                
                # Save account info
                self.database.save_account(user_info)
                
                # Analyze account
                analysis = self.analyzer.analyze_account(user_info, self.client)
                self.database.save_analysis_result(analysis)
                
                # Check if matches criteria
                if analysis['matches_criteria']:
                    matching_accounts.append(analysis)
                    logger.info(f"✓ MATCH FOUND: {username} - {user_info.get('follower_count', 0)} followers")
                else:
                    logger.debug(f"✗ No match: {username}")
                    logger.debug(f"  Israeli: {analysis['is_israeli']}, "
                               f"Topic: {analysis['is_relevant_topic']}, "
                               f"Followers: {analysis['meets_follower_threshold']}, "
                               f"Inactive: {analysis['is_inactive']}")
            
            except Exception as e:
                logger.error(f"Error analyzing user: {e}")
                continue
        
        # Step 4: Save history and generate reports
        self.database.save_scan_history(analyzed_count, len(matching_accounts))
        
        # Step 5: Generate reports
        logger.info("Generating reports...")
        self.report_generator.export_to_csv(matching_accounts)
        self.report_generator.export_to_json(matching_accounts)
        summary = self.report_generator.generate_summary_report(matching_accounts)
        
        logger.info("=== Bot execution completed ===")
        logger.info(summary)
        
        return True

    def scan_specific_account(self, username):
        """Scan a specific account"""
        logger.info(f"Scanning specific account: {username}")
        
        if not self.client.login():
            logger.error("Failed to login")
            return None
        
        user_info = self.client.get_user_info(username)
        if not user_info:
            logger.error(f"Could not fetch info for {username}")
            return None
        
        analysis = self.analyzer.analyze_account(user_info, self.client)
        
        logger.info(f"Analysis for {username}:")
        logger.info(f"  - Israeli: {analysis['is_israeli']}")
        logger.info(f"  - Relevant topic: {analysis['is_relevant_topic']}")
        logger.info(f"  - Followers: {analysis['follower_count']} (meets threshold: {analysis['meets_follower_threshold']})")
        logger.info(f"  - Inactive: {analysis['is_inactive']}")
        logger.info(f"  - Matches criteria: {analysis['matches_criteria']}")
        
        return analysis


def main():
    """Main entry point"""
    bot = InstagramBot()
    
    # Option 1: Run full scan
    # bot.run()
    
    # Option 2: Scan specific account (for testing)
    bot.scan_specific_account('relevant_il')


if __name__ == '__main__':
    main()
