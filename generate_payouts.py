import pandas as pd
import glob
import os
import re

# Create /payouts folder if not exists
os.makedirs("payouts", exist_ok=True)

# Load contacts data
contacts_df = pd.read_csv("contacts.csv", dtype={"Name": str, "Owner": str, "Share": float, "Address": str})

# Find tracker result files
result_files = glob.glob("tracker_results_*.csv")

# Regex to extract start and end dates from filename
filename_pattern = re.compile(r"tracker_results_(\d{4}_\d{2}_\d{2})_to_(\d{4}_\d{2}_\d{2})\.csv")

for file in result_files:
    filename = os.path.basename(file)
    match = filename_pattern.match(filename)

    if not match:
        print(f"[SKIP] Filename format not recognized: {filename}")
        continue

    # Normalize underscore dates to dashed
    start_date = match.group(1).replace("_", "-")
    end_date = match.group(2).replace("_", "-")


    start_date, end_date = match.groups()
    print(f"[PROCESS] {filename} (Date Range: {start_date} to {end_date})")

    try:
        df = pd.read_csv(file, dtype={"Name": str})
        merged_df = pd.merge(df, contacts_df, on="Name", how="inner")

        if merged_df.empty:
            print(f"[WARN] No matching names found in contacts for {filename}")
            continue

        merged_df["Payout"] = merged_df["Performance"] * merged_df["Share"]

        payouts_df = merged_df.groupby(["Owner", "Address"], as_index=False)["Payout"].sum()
        payouts_df["Total"] = payouts_df["Payout"].round(5)
        payouts_df.drop(columns=["Payout"], inplace=True)

        output_filename = f"payouts/payouts_{start_date}_to_{end_date}.csv"
        payouts_df.to_csv(output_filename, index=False)

        print(f"✅ Wrote: {output_filename}")

    except Exception as e:
        print(f"[ERROR] Failed to process {filename}: {e}")
