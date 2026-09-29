# Electricity Bill PDF & Email Automation

A Python automation tool that reads electricity bill data from Excel, generates individual password-protected PDF bills, and automatically emails each PDF to the address specified in the corresponding Excel row.

## Features



- Read multiple bill records from Excel
- Generate one PDF per Excel row
- Generate a bill layout similar to the provided electricity bill format
- Password-protect every PDF
- Use the customer's **Contact** number as the PDF password
- Read the recipient from the Excel **Email** column
- Automatically attach and send PDFs through Gmail SMTP
- Meaningful PDF filenames using Flat No and Name
- Validate required Excel columns
- Handle row-level failures without stopping the entire batch
- Maintain application logs
- Keep email credentials in `.env`
- Can later be packaged as a Windows `.exe`

## Workflow

```text
Excel File
   |
   v
Read + Validate Excel
   |
   v
Generate Individual PDF
   |
   v
Password = Contact Number
   |
   v
Read Email Address
   |
   v
Attach PDF
   |
   v
Gmail SMTP
   |
   v
Customer Email
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| Pandas | Excel data processing |
| OpenPyXL | Reading `.xlsx` files |
| ReportLab | PDF generation and encryption |
| python-dotenv | Loading `.env` configuration |
| Gmail SMTP | Sending emails |
| Python Logging | Application/error logs |

## Project Structure

```text
excel_pdf_email_automation/
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
│
├── input/
│   └── electricity_bill.xlsx
│
├── output/
│   └── generated PDF files
│
├── logs/
│   └── automation.log
│
├── config/
│   ├── __init__.py
│   └── config.py
│
└── services/
    ├── __init__.py
    ├── excel_service.py
    ├── pdf_service.py
    └── email_service.py
```

## Prerequisites

- Python 3.10+
- VS Code or another Python IDE
- Gmail account for sending emails
- Google 2-Step Verification
- Google App Password

Check Python:

```bash
python --version
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/excel-pdf-email-automation.git
cd excel-pdf-email-automation
```

Create a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.env\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.env\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Or:

```bash
pip install pandas openpyxl reportlab python-dotenv
```

## Gmail Configuration

The application uses Gmail SMTP.

**Do not use your normal Gmail password.** Use a Google **App Password**.

Enable Google 2-Step Verification and create an App Password from your Google Account security settings.

Create `.env` in the project root:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=yourgmail@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop
```

Replace the email and App Password with your own values.

**Never commit `.env` to GitHub.**

## Excel Input

Place the Excel file here:

```text
input/electricity_bill.xlsx
```

The expected columns are:

```text
Name
Tower No
Flat No
Meter No
Flat Area
Main Load KVA
DG Load KVA
Duration Days
Month
Email
Contact
Maintenance Rate
Maintenance Per Day
Maintenance Monthly
Main Supply Rate
Main Supply Per Day
Main Supply Monthly
DG Supply Rate
DG Supply Per Day
DG Supply Monthly
Meter Charges Per Day
Meter Charges Monthly
Maintenance Total
Main Consumed Unit
Main Unit Rate
Main Total
DG Consumed Unit
DG Unit Rate
DG Total
Electricity Total
Grand Total
Amount In Words
```

### Important columns

| Column | Purpose |
|---|---|
| `Name` | Customer name |
| `Flat No` | Used in PDF filename |
| `Email` | Recipient email |
| `Contact` | PDF password |
| `Grand Total` | Total bill |
| `Amount In Words` | Amount displayed in words |

Example:

| Name | Tower No | Flat No | Contact | Email |
|---|---|---|---|---|
| Santosh Kumar Jain | T-7 | 602 | 9876543210 | customer@example.com |

The generated PDF password will be:

```text
9876543210
```

## Run the Application

From the project root:

```bash
python main.py
```

The application:

1. Reads the Excel file
2. Validates required columns
3. Processes each row
4. Generates a password-protected PDF
5. Reads the customer's email
6. Attaches the PDF
7. Connects to Gmail SMTP
8. Sends the email
9. Writes the result to the log

Example output:

```text
======================================================================
 ELECTRICITY BILL PDF + EMAIL AUTOMATION
======================================================================

Reading Excel file:
...\input\electricity_bill.xlsx

Records found: 3

----------------------------------------------------------------------
Processing Excel Row: 2
----------------------------------------------------------------------

Name       : Santosh Kumar Jain
Flat No    : 602
Email      : customer@example.com

[1/2] Generating PDF...
      PDF created successfully:
      ...\outputƂ_Santosh_Kumar_Jain.pdf

[2/2] Sending email...
      Connecting to smtp.gmail.com:587
      SMTP connection successful.
      TLS enabled.
      SMTP login successful.
      Email sent to: customer@example.com

      EMAIL SENT SUCCESSFULLY
```

Final summary:

```text
======================================================================
 AUTOMATION COMPLETED
======================================================================

Total records     : 3

PDF
  Successful      : 3
  Failed          : 0

EMAIL
  Sent            : 3
  Failed          : 0
```

## Output

Generated PDFs are stored in:

```text
output/
```

Example:

```text
output/
├── 602_Santosh_Kumar_Jain.pdf
├── 603_Rahul_Sharma.pdf
└── 604_Amit_Kumar.pdf
```

Each PDF is password protected using the corresponding Excel `Contact` value.

## Logging

Logs are stored in:

```text
logs/automation.log
```

The log records successful PDF generation, successful emails, and errors.

## Error Handling

Failures are handled at the individual-row level.

For example, if row 25 has an invalid email, the application can continue processing subsequent rows.

```text
Customer 1   -> PDF + Email
Customer 2   -> PDF + Email
...
Customer 25  -> Email Failed
Customer 26  -> PDF + Email
...
Customer 100 -> PDF + Email
```

## Gmail Troubleshooting

If you see:

```text
534 5.7.9 Application-specific password required
```

check:

1. 2-Step Verification is enabled.
2. A Google App Password was created.
3. The App Password is in `.env`.
4. The normal Gmail password was not used.
5. The App Password has not been revoked.
6. `.env` is in the project root.
7. `python-dotenv` is installed.

You can test whether the configuration is being loaded without printing the password:

```python
import os
from dotenv import load_dotenv

load_dotenv()

print("SMTP SERVER:", os.getenv("SMTP_SERVER"))
print("SMTP PORT:", os.getenv("SMTP_PORT"))
print("EMAIL:", os.getenv("EMAIL_ADDRESS"))

password = os.getenv("EMAIL_PASSWORD")

if password:
    print("PASSWORD FOUND")
    print("PASSWORD LENGTH:", len(password))
else:
    print("PASSWORD NOT FOUND")
```

Never print or share the actual App Password.

## Security

Never hard-code credentials:

```python
EMAIL_PASSWORD = "myrealpassword"
```

Use environment variables instead:

```python
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
```

Recommended `.gitignore`:

```gitignore
# Virtual environment
venv/
.venv/
env/

# Python
__pycache__/
*.py[cod]

# IDE
.vscode/
.idea/

# Environment variables
.env
.env.*

# Generated PDFs
output/*.pdf

# Logs
logs/*.log

# Customer Excel data
input/*.xlsx
input/*.xls

# Temporary files
*.tmp
*.temp

# OS files
.DS_Store
Thumbs.db
```

Customer Excel files and generated PDFs may contain personal information, so they should not be committed to a public repository.

## Testing

Before sending real bills, test with your own email address and one or two sample Excel rows.

Verify:

### PDF

- PDF opens correctly
- Password works
- Customer name is correct
- Flat number is correct
- Bill amount is correct
- Layout is correct

### Email

- Recipient is correct
- Subject is correct
- PDF is attached
- Attachment opens
- PDF password works
- Sender account is correct

## Architecture

```text
main.py
   |
   +-- excel_service.py
   |      |
   |      +-- Read Excel
   |      +-- Validate columns
   |      +-- Clean row values
   |
   +-- pdf_service.py
   |      |
   |      +-- Generate bill
   |      +-- Encrypt PDF
   |
   +-- email_service.py
          |
          +-- Gmail SMTP
          +-- Create email
          +-- Attach PDF
          +-- Send email
```

### `main.py`

Controls the complete workflow.

### `excel_service.py`

Reads and validates Excel data.

### `pdf_service.py`

Creates and password-protects electricity bill PDFs.

### `email_service.py`

Connects to Gmail SMTP, creates emails, attaches PDFs, and sends them.

### `config.py`

Stores project paths for input, output, and logs.

## Future Improvements

Possible next versions could include:

- Tkinter GUI
- Excel file picker
- Output-folder selection
- Gmail OAuth2
- Microsoft 365 support
- Other SMTP providers
- Custom email templates
- Retry failed emails
- Duplicate-email protection
- Email delivery dashboard
- Database integration
- ZIP download of generated PDFs
- Preview before sending
- Progress bar
- Windows `.exe`
- FastAPI web interface
- Background processing
- AWS S3 storage
- Docker deployment

## Build a Windows `.exe`

Install PyInstaller:

```bash
pip install pyinstaller
```

Build:

```bash
pyinstaller --onefile --name ExcelBillAutomation main.py
```

For a GUI application:

```bash
pyinstaller --onefile --windowed --name ExcelBillAutomation main.py
```

The executable will be created in:

```text
dist/ExcelBillAutomation.exe
```

## GitHub

Initialize Git:

```bash
git init
```

Check files:

```bash
git status
```

Add files:

```bash
git add .
```

Commit:

```bash
git commit -m "Initial electricity bill automation project"
```

Rename branch:

```bash
git branch -M main
```

Add the GitHub repository:

```bash
git remote add origin https://github.com/YOUR_USERNAME/excel-pdf-email-automation.git
```

Push:

```bash
git push -u origin main
```

Before `git add .`, always verify that `.env`, customer Excel data, generated PDFs, passwords, and other secrets are excluded.

## Use Cases

This automation can be useful for:

- Resident Welfare Associations
- Apartment societies
- Property management companies
- Utility billing teams
- Facility management companies
- Small businesses generating recurring invoices
- Rental/property management teams

Instead of manually generating and emailing hundreds of bills, the process can be automated from a single Excel file.

## Author

**Deepanshu Jangid**

Java Backend Developer | Python Automation | Backend Engineering

This project demonstrates practical experience with:

- Python automation
- Excel processing
- PDF generation
- PDF encryption
- SMTP email automation
- Error handling
- Logging
- Environment variables
- Git/GitHub

## License

Add an appropriate open-source license before distributing the project publicly or commercially.
