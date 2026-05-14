import pandas as pd
import os


# =====================================================
# GENERATE EXCEL REPORT
# =====================================================

def generate_excel_report(
    unmatched_results,
    summary_df
):

    os.makedirs(
        "outputs",
        exist_ok=True
    )

    output_path = (
        "outputs/reconciliation_report.xlsx"
    )

    with pd.ExcelWriter(
        output_path,
        engine="xlsxwriter"
    ) as writer:

        # =============================================
        # SUMMARY SHEET
        # =============================================

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        # =============================================
        # UNMATCHED SHEETS
        # =============================================

        for file_name, df in unmatched_results.items():

            sheet_name = (
                file_name
                .replace(".xlsx", "")
                .replace(".xls", "")
            )

            sheet_name = sheet_name[:31]

            if df.empty:

                empty_df = pd.DataFrame({
                    "Message": [
                        "No unmatched records found"
                    ]
                })

                empty_df.to_excel(
                    writer,
                    sheet_name=sheet_name,
                    index=False
                )

            else:

                df.to_excel(
                    writer,
                    sheet_name=sheet_name,
                    index=False
                )

    return output_path