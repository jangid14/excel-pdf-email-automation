import re

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.pdfencrypt import StandardEncryption

# ============================================================
# Password Protected Canvas
# ============================================================

class PasswordProtectedCanvas(canvas.Canvas):

    def __init__(self, filename, password, **kwargs):

        encryption = StandardEncryption(
            password,
            canPrint=1,
            canModify=0,
            canCopy=0,
            canAnnotate=0
        )

        kwargs["encrypt"] = encryption

        super().__init__(
            filename,
            **kwargs
        )


# ============================================================
# Helper Functions
# ============================================================

def clean_filename(value):

    value = str(value)

    value = re.sub(
        r'[<>:"/\\|?*]',
        '',
        value
    )

    value = value.strip()

    value = value.replace(
        " ",
        "_"
    )

    return value


def safe_text(value):

    if value is None:
        return ""

    return str(value)


def money(value):

    try:

        return f"{float(value):,.0f}"

    except:

        return safe_text(value)


def number(value):

    try:

        return f"{float(value):g}"

    except:

        return safe_text(value)


# ============================================================
# Draw Centered Text
# ============================================================

def draw_centered(
    pdf,
    text,
    x,
    y,
    font="Helvetica",
    size=8
):

    pdf.setFont(
        font,
        size
    )

    pdf.drawCentredString(
        x,
        y,
        safe_text(text)
    )


# ============================================================
# Draw Cell
# ============================================================

def draw_cell(
    pdf,
    x,
    y,
    width,
    height,
    text="",
    font="Helvetica",
    size=7,
    align="left"
):

    pdf.setFont(
        font,
        size
    )

    # Border
    pdf.rect(
        x,
        y,
        width,
        height
    )

    # Text position
    text = safe_text(text)

    if align == "center":

        pdf.drawCentredString(
            x + width / 2,
            y + height / 2 - size / 3,
            text
        )

    elif align == "right":

        pdf.drawRightString(
            x + width - 3,
            y + height / 2 - size / 3,
            text
        )

    else:

        pdf.drawString(
            x + 3,
            y + height / 2 - size / 3,
            text
        )


# ============================================================
# Draw Section Header
# ============================================================

def draw_section_header(
    pdf,
    x,
    y,
    width,
    height,
    title
):

    pdf.rect(
        x,
        y,
        width,
        height
    )

    draw_centered(
        pdf,
        title,
        x + width / 2,
        y + height / 2 - 3,
        font="Helvetica-Bold",
        size=8
    )


# ============================================================
# Main PDF Generator
# ============================================================

