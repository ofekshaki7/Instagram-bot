# Instagram Bot - Israeli Inactive Accounts Monitor

זהו בוט המנטר עמודי אינסטגרם ישראלים עם יותר מ-10K עוקבים בתחומי אקטואליה, פוליטיקה וציבוריות שלא היו פעילים ב-3 חודשים האחרונים.

## Features 🎯

- Monitors Israeli Instagram accounts with 10K+ followers
- Filters by topics: Current events, Politics, Public figures
- Detects inactive accounts (no posts for 3+ months)
- Generates reports of potentially dormant accounts
- Data export to CSV/JSON

## Technology Stack 🛠️

- **Python 3.9+**
- **Instagrapi**: Instagram API wrapper
- **Pandas**: Data analysis and export
- **SQLite**: Local database for tracking
- **APScheduler**: Scheduled monitoring

## Project Structure 📁

```
.
├── bot/
│   ├── __init__.py
│   ├── instagram_client.py      # Instagram API interactions
│   ├── account_analyzer.py      # Account analysis logic
│   ├── database.py              # Database operations
│   └── utils.py                 # Utility functions
├── config/
│   ├── __init__.py
│   └── settings.py              # Configuration
├── reports/                     # Generated reports
├── main.py                      # Entry point
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/ofekshaki7/Instagram-bot.git
cd Instagram-bot
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Instagram credentials
```

## Usage 📖

```bash
python main.py
```

## Important Notes ⚠️

- Always comply with Instagram's Terms of Service
- Use a test account to avoid rate limiting
- Respect API rate limits (delays between requests)
- Store credentials securely in environment variables

## License 📄

MIT License
