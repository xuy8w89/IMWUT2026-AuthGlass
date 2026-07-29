# Dataset — Coming Soon

The AuthGlass recordings are not yet downloadable. This directory will hold the download script, the data-layout specification, and the official cross-validation splits.

**Read the full dataset card first:** [`../docs/dataset.md`](../docs/dataset.md)

## What lands here

- `download.py` / `download.sh` — fetch and verify the archives (checksums included)
- `LAYOUT.md` — the authoritative on-disk layout and file-naming scheme
- `metadata.csv` — subject and utterance IDs, volume level, anonymized demographics
- `splits/` — the subject-independent 7-fold splits used for every benchmark task, so published numbers stay comparable

## Size, roughly

30,240 samples × 16 channels × 96 kHz. Expect the raw archive to be **large**; a 16 kHz downsampled variant will be provided for users who only need commodity-device-equivalent data.

## Terms

The dataset was collected under IRB approval with informed consent for publication of anonymized recordings. By using it you agree not to attempt re-identification of participants, and not to use the data to build systems that impersonate or target individuals. See [`../LICENSE`](../LICENSE).

⭐ Watch this repository to be notified when the download opens.
