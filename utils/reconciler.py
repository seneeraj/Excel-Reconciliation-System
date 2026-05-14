import pandas as pd


# =====================================================
# CREATE COMPOSITE KEY
# =====================================================

def create_composite_key(
    df,
    columns
):

    temp_df = df[columns].copy()

    temp_df = temp_df.fillna("").astype(str)

    composite_key = temp_df.apply(
        lambda row: "||".join(
            row.str.strip().str.lower()
        ),
        axis=1
    )

    return composite_key


# =====================================================
# RECONCILIATION FUNCTION
# =====================================================

def reconcile_data(
    primary_df,
    secondary_df,
    mappings
):

    # =================================================
    # EXTRACT MAPPED COLUMNS
    # =================================================

    primary_columns = [
        item["primary"]
        for item in mappings
    ]

    secondary_columns = [
        item["secondary"]
        for item in mappings
    ]

    # =================================================
    # CREATE COMPOSITE KEYS
    # =================================================

    primary_keys = create_composite_key(
        primary_df,
        primary_columns
    )

    secondary_keys = create_composite_key(
        secondary_df,
        secondary_columns
    )

    # =================================================
    # FIND UNMATCHED ROWS
    # =================================================

    unmatched_mask = ~primary_keys.isin(
        secondary_keys
    )

    unmatched_df = primary_df.loc[
        unmatched_mask
    ].copy()

    # =================================================
    # ADD RECONCILIATION STATUS
    # =================================================

    unmatched_df[
        "Reconciliation_Status"
    ] = "Not Matched"

    # =================================================
    # ADD RECONCILIATION KEY
    # =================================================

    unmatched_df[
        "Reconciliation_Key"
    ] = primary_keys[
        unmatched_mask
    ].values

    # =================================================
    # MATCHED COUNT
    # =================================================

    matched_count = (
        len(primary_df)
        - len(unmatched_df)
    )

    return unmatched_df, matched_count