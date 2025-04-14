# Instagram Login Automation with Selenium

This project demonstrates how to use Selenium with Python to automate the Instagram login process.

## Prerequisites

- Python 3.6 or higher
- Chrome browser installed

## Installation

1. Clone this repository or download the files
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the script:

```bash
python instagram_login.py
```

The script will:
1. Open Chrome browser
2. Navigate to Instagram login page
3. Wait for you to enter your username and password securely
4. Attempt to log in to your account
5. Ask if you want to keep the browser open when finished

## Notes

- This is for educational purposes only
- Instagram may detect automated login attempts and might:
  - Request additional verification
  - Temporarily lock your account
  - Present CAPTCHAs to solve
- The script includes handling for cookie notices and basic error management
- Never share your login credentials with others

## Learning Points

This example demonstrates:
- Setting up Selenium WebDriver with Chrome
- Element location using various selectors (CSS, XPath)
- WebDriverWait for handling dynamic content
- Input field interaction
- Button clicking
- Basic error handling
- Secure password input

## Customization

You can modify the script to:
- Use a different browser (Firefox, Edge, etc.)
- Run in headless mode (no visible browser window)
- Add more automation steps after login 