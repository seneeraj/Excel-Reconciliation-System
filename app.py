import streamlit as st
import pandas as pd

from utils.reconciler import reconcile_data
from utils.report_generator import generate_excel_report


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Excel Reconciliation System",
    page_icon="📊",
    layout="wide"
)


# =====================================================
# APPLICATION TITLE
# =====================================================

st.title("📊 Excel Reconciliation System")

st.markdown(
    """
    Upload Excel files, map columns dynamically,
    and reconcile unmatched records.
    """
)


# =====================================================
# HELPER FUNCTION
# =====================================================

def load_excel_file(file, sheet_name):

    df = pd.read_excel(
        file,
        sheet_name=sheet_name
    )

    # Clean column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df


# =====================================================
# SIDEBAR - FILE UPLOAD
# =====================================================

st.sidebar.header("📁 Upload Files")

primary_file = st.sidebar.file_uploader(
    "Upload Primary Excel File",
    type=["xlsx"]
)

secondary_files = st.sidebar.file_uploader(
    "Upload Secondary Excel Files",
    type=["xlsx"],
    accept_multiple_files=True
)


# =====================================================
# MAIN APPLICATION
# =====================================================

if primary_file:

    # =================================================
    # PRIMARY FILE CONFIGURATION
    # =================================================

    primary_excel = pd.ExcelFile(
        primary_file
    )

    primary_sheet = st.selectbox(
        "Select Primary Sheet",
        primary_excel.sheet_names
    )

    primary_df = load_excel_file(
        primary_file,
        primary_sheet
    )

    # =================================================
    # PRIMARY FILE PREVIEW
    # =================================================

    st.markdown("---")

    st.subheader("📄 Primary File Preview")

    st.dataframe(
        primary_df.head(),
        width="stretch"
    )

    st.info(
        f"Primary File Rows: {len(primary_df)} | "
        f"Columns: {len(primary_df.columns)}"
    )

    # =================================================
    # SECONDARY FILES
    # =================================================

    if secondary_files:

        secondary_configurations = []

        # =============================================
        # PROCESS EACH SECONDARY FILE
        # =============================================

        for file_index, file in enumerate(
            secondary_files
        ):

            st.markdown("---")

            st.header(
                f"📘 Secondary File: {file.name}"
            )

            secondary_excel = pd.ExcelFile(
                file
            )

            secondary_sheet = st.selectbox(
                f"Select Sheet - {file.name}",
                secondary_excel.sheet_names,
                key=f"sheet_{file_index}"
            )

            secondary_df = load_excel_file(
                file,
                secondary_sheet
            )

            # =========================================
            # SECONDARY PREVIEW
            # =========================================

            st.subheader(
                "📄 Secondary File Preview"
            )

            st.dataframe(
                secondary_df.head(),
                width="stretch"
            )

            st.info(
                f"Secondary File Rows: "
                f"{len(secondary_df)} | "
                f"Columns: "
                f"{len(secondary_df.columns)}"
            )

            # =========================================
            # COLUMN MAPPING SECTION
            # =========================================

            st.markdown("## 🔗 Column Mapping")

            st.markdown(
                """
                Select matching columns between
                Primary and Secondary files.
                """
            )

            mapping_count = st.number_input(
                f"Number of Column Mappings - "
                f"{file.name}",
                min_value=1,
                max_value=50,
                value=1,
                step=1,
                key=f"mapping_count_{file_index}"
            )

            column_mappings = []

            # =========================================
            # DYNAMIC MAPPING ROWS
            # =========================================

            for mapping_index in range(
                mapping_count
            ):

                st.markdown(
                    f"### Mapping "
                    f"{mapping_index + 1}"
                )

                left_col, right_col = st.columns(2)

                # =====================================
                # PRIMARY COLUMN SELECTION
                # =====================================

                with left_col:

                    primary_column = st.selectbox(
                        f"Primary Column "
                        f"{mapping_index + 1}",
                        options=(
                            primary_df.columns
                            .tolist()
                        ),
                        key=(
                            f"primary_"
                            f"{file_index}_"
                            f"{mapping_index}"
                        )
                    )

                # =====================================
                # SECONDARY COLUMN SELECTION
                # =====================================

                with right_col:

                    secondary_column = (
                        st.selectbox(
                            f"Secondary Column "
                            f"{mapping_index + 1}",
                            options=(
                                secondary_df
                                .columns
                                .tolist()
                            ),
                            key=(
                                f"secondary_"
                                f"{file_index}_"
                                f"{mapping_index}"
                            )
                        )
                    )

                # =====================================
                # STORE MAPPING
                # =====================================

                column_mappings.append({
                    "primary": primary_column,
                    "secondary": secondary_column
                })

            # =========================================
            # STORE FILE CONFIGURATION
            # =========================================

            secondary_configurations.append({
                "file_name": file.name,
                "df": secondary_df,
                "mappings": column_mappings
            })

        # =================================================
        # START RECONCILIATION
        # =================================================

        st.markdown("---")

        if st.button(
            "🚀 Start Reconciliation"
        ):

            unmatched_results = {}

            summary_data = []

            progress_bar = st.progress(0)

            total_files = len(
                secondary_configurations
            )

            # =============================================
            # PROCESS EACH FILE
            # =============================================

            for index, config in enumerate(
                secondary_configurations
            ):

                unmatched_df, matched_count = (
                    reconcile_data(
                        primary_df=primary_df,
                        secondary_df=config["df"],
                        mappings=config["mappings"]
                    )
                )

                unmatched_results[
                    config["file_name"]
                ] = unmatched_df

                summary_data.append({
                    "File Name": (
                        config["file_name"]
                    ),
                    "Primary Rows": (
                        len(primary_df)
                    ),
                    "Matched Rows": (
                        matched_count
                    ),
                    "Unmatched Rows": (
                        len(unmatched_df)
                    )
                })

                progress = (
                    (index + 1)
                    / total_files
                )

                progress_bar.progress(
                    progress
                )

            # =============================================
            # SUMMARY SECTION
            # =============================================

            st.success(
                "✅ Reconciliation "
                "Completed Successfully!"
            )

            summary_df = pd.DataFrame(
                summary_data
            )

            st.subheader(
                "📈 Reconciliation Summary"
            )

            st.dataframe(
                summary_df,
                width="stretch"
            )

            # =============================================
            # GENERATE REPORT
            # =============================================

            report_path = generate_excel_report(
                unmatched_results,
                summary_df
            )

            # =============================================
            # DOWNLOAD REPORT
            # =============================================

            with open(
                report_path,
                "rb"
            ) as f:

                st.download_button(
                    label=(
                        "📥 Download "
                        "Reconciliation Report"
                    ),
                    data=f,
                    file_name=(
                        "reconciliation_report.xlsx"
                    ),
                    mime=(
                        "application/vnd."
                        "openxmlformats-"
                        "officedocument."
                        "spreadsheetml.sheet"
                    )
                )

else:

    st.info(
        "📁 Please upload the "
        "Primary Excel File to begin."
    )