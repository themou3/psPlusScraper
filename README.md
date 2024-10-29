# Selenium Playstation Plus games scraper(parser)
Python script that uses Selenium and Webdriver to get .csv file with all free games (Extra, Premium subscriptions)
IDK why anyone would want this, but I wish it was like "SCRAPER" of all the ps subscription games on your account, but for known reasons this is impossible, and I decided to just create a parser that would collect in separate file games with links and the type of subscription.

& you don't need it, because there is already a page with all the free games here: https://www.playstation.com/ps-plus/games/

issues:
1. https://community.brave.com/t/login-to-store-playstation-com-fails-with-cant-connect-to-the-server-18-d7281102-1699006140-589a1d42/514265/
2. https://community.brave.com/t/cant-log-into-psn-or-playstation-store/122069/4
3. https://bugzilla.mozilla.org/show_bug.cgi?id=1638673

# Preconditions

0. Clone repository
1. latest Python with pip
2. installed requirements (pip install -r requirements)
3. latest Firefox

# Run

1. Run script (Windows: py ./psPlusScraper.py | Linux: python3 ./psPlusScraper.py)
2. Wait for the script to go through all the pages
3. Open .csv file in script directory/folder