# AuthGlass Dataset

The AuthGlass recordings are hosted on Hugging Face:

**[huggingface.co/datasets/JZ0102/AuthGlass_Dataset](https://huggingface.co/datasets/JZ0102/AuthGlass_Dataset)**

~188 GB in total, as eight tar archives (~23.5 GB each). Read the full dataset card first: [`../docs/dataset.md`](../docs/dataset.md).

## Download

```bash
pip install -U huggingface_hub

python download.py                       # everything, into ./AuthGlass
python download.py --genuine --sets 1 7  # genuine speech + attack sets 1 and 7
python download.py --sets 2 --extract    # one archive, untar after download
```

`download.py` wraps `huggingface_hub.hf_hub_download` with resumable transfers. You can also grab individual archives from the Hugging Face page or with the CLI:

```bash
hf download JZ0102/AuthGlass_Dataset data_noattack.tar --repo-type dataset --local-dir AuthGlass
```

## Archives

| Archive | Condition | Size |
| :-- | :-- | --: |
| `data_noattack.tar` | Genuine wearer speech | 23.5 GB |
| `attack_1_artificial_throat.tar` | Set 1 — wearer-based replay via GRAS 45BC KEMAR torso–mouth simulator | 23.5 GB |
| `attack_2_front_100.tar` | Set 2 — loudspeaker 100 cm in front | 23.5 GB |
| `attack_3_right_100.tar` | Set 3 — loudspeaker 100 cm to the right | 23.5 GB |
| `attack_4_back_100.tar` | Set 4 — loudspeaker 100 cm behind | 23.5 GB |
| `attack_5_left_100.tar` | Set 5 — loudspeaker 100 cm to the left | 23.5 GB |
| `attack_6_front_50.tar` | Set 6 — loudspeaker 50 cm in front | 23.5 GB |
| `attack_7_front_25.tar` | Set 7 — loudspeaker 25 cm in front | 23.5 GB |

## Layout

Each archive extracts to one top-level folder, with one sub-folder per subject and one recording per passphrase:

```
data_noattack/
├── 01/
│   ├── samp1/output.npy        # passphrase 1, all 6 utterances (3 volumes × 2 repeats) in one take
│   ├── samp2/output.npy
│   ├── ...
│   ├── samp15/output.npy
│   └── phoneme/
│       ├── samp1.csv           # MAUS segmentation for samp1 (see below)
│       └── ...
├── 02/
└── ... /42/

attack_N_<condition>/
└── <subject>/samp<k>/output.npy          # sets 1, 4, 5, 6, 7 (+ phoneme/ as above)
└── <subject>/samp<k>/output_attack.npy   # sets 2, 3
```

- `samp1` … `samp15` correspond to the 15 passphrases listed in the dataset card (§5).
- Each `output*.npy` is one continuous take holding all six utterances of that passphrase.
- Subject folders are numeric (`01` … `42`) in the genuine archive and in sets 1, 4–7; sets 2 and 3 use short alphabetic subject codes instead.

## Recording format

| | |
| :-- | :-- |
| Container | NumPy `.npy` |
| Shape | `(n_samples, 16)` — channels on the last axis |
| dtype | `int16` |
| Sampling rate | 96 kHz |
| Typical length | 7–15 s per take (≈ 0.7–1.4 M samples) |

Channel mapping follows the dataset card (§3): Channel 7 is the air-conduction reference, Channels 15/16 are the bone-conduction nose-pad VPUs, the remaining channels provide the sound-field view.

```python
import numpy as np

x = np.load("AuthGlass/data_noattack/01/samp1/output.npy")   # (n_samples, 16), int16
fs = 96_000
ac  = x[:, 6]                     # Channel 7: AC reference
bc  = x[:, 14:16]                 # Channels 15–16: bone conduction
sf  = np.delete(x, 6, axis=1)     # the 15 remaining channels
```

## Segmentation annotations

`phoneme/samp<k>.csv` holds the verified MAUS alignment for the matching take, as `label,start,end,formant1,formant2,formant3` with times in seconds. Rows labelled `<p:>` are pauses; the six utterances are the intervals *between* consecutive pauses:

```python
import pandas as pd

seg = pd.read_csv("AuthGlass/data_noattack/01/phoneme/samp1.csv")
pauses = seg[seg.label == "<p:>"][["start", "end"]].to_numpy()
utterances = [(pauses[i, 1], pauses[i + 1, 0]) for i in range(len(pauses) - 1)]   # 6 (start, end) pairs
clips = [x[int(s * fs):int(e * fs)] for s, e in utterances]
```

## Terms

The dataset was collected under IRB approval with informed consent for publication of anonymized recordings. By using it you agree not to attempt re-identification of participants, and not to use the data to build systems that impersonate or target individuals. See [`../LICENSE`](../LICENSE) and cite the paper (BibTeX in the top-level [README](../README.md#-citation)).
