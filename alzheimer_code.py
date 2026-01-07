#!/usr/bin/env python3
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import requests
from pathlib import Path

data_dir = Path("/Users/achmaddhani/SCCR/regulatory_analysis_faheem/alzheimer_data/fastqgz_copy")

fastqs = list(data_dir.glob("*.fastq.gz"))
fastqs = [fq.resolve() for fq in fastqs]
fastqs


rows = []
for fq in fastqs:
    sample = fq.name.replace(".fastq.gz", "")
    rows.append({
        "sample": sample,
        "fastq_1": str(fq)
    })

df = pd.DataFrame(rows)


ad_ids = [f"SRR355823{n}" for n in range(54, 64)]      # 54–63 for AD
control_ids = [f"SRR355823{n}" for n in range(64, 73)]  # 64–72 for Control

print(f"AD_ids{ad_ids}, and control ids {control_ids}")

name_map = {}

n_ad = len(ad_ids)
for i, sid in enumerate(ad_ids):
    name_map[sid] = f"ad_{n_ad - i}"

n_ctrl = len(control_ids)
for i, sid in enumerate(control_ids):
    name_map[sid] = f"control_{n_ctrl - i}"
    
print(name_map)


df["sample"] = df["sample"].map(name_map)
df.to_csv("samplesheet.csv", index=False)
