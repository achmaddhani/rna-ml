#!/usr/bin/env python3
"""
Generate samplesheet.csv from FASTQ files and rename samples to ad_* / control_*.

- Scans a directory for *.fastq.gz
- Builds a DataFrame with columns: sample, fastq_1
- Maps SRR IDs to standardized sample names:
    SRR35582354–SRR35582363 -> ad_10 ... ad_1
    SRR35582364–SRR35582372 -> control_9 ... control_1
"""

from pathlib import Path
import sys
import pandas as pd


def build_name_map() -> dict:
    ad_ids = [f"SRR355823{n}" for n in range(54, 64)]        # 54–63 for AD (10 samples)
    control_ids = [f"SRR355823{n}" for n in range(64, 73)]   # 64–72 for Control (9 samples)

    name_map: dict[str, str] = {}

    n_ad = len(ad_ids)
    for i, sid in enumerate(ad_ids):
        name_map[sid] = f"ad_{n_ad - i}"

    n_ctrl = len(control_ids)
    for i, sid in enumerate(control_ids):
        name_map[sid] = f"control_{n_ctrl - i}"

    print(f"AD IDs: {ad_ids}")
    print(f"Control IDs: {control_ids}")
    print(f"Name map size: {len(name_map)}")

    return name_map


def main() -> int:
    data_dir = Path(
        "/Users/achmaddhani/SCCR/regulatory_analysis_faheem/alzheimer_data/fastqgz_copy"
    )
    output_csv = Path("samplesheet.csv")

    if not data_dir.exists():
        print(f"ERROR: data_dir does not exist: {data_dir}", file=sys.stderr)
        return 1

    fastqs = sorted(data_dir.glob("*.fastq.gz"))
    fastqs = [fq.resolve() for fq in fastqs]

    if not fastqs:
        print(f"ERROR: No *.fastq.gz files found in: {data_dir}", file=sys.stderr)
        return 1

    # Build initial dataframe
    rows = []
    for fq in fastqs:
        sample = fq.name.replace(".fastq.gz", "")
        rows.append({"sample": sample, "fastq_1": str(fq)})

    df = pd.DataFrame(rows)

    # Map SRR IDs to ad_* / control_*
    name_map = build_name_map()
    df["sample_mapped"] = df["sample"].map(name_map)

    # Warn if any samples didn't map
    unmapped = df[df["sample_mapped"].isna()]["sample"].tolist()
    if unmapped:
        print("WARNING: Some samples were not found in the mapping (left unmapped):")
        for s in unmapped:
            print(f"  - {s}")

    # Use mapped sample name when available, otherwise keep original
    df["sample"] = df["sample_mapped"].fillna(df["sample"])
    df = df.drop(columns=["sample_mapped"])

    df.to_csv(output_csv, index=False)
    print(f"Saved: {output_csv.resolve()}")
    print(f"Rows: {len(df)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