def create_pdf(row, output_path):

    # ========================================================
    # PASSWORD
    # ========================================================

    password = safe_text(
        row.get("Contact", "")
    ).strip()

    # Handle Excel values like 9876543210.0
    if password.endswith(".0"):

        password = password[:-2]

    if not password:

        raise ValueError(
            "Contact number is empty. "
            "Cannot create password protected PDF."
        )

    # ========================================================
    # Create PDF
    # ========================================================

    pdf = PasswordProtectedCanvas(
        str(output_path),
        password,
        pagesize=A4
    )

    page_width, page_height = A4

    # ========================================================
    # Page Settings
    # ========================================================

    left = 45
    right = 45

    table_width = page_width - left - right

    # Start near top
    y = page_height - 55

    # ========================================================
    # HEADER
    # ========================================================

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    pdf.drawCentredString(
        page_width / 2,
        y,
        "Civi-Tech Florencia Park Sapphire Resident Welfare Association"
    )

    y -= 13

    pdf.setFont(
        "Helvetica-Bold",
        9
    )

    pdf.drawCentredString(
        page_width / 2,
        y,
        "Sec-7, Vaishali, Ramprastha Green, Ghaziabad"
    )

    y -= 12

    # ========================================================
    # BASIC INFORMATION
    # ========================================================

    info_top = y

    row_height = 15

    label_width = 75

    # NAME
    draw_cell(
        pdf,
        left,
        y - row_height,
        label_width,
        row_height,
        "NAME",
        font="Helvetica",
        size=7
    )

    draw_cell(
        pdf,
        left + label_width,
        y - row_height,
        table_width - label_width,
        row_height,
        row.get("Name", ""),
        size=7
    )

    y -= row_height

    # TOWER
    draw_cell(
        pdf,
        left,
        y - row_height,
        label_width,
        row_height,
        "TOWER NO.",
        size=7
    )

    draw_cell(
        pdf,
        left + label_width,
        y - row_height,
        table_width - label_width,
        row_height,
        row.get("Tower No", ""),
        size=7
    )

    y -= row_height

    # FLAT
    draw_cell(
        pdf,
        left,
        y - row_height,
        label_width,
        row_height,
        "FLAT NO.",
        size=7
    )

    draw_cell(
        pdf,
        left + label_width,
        y - row_height,
        table_width - label_width,
        row_height,
        row.get("Flat No", ""),
        size=7
    )

    y -= row_height

    # METER
    draw_cell(
        pdf,
        left,
        y - row_height,
        label_width,
        row_height,
        "METER NO.",
        size=7
    )

    draw_cell(
        pdf,
        left + label_width,
        y - row_height,
        table_width - label_width,
        row_height,
        row.get("Meter No", ""),
        size=7
    )

    y -= row_height

    # FLAT AREA
    draw_cell(
        pdf,
        left,
        y - row_height,
        label_width,
        row_height,
        "FLAT AREA",
        size=7
    )

    draw_cell(
        pdf,
        left + label_width,
        y - row_height,
        table_width - label_width,
        row_height,
        row.get("Flat Area", ""),
        size=7
    )

    y -= row_height

    # MAIN LOAD + DG LOAD
    half = table_width / 2

    draw_cell(
        pdf,
        left,
        y - row_height,
        label_width,
        row_height,
        "MAIN LOAD(KVA)",
        size=7
    )

    draw_cell(
        pdf,
        left + label_width,
        y - row_height,
        65,
        row_height,
        number(row.get("Main Load KVA", "")),
        size=7
    )

    draw_cell(
        pdf,
        left + half,
        y - row_height,
        75,
        row_height,
        "D.G. LOAD(KVA)",
        size=7
    )

    draw_cell(
        pdf,
        left + half + 75,
        y - row_height,
        table_width / 2 - 75,
        row_height,
        number(row.get("DG Load KVA", "")),
        size=7
    )

    y -= row_height

    # DURATION + MONTH
    draw_cell(
        pdf,
        left,
        y - row_height,
        label_width,
        row_height,
        "DURATION (Days)",
        size=7
    )

    draw_cell(
        pdf,
        left + label_width,
        y - row_height,
        65,
        row_height,
        row.get("Duration Days", ""),
        size=7
    )

    draw_cell(
        pdf,
        left + half,
        y - row_height,
        75,
        row_height,
        "Month",
        size=7
    )

    draw_cell(
        pdf,
        left + half + 75,
        y - row_height,
        table_width / 2 - 75,
        row_height,
        row.get("Month", ""),
        size=7
    )

    y -= row_height + 4

    # ========================================================
    # FIXED MAINTENANCE BILL (A)
    # ========================================================

    draw_section_header(
        pdf,
        left,
        y - 18,
        table_width,
        18,
        "Fixed Maintenance Bill (A)"
    )

    y -= 18

    # Column widths
    col1 = 30
    col2 = 155
    col3 = 80
    col4 = 80
    col5 = table_width - (
        col1 + col2 + col3 + col4
    )

    header_height = 38

    # Headers
    draw_cell(
        pdf,
        left,
        y - header_height,
        col1,
        header_height,
        "S. No.",
        font="Helvetica-Bold",
        size=6,
        align="center"
    )

    draw_cell(
        pdf,
        left + col1,
        y - header_height,
        col2,
        header_height,
        "Description",
        font="Helvetica-Bold",
        size=6,
        align="center"
    )

    draw_cell(
        pdf,
        left + col1 + col2,
        y - header_height,
        col3,
        header_height,
        "Fix charge Rate(Rs./Sqft/KVA)",
        font="Helvetica-Bold",
        size=6,
        align="center"
    )

    draw_cell(
        pdf,
        left + col1 + col2 + col3,
        y - header_height,
        col4,
        header_height,
        "Per Day Fix Charge(Rs.)",
        font="Helvetica-Bold",
        size=6,
        align="center"
    )

    draw_cell(
        pdf,
        left + col1 + col2 + col3 + col4,
        y - header_height,
        col5,
        header_height,
        "Monthly Fix Charge(Rs.)",
        font="Helvetica-Bold",
        size=6,
        align="center"
    )

    y -= header_height

    maintenance_rows = [

        (
            "1",
            "Maintenance Charge",
            row.get("Maintenance Rate", ""),
            row.get("Maintenance Per Day", ""),
            row.get("Maintenance Monthly", "")
        ),

        (
            "2",
            "Main Supply Load (KVA)",
            row.get("Main Supply Rate", ""),
            row.get("Main Supply Per Day", ""),
            row.get("Main Supply Monthly", "")
        ),

        (
            "3",
            "D.G. Supply Load (KVA)",
            row.get("DG Supply Rate", ""),
            row.get("DG Supply Per Day", ""),
            row.get("DG Supply Monthly", "")
        ),

        (
            "4",
            "Secure Meter Charges",
            "",
            row.get("Meter Charges Per Day", ""),
            row.get("Meter Charges Monthly", "")
        )
    ]

    data_row_height = 18

    for item in maintenance_rows:

        draw_cell(
            pdf,
            left,
            y - data_row_height,
            col1,
            data_row_height,
            item[0],
            size=6,
            align="center"
        )

        draw_cell(
            pdf,
            left + col1,
            y - data_row_height,
            col2,
            data_row_height,
            item[1],
            size=6
        )

        draw_cell(
            pdf,
            left + col1 + col2,
            y - data_row_height,
            col3,
            data_row_height,
            number(item[2]),
            size=6,
            align="right"
        )

        draw_cell(
            pdf,
            left + col1 + col2 + col3,
            y - data_row_height,
            col4,
            data_row_height,
            number(item[3]),
            size=6,
            align="right"
        )

        draw_cell(
            pdf,
            left + col1 + col2 + col3 + col4,
            y - data_row_height,
            col5,
            data_row_height,
            money(item[4]),
            size=6,
            align="right"
        )

        y -= data_row_height

    # TOTAL
    total_height = 18

    draw_cell(
        pdf,
        left,
        y - total_height,
        col1 + col2 + col3 + col4,
        total_height,
        "TOTAL",
        font="Helvetica-Bold",
        size=7,
        align="right"
    )

    draw_cell(
        pdf,
        left + col1 + col2 + col3 + col4,
        y - total_height,
        col5,
        total_height,
        money(row.get("Maintenance Total", "")),
        font="Helvetica-Bold",
        size=7,
        align="right"
    )

    y -= total_height + 5

    # ========================================================
    # ELECTRICITY CONSUMPTION BILL
    # ========================================================

    draw_section_header(
        pdf,
        left,
        y - 18,
        table_width,
        18,
        "Electricity Consumption Bill (Main/D.G.) (B)"
    )

    y -= 18

    col1 = 30
    col2 = 180
    col3 = 100
    col4 = 75
    col5 = table_width - (
        col1 + col2 + col3 + col4
    )

    header_height = 32

    draw_cell(
        pdf,
        left,
        y - header_height,
        col1,
        header_height,
        "S. No.",
        font="Helvetica-Bold",
        size=6,
        align="center"
    )

    draw_cell(
        pdf,
        left + col1,
        y - header_height,
        col2,
        header_height,
        "Description",
        font="Helvetica-Bold",
        size=6,
        align="center"
    )

    draw_cell(
        pdf,
        left + col1 + col2,
        y - header_height,
        col3,
        header_height,
        "Consumed Unit",
        font="Helvetica-Bold",
        size=6,
        align="center"
    )

    draw_cell(
        pdf,
        left + col1 + col2 + col3,
        y - header_height,
        col4,
        header_height,
        "Unit Rate(Rs.)",
        font="Helvetica-Bold",
        size=6,
        align="center"
    )

    draw_cell(
        pdf,
        left + col1 + col2 + col3 + col4,
        y - header_height,
        col5,
        header_height,
        "Total Amt",
        font="Helvetica-Bold",
        size=6,
        align="center"
    )

    y -= header_height

    electricity_rows = [

        (
            "1",
            "Main Supply",
            row.get("Main Consumed Unit", ""),
            row.get("Main Unit Rate", ""),
            row.get("Main Total", "")
        ),

        (
            "2",
            "D.G Supply",
            row.get("DG Consumed Unit", ""),
            row.get("DG Unit Rate", ""),
            row.get("DG Total", "")
        )
    ]

    data_row_height = 18

    for item in electricity_rows:

        draw_cell(
            pdf,
            left,
            y - data_row_height,
            col1,
            data_row_height,
            item[0],
            size=6,
            align="center"
        )

        draw_cell(
            pdf,
            left + col1,
            y - data_row_height,
            col2,
            data_row_height,
            item[1],
            size=6
        )

        draw_cell(
            pdf,
            left + col1 + col2,
            y - data_row_height,
            col3,
            data_row_height,
            number(item[2]),
            size=6,
            align="right"
        )

        draw_cell(
            pdf,
            left + col1 + col2 + col3,
            y - data_row_height,
            col4,
            data_row_height,
            number(item[3]),
            size=6,
            align="right"
        )

        draw_cell(
            pdf,
            left + col1 + col2 + col3 + col4,
            y - data_row_height,
            col5,
            data_row_height,
            money(item[4]),
            size=6,
            align="right"
        )

        y -= data_row_height

    # Total electricity
    draw_cell(
        pdf,
        left,
        y - 18,
        col1 + col2 + col3 + col4,
        18,
        "Total",
        font="Helvetica-Bold",
        size=7,
        align="right"
    )

    draw_cell(
        pdf,
        left + col1 + col2 + col3 + col4,
        y - 18,
        col5,
        18,
        money(row.get("Electricity Total", "")),
        font="Helvetica-Bold",
        size=7,
        align="right"
    )

    y -= 18 + 5

    # ========================================================
    # GRAND TOTAL
    # ========================================================

    grand_height = 22

    draw_cell(
        pdf,
        left,
        y - grand_height,
        table_width * 0.70,
        grand_height,
        "Fixed Maintenance Bill + Electricity Consumption Bill",
        font="Helvetica-Bold",
        size=7,
        align="center"
    )

    draw_cell(
        pdf,
        left + table_width * 0.70,
        y - grand_height,
        table_width * 0.30,
        grand_height,
        money(row.get("Grand Total", "")),
        font="Helvetica-Bold",
        size=8,
        align="right"
    )

    y -= grand_height

    # ========================================================
    # AMOUNT IN WORDS
    # ========================================================

    words_height = 20

    draw_cell(
        pdf,
        left,
        y - words_height,
        table_width,
        words_height,
        f"In words: {row.get('Amount In Words', '')}",
        font="Helvetica",
        size=7
    )

    y -= words_height + 3

    # ========================================================
    # FINAL TOTAL
    # ========================================================

    draw_cell(
        pdf,
        left,
        y - 20,
        table_width * 0.70,
        20,
        "Total (A+B)",
        font="Helvetica-Bold",
        size=8,
        align="right"
    )

    draw_cell(
        pdf,
        left + table_width * 0.70,
        y - 20,
        table_width * 0.30,
        20,
        money(row.get("Grand Total", "")),
        font="Helvetica-Bold",
        size=8,
        align="right"
    )

    y -= 35

    # ========================================================
    # FOOTER
    # ========================================================

    pdf.setFont(
        "Helvetica",
        6
    )

    pdf.drawString(
        left,
        y,
        "*Subject to final reconciliation"
    )

    # ========================================================
    # Save PDF
    # ========================================================

    pdf.showPage()

    pdf.save()