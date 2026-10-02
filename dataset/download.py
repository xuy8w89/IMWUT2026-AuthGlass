#!/usr/bin/env python3
"""Download the AuthGlass dataset from Hugging Face.

The dataset is hosted at https://huggingface.co/datasets/JZ0102/AuthGlass_Dataset
as eight tar archives (~23.5 GB each, ~188 GB total):

    data_noattack.tar               genuine wearer speech
    attack_1_artificial_throat.tar  Set 1: wearer-based replay (KEMAR torso-mouth simulator)
    attack_2_front_100.tar          Set 2: loudspeaker 100 cm in front
    attack_3_right_100.tar          Set 3: loudspeaker 100 cm to the right
    attack_4_back_100.tar           Set 4: loudspeaker 100 cm behind
    attack_5_left_100.tar           Set 5: loudspeaker 100 cm to the left
    attack_6_front_50.tar           Set 6: loudspeaker 50 cm in front
    attack_7_front_25.tar           Set 7: loudspeaker 25 cm in front

Examples:
    python download.py                          # everything, into ./AuthGlass
    python download.py --genuine --sets 1 2     # genuine + attack sets 1 and 2
    python download.py --sets 7 --out /data/ag  # only attack set 7
    python download.py --extract                # also untar after downloading

Requires: pip install -U huggingface_hub
"""
import argparse
import subprocess
import sys
from pathlib import Path

REPO_ID = "JZ0102/AuthGlass_Dataset"
GENUINE = "data_noattack.tar"
ATTACK_SETS = {
    1: "attack_1_artificial_throat.tar",
    2: "attack_2_front_100.tar",
    3: "attack_3_right_100.tar",
    4: "attack_4_back_100.tar",
    5: "attack_5_left_100.tar",
    6: "attack_6_front_50.tar",
    7: "attack_7_front_25.tar",
}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", default="AuthGlass", help="target directory (default: ./AuthGlass)")
    p.add_argument("--genuine", action="store_true", help="download the genuine (no-attack) archive")
    p.add_argument("--sets", type=int, nargs="*", choices=sorted(ATTACK_SETS), metavar="N",
                   help="attack sets to download (1-7); omit --genuine/--sets to download everything")
    p.add_argument("--extract", action="store_true", help="untar each archive after download")
    p.add_argument("--keep-archives", action="store_true", help="keep .tar files after extraction")
    args = p.parse_args()

    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        print("huggingface_hub is not installed. Run: pip install -U huggingface_hub", file=sys.stderr)
        return 1

    if not args.genuine and not args.sets:
        files = [GENUINE] + list(ATTACK_SETS.values())
    else:
        files = ([GENUINE] if args.genuine else []) + [ATTACK_SETS[i] for i in (args.sets or [])]

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for f in files:
        print(f"==> {f}")
        path = hf_hub_download(repo_id=REPO_ID, repo_type="dataset", filename=f,
                               local_dir=str(out), resume_download=True)
        if args.extract:
            print(f"    extracting into {out}/")
            subprocess.run(["tar", "-xf", path, "-C", str(out)], check=True)
            if not args.keep_archives:
                Path(path).unlink()
    print("done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
