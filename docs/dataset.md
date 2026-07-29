# AuthGlass Dataset Card

> 🚧 **The dataset is not yet downloadable.** This page documents what will be released, so that reviewers and prospective users can plan ahead. Numbers and definitions follow the IMWUT 2026 paper.

## 1. Motivation

Voice is the dominant input modality on modern smart glasses because it is hands-free, needs no extra hardware, and can authenticate a user *implicitly* during normal interaction. It is also the modality most exposed to ambient audio, and therefore to replay, injection, and impersonation attacks.

Prior voice liveness/authentication datasets target smartphones or earbuds. Smart glasses are different: microphones sit along a **curved, non-uniform frame** wrapped around the head, and the frame is in continuous skin contact. That geometry produces acoustic cues — speech-induced vibration and head-coupled spatial sound-field patterns — that existing single-channel or planar-array methods do not model. AuthGlass exists to make those cues measurable.

## 2. Sensing Platform

A custom DIY smart-glasses prototype (167.0 mm × 145.3 mm):

| Sensor | Model | Count | Placement |
| :-- | :-- | :-: | :-- |
| Air-conduction microphone (AC) | Infineon IM73D122V01 | 14 | 5 per temple, 1 above each lens, 2 at centre (downward- and forward-facing) |
| Bone-conduction VPU (BC) | Sonion VPU14AA01 | 2 | 1 embedded in each nose pad |

All 16 channels are acquired synchronously at **96 kHz** through a common acquisition board (bundled flexible flat cables reduce inter-channel crosstalk) and streamed to a PC over TCP.

Nose-pad placement for the BC sensors was chosen after a pilot study: sensors on the inner side of the temple produced markedly weaker signals with spike noise, attributable to poor skin contact and hair friction.

## 3. Modality → Channel Mapping

| Modality | Channel(s) | Role |
| :-- | :-- | :-- |
| **AC** | Channel 7 | Centrally mounted, downward-facing; the reference channel for all SF features |
| **BC** | Channel 15 or 16 (higher-energy of the two) | Speech-induced vibration through the nose pad |
| **SF** | Channels 1–6, 8–14 | Complementary AC channels, always compared *against* Channel 7 |

## 4. Data Composition

| Category | Name | Description | Subjects | Utterances / subject |
| :-- | :-- | :-- | :-: | :-- |
| Genuine user data | Positive | Live speech from the wearer | 42 | 15 (× 6 repeats) |
| Wearer-based attack | Set 1 | Replay via GRAS 45BC KEMAR torso–mouth simulator wearing the glasses | 42 | 15 (× 6 repeats) |
| Environment-based attack | Set 2 | Loudspeaker 100 cm in front | 42 | 15 (× 6 repeats) |
| Environment-based attack | Set 3 | Loudspeaker 100 cm to the right | 42 | 15 (× 6 repeats) |
| Environment-based attack | Set 4 | Loudspeaker 100 cm behind | 42 | 15 (× 6 repeats) |
| Environment-based attack | Set 5 | Loudspeaker 100 cm to the left | 42 | 15 (× 6 repeats) |
| Environment-based attack | Set 6 | Loudspeaker 50 cm in front | 42 | 15 (× 6 repeats) |
| Environment-based attack | Set 7 | Loudspeaker 25 cm in front | 42 | 15 (× 6 repeats) |

**Totals:** 3,780 genuine utterances · 3,780 wearer-based attack samples · 22,680 environment-based attack samples.

Environment-based attacks use a PreSonus Eris E5 loudspeaker at mannequin head height, with playback volume manually calibrated against the sound pressure levels observed during genuine collection. The mannequin (the same torso–mouth simulator) stands in for a stationary user.

## 5. Passphrase Set

Fifteen everyday voice commands, each ≤ 5 words, selected to collectively cover most English vowels and consonants so that results are not biased by the phonetics of any single phrase:

| | | |
| :-- | :-- | :-- |
| (1) Hi siri | (2) Hi google | (3) Hi alexa |
| (4) Pay the bill | (5) Call tom | (6) Turn on bluetooth |
| (7) Take a photo | (8) Play some music | (9) Show me my first message |
| (10) Send an email to john | (11) Check my voicemail | (12) What's my appointment |
| (13) Set an alarm | (14) Thank you | (15) A hundred dollars |

Each phrase is spoken at **three volume levels** — from soft (as if to a nearby listener) to loud (as if projecting ~5 m) — with **two repeats** per level.

## 6. Participants

42 participants recruited from a university campus.

