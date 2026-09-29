import logging
from pathlib import Path

from config.config import INPUT_FILE, OUTPUT_DIR, LOG_DIR, LOG_FILE
from services.excel_service import read_excel, get_row_data
from services.pdf_service import create_pdf, clean_filename
from services.email_service import send_email


# ---------------------------------------------------------
# CREATE REQUIRED DIRECTORIES
# ---------------------------------------------------------

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# LOGGING
# ---------------------------------------------------------

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------

def main():

    print("\n" + "=" * 70)
    print(" ELECTRICITY BILL PDF + EMAIL AUTOMATION")
    print("=" * 70 + "\n")

    # -----------------------------------------------------
    # CHECK EXCEL FILE
    # -----------------------------------------------------

    if not Path(INPUT_FILE).exists():

        raise FileNotFoundError(
            f"Excel file not found:\n{INPUT_FILE}"
        )

    print(f"Reading Excel file:")
    print(f"{INPUT_FILE}\n")

    # -----------------------------------------------------
    # READ EXCEL
    # -----------------------------------------------------

    df = read_excel(INPUT_FILE)

    print(f"Records found: {len(df)}\n")

    # -----------------------------------------------------
    # COUNTERS
    # -----------------------------------------------------

    pdf_success = 0
    pdf_failed = 0

    email_success = 0
    email_failed = 0

    # -----------------------------------------------------
    # PROCESS EACH ROW
    # -----------------------------------------------------

    for index, row in df.iterrows():

        excel_row = index + 2

        print("\n" + "-" * 70)
        print(f"Processing Excel Row: {excel_row}")
        print("-" * 70)

        try:

            # -------------------------------------------------
            # GET ROW DATA
            # -------------------------------------------------

            data = get_row_data(row)

            name = data["Name"]
            flat_no = data["Flat No"]
            email = data["Email"]

            print(f"Name       : {name}")
            print(f"Flat No    : {flat_no}")
            print(f"Email      : {email}")

            # -------------------------------------------------
            # CREATE PDF FILE NAME
            # -------------------------------------------------

            filename = (
                f"{clean_filename(flat_no)}_"
                f"{clean_filename(name)}.pdf"
            )

            output_path = OUTPUT_DIR / filename

            # -------------------------------------------------
            # GENERATE PDF
            # -------------------------------------------------

            print("\n[1/2] Generating PDF...")

            create_pdf(
                data,
                output_path
            )

            print(f"      PDF created successfully:")
            print(f"      {output_path}")

            pdf_success += 1

            logger.info(
                f"PDF generated successfully: {filename}"
            )

            # -------------------------------------------------
            # SEND EMAIL
            # -------------------------------------------------

            print("\n[2/2] Sending email...")

            send_email(
                recipient=email,
                recipient_name=name,
                flat_no=flat_no,
                pdf_path=output_path
            )

            print("      EMAIL SENT SUCCESSFULLY")

            email_success += 1

            logger.info(
                f"Email sent successfully to {email}"
            )

        except Exception as error:

            print("\n      PROCESS FAILED")
            print(f"      Error: {error}")

            logger.exception(
                f"Row {excel_row} failed"
            )

            # Determine whether it was PDF/email failure
            if 'output_path' in locals() and Path(output_path).exists():
                email_failed += 1
            else:
                pdf_failed += 1

    # ---------------------------------------------------------
    # FINAL SUMMARY
    # ---------------------------------------------------------

    print("\n\n" + "=" * 70)
    print(" AUTOMATION COMPLETED")
    print("=" * 70)

    print(f"\nTotal records     : {len(df)}")

    print("\nPDF")
    print(f"  Successful      : {pdf_success}")
    print(f"  Failed          : {pdf_failed}")

    print("\nEMAIL")
    print(f"  Sent            : {email_success}")
    print(f"  Failed          : {email_failed}")

    print(f"\nPDF folder        : {OUTPUT_DIR}")
    print(f"Log file          : {LOG_FILE}")

    print("\n" + "=" * 70)


# ---------------------------------------------------------
# APPLICATION ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":

    try:

        main()

    except Exception as error:

        print("\n")
        print("=" * 70)
        print(" APPLICATION ERROR")
        print("=" * 70)

        print(error)

        logger.exception(
            "Application failed"
        )
