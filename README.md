# REAPR - Real-time Event Annotation & Processing Recorder

A Python-based real-time data collection system that monitors YouTube Live chat streams, filters messages by custom keywords (tags), stores events in a MySQL database, and synchronizes with Google Sheets for downstream analysis.

## Overview

REAPR was designed to capture and organize viewer-submitted events, requests, thoughts, and feedback from live stream chat in real-time. The system automatically detects tagged messages, persists them to a database, and maintains synchronization with cloud spreadsheets for collaborative review.

## Features

- **Real-time YouTube Chat Monitoring** - Captures live chat messages using the pytchat library
- **Keyword-based Filtering** - Detects and processes messages tagged with #EVENT, #REQUEST, #THOUGHT, or #FEEDBACK
- **MySQL Database Integration** - Persistent storage with automatic synchronization
- **Google Sheets Sync** - Bi-directional sync with Google Sheets for team collaboration
- **Automated Stream Detection** - Web scraping to dynamically discover active YouTube stream IDs
- **Containerized Deployment** - Docker-based deployment for easy scaling
- **Auto-restart Capability** - Built-in process monitoring and automatic recovery

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.9+ |
| Database | MySQL |
| Web Scraping | BeautifulSoup, Mechanize |
| Data Processing | Pandas |
| YouTube Integration | pytchat |
| Containerization | Docker |
| Cloud Integration | Google Sheets API |

## Architecture

```
YouTube Live Stream → REAPR (Chat Monitor) → MySQL Database
                                              ↓
                              Google Sheets (Sync)
```

## Prerequisites

- Python 3.9 or higher
- MySQL 5.7+
- Docker (optional, for containerized deployment)
- Google Sheets API credentials (for spreadsheet sync)

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/skinwalker-ranch-insiders/reapr.git
cd reapr
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure settings:
Edit `settings.py` with your configuration:
```python
s_login = 'your_insiders_email'
s_password = 'your_password'
db_server = 'localhost'
db_user = 'reapr_user'
db_passwd = 'your_password'
db_name = 'reapr_database'
sheet_id = 'your_google_sheet_id'
```

5. Database Setup:
```sql
CREATE DATABASE reapr_database;
CREATE TABLE yt_events (
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    YT_Tag VARCHAR(30),
    YT_DateTime DATETIME,
    YT_User VARCHAR(60),
    YT_Msg VARCHAR(200),
    IN_SS VARCHAR(1),
    PRIMARY KEY (id)
);
```

### Docker Deployment

```bash
docker build -t reapr .
docker run -d --name reapr --network host -v $(pwd):/usr/src/reapr reapr:latest sh ./rcloak.sh
```

## Usage

Run the application:
```bash
python3 reapr.py
```

The application will:
1. Authenticate with the Skinwalker Ranch website
2. Retrieve the current live stream ID
3. Begin monitoring YouTube chat in real-time
4. Process and store tagged messages automatically

## Project Structure

```
REAPR/
├── reapr.py          # Main application logic
├── settings.py       # Configuration variables
├── requirements.txt  # Python dependencies
├── Dockerfile        # Docker container definition
├── rcloak.sh        # Process monitoring script
└── README.md        # Project documentation
```

## Key Implementation Details

### Real-time Chat Processing
- Uses async chat capture via pytchat to handle high-volume live streams
- Regex-based tag detection for flexible message classification

### Database Operations
- MySQL connector for reliable data persistence
- Automatic synchronization with Google Sheets after each new event
- Tracks synchronization status to prevent duplicate entries

### Stream Discovery
- Automated YouTube stream ID retrieval via web scraping
- Handles authentication and session management

## Contributing

Contributions are welcome! This project was developed with contributions from:
- Robert Davies (@skinwalker-ranch-insiders)
- @johns67467 (MySQL integration)
- @Kris - We Have Fun (code review & suggestions)
- @John Neiberger (code review & suggestions)

## License

MIT License

## Acknowledgments

- [pytchat](https://pypi.org/project/pytchat/) for YouTube live chat integration
- Skinwalker Ranch Insiders community for testing and feedback