| Attribute | Distribution |
| :-- | :-- |
| Age | 18–42, mean 24.6 ± 4.3 |
| Gender | 28 male (66.7 %), 14 female (33.3 %) |
| Affiliation | 41 students, 1 staff; Engineering & CS (33), Arts (3), interdisciplinary Colleges (3), Medicine (1), Research Institute (1) |
| Linguistic background | Chinese-accented English (37), South Asian (2), Arabic-accented (2), American English (1) |

Participants sat in a natural posture in a quiet conference room, wore the prototype, and were asked to speak at a conversational pace with clear but unexaggerated articulation. Short rests were given between passphrases to limit vocal fatigue.

## 7. Processing and Annotations

- Every recording was manually reviewed for capture success.
- Utterances were segmented with [MAUS](https://clarin.phonetik.uni-muenchen.de/BASWebServices/) forced alignment, then temporally aligned across attack settings, then **manually verified**.
- Each sample carries a **subject ID** (1–42) and an **utterance ID** (1–15).

## 8. Derived Features

Reference implementations will ship in `src/features/`.

### AC and BC — log-Mel spectrograms

BC signals are first high-pass filtered (Butterworth, 100 Hz cutoff) to suppress motion artifacts and ambient rumble. All signals are resampled to 96 kHz by linear interpolation for consistent temporal resolution.

| Parameter | Value |
| :-- | :-- |
| Sampling rate | 96,000 Hz |
| Max frequency | 8,000 Hz |
| `n_fft` | 2048 |
| Hop length | 1024 |
| `n_mels` | 128 |

### Sound field — ERT, TDT, EDF

**Energy Ratio over Time (ERT).** STFT per voiced segment; spectral energy summed over 100–8,000 Hz per AC channel; normalized against Channel 7; linearly scaled then squashed with `tanh` for a bounded, numerically stable range.

**Time Delay over Time (TDT).** Cross-correlation against Channel 7; the lag at the maximum correlation peak is the delay estimate. A confidence score — the peak correlation normalized by signal energies, passed through a logit-like transform — weights the estimate, suppressing unreliable lags from noise or silence. Scaled and `tanh`-normalized as with ERT.

**Energy Distribution over Frequency (EDF).** STFT per voiced segment, averaged along time to a frequency-wise energy profile per channel, normalized by the maximum STFT energy of Channel 7. This preserves relative spectral shape while removing overall amplitude variation.

| Feature | Sample rate | Range | Other |
| :-- | :-- | :-- | :-- |
| ERT / TDT | 96,000 Hz | 100–8,000 Hz | step 0.005 s, scaling factor 2000 |
| EDF | 96,000 Hz | ≤ 8,000 Hz | `n_fft` 1024, hop 1024 |

## 9. Planned Release Layout

```
dataset/
├── genuine/
│   └── S{01..42}/U{01..15}/V{1..3}_R{1,2}.wav      # 16-channel, 96 kHz
├── attack_set1/                                     # wearer-based (KEMAR simulator)
│   └── S{01..42}/U{01..15}/V{1..3}_R{1,2}.wav
├── attack_set2..7/                                  # environment-based (loudspeaker)
│   └── S{01..42}/U{01..15}/V{1..3}_R{1,2}.wav
├── annotations/
│   ├── segmentation/                                # MAUS alignments (verified)
│   └── metadata.csv                                 # subject/utterance IDs, volume level, demographics
└── splits/                                          # subject-independent 7-fold splits per task
```

*The exact layout may change slightly before release; this section will be updated to match the shipped archive.*

## 10. Known Limitations

- **Population bias.** Participants come from a single university campus, skewing young, technically trained, and toward Chinese-accented English. Generalization to broader demographics, accents, and speaking styles is untested.
- **Controlled acoustics.** Recording took place in a quiet conference room (attacks in a sound-isolation room). No environmental noise was injected during collection, and robustness under noise is neither evaluated nor optimized. Multi-channel noise augmentation (e.g. DEMAND) is a natural extension.
- **Attack coverage.** The seven settings are representative, not exhaustive. Adaptive replay, multi-source injection, and high-fidelity voice synthesis are not covered.
- **Wearing conditions.** Variation in how the glasses are worn may perturb on-body acoustic cues; this is not systematically varied in the dataset.

We release the hardware design alongside the data precisely so that these gaps can be filled by the community.

## 11. Ethics

The study protocol was approved by an Institutional Review Board. All participants gave informed consent covering the use and publication of their anonymized data for research. All released data are anonymized. Users of the dataset must not attempt to re-identify participants and must not use the data to build systems that impersonate or target individuals.
