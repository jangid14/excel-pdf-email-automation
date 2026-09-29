import pandas as pd


REQUIRED_COLUMNS = [

    "Name",
    "Tower No",
    "Flat No",
    "Meter No",
    "Flat Area",

    "Main Load KVA",
    "DG Load KVA",

    "Duration Days",
    "Month",

    "Email",
    "Contact",

    "Maintenance Rate",
    "Maintenance Per Day",
    "Maintenance Monthly",

    "Main Supply Rate",
    "Main Supply Per Day",
    "Main Supply Monthly",

    "DG Supply Rate",
    "DG Supply Per Day",
    "DG Supply Monthly",

    "Meter Charges Per Day",
    "Meter Charges Monthly",

    "Maintenance Total",

    "Main Consumed Unit",
    "Main Unit Rate",
    "Main Total",

    "DG Consumed Unit",
    "DG Unit Rate",
    "DG Total",

    "Electricity Total",

    "Grand Total",

    "Amount In Words"
]

def read_excel(file_path):

    df = pd.read_excel(

        file_path,

        dtype={
            "Contact": str,
            "Flat No": str,
            "Tower No": str,
            "Meter No": str
        }
    )

    validate_excel(df)

    return df


def validate_excel(df):

    missing_columns = [

        column

        for column in REQUIRED_COLUMNS

        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(

            "Missing Excel columns:\n"
            + "\n".join(missing_columns)
        )

    if df.empty:

        raise ValueError(
            "Excel file is empty."
        )


def clean_value(value):

    if pd.isna(value):

        return ""

    return str(value).strip()


def get_row_data(row):

    data = {}

    for column in REQUIRED_COLUMNS:

        data[column] = clean_value(
            row[column]
        )

    return data