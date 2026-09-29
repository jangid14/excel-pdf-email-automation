import os
import smtplib

from pathlib import Path
from dotenv import load_dotenv
from email.message import EmailMessage


# Load .env
load_dotenv()


SMTP_SERVER = os.getenv(
    "SMTP_SERVER",
    "smtp.gmail.com"
)

SMTP_PORT = int(
    os.getenv(
        "SMTP_PORT",
        "587"
    )
)

EMAIL_ADDRESS = os.getenv(
    "EMAIL_ADDRESS",
    ""
).strip()

EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD",
    ""
).strip()


def validate_email_configuration():

    if not EMAIL_ADDRESS:
        raise ValueError(
            "EMAIL_ADDRESS is missing from .env"
        )

    if not EMAIL_PASSWORD:
        raise ValueError(
            "EMAIL_PASSWORD is missing from .env"
        )

    if len(EMAIL_PASSWORD) != 16:
        raise ValueError(
            "EMAIL_PASSWORD does not look like a "
            "Google App Password. Expected 16 characters."
        )


def send_email(
    recipient,
    recipient_name,
    flat_no,
    pdf_path
):

    # -----------------------------------------------------
    # Validate configuration
    # -----------------------------------------------------

    validate_email_configuration()

    # -----------------------------------------------------
    # Validate recipient
    # -----------------------------------------------------

    recipient = str(
        recipient
    ).strip()

    if not recipient:

        raise ValueError(
            f"Email address is empty for Flat {flat_no}"
        )

    # -----------------------------------------------------
    # Validate PDF
    # -----------------------------------------------------

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():

        raise FileNotFoundError(
            f"PDF not found:\n{pdf_path}"
        )

    if pdf_path.stat().st_size == 0:

        raise ValueError(
            f"PDF is empty:\n{pdf_path}"
        )

    # -----------------------------------------------------
    # Create email
    # -----------------------------------------------------

    message = EmailMessage()

    message["From"] = EMAIL_ADDRESS
    message["To"] = recipient

    message["Subject"] = (
        f"Electricity Bill - Flat {flat_no}"
    )

    message.set_content(
        f"""
Dear {recipient_name},

Please find attached your electricity bill.

The PDF is password protected.

Password:
Your registered contact number.

Regards,
Civi-Tech Florencia Park
Resident Welfare Association
"""
    )

    # -----------------------------------------------------
    # Attach PDF
    # -----------------------------------------------------

    with open(
        pdf_path,
        "rb"
    ) as file:

        pdf_data = file.read()

    message.add_attachment(
        pdf_data,
        maintype="application",
        subtype="pdf",
        filename=pdf_path.name
    )

    # -----------------------------------------------------
    # Connect to Gmail
    # -----------------------------------------------------

    print(
        f"      Connecting to "
        f"{SMTP_SERVER}:{SMTP_PORT}"
    )

    try:

        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT,
            timeout=30
        ) as server:

            print(
                "      SMTP connection successful."
            )

            server.starttls()

            print(
                "      TLS enabled."
            )

            server.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            print(
                "      SMTP login successful."
            )

            server.send_message(
                message
            )

            print(
                f"      Email sent to: {recipient}"
            )

    except smtplib.SMTPAuthenticationError as error:

        raise RuntimeError(
            "\nGMAIL AUTHENTICATION FAILED.\n"
            "Check your Google App Password.\n\n"
            f"Original error: {error}"
        )

    except smtplib.SMTPRecipientsRefused as error:

        raise RuntimeError(
            f"\nRecipient rejected:\n"
            f"{recipient}\n\n"
            f"Original error: {error}"
        )

    except smtplib.SMTPConnectError as error:

        raise RuntimeError(
            "\nCould not connect to Gmail SMTP.\n\n"
            f"Original error: {error}"
        )

    except smtplib.SMTPException as error:

        raise RuntimeError(
            f"\nSMTP error:\n{error}"
        )