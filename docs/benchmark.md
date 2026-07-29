# Benchmark Protocols

> 🚧 Placeholder documentation ahead of the artifact release. The runnable harness will live in `src/benchmark/`; this page fixes the protocols so results stay comparable.

Four tasks: two for liveness detection, two for authentication. Every task uses a **subject-independent** split — no subject appears in both training and test — with **7-fold cross-validation**.

---

## Task 1 — Liveness Detection Accuracy

**Question.** Can the system tell a live wearer from a replayed or injected signal, for each attack setting?

**Data split.** Seven evaluation sets, one per attack setting. Each pairs positive samples with attack samples of that setting, in equal number and one-to-one correspondence. Positives are labelled `0`, attacks `1`.

**Method.** Train on the training subjects of a given set, test on the held-out subjects of the same set. Report overall classification accuracy, averaged over folds.

**Metric.** Accuracy at the EER operating point (1 − EER).

> ⚠️ Because training and testing share an attack type here, methods that key on device-specific artifacts of the attacking loudspeaker can score near-perfectly without learning any liveness cue. Task 2 exists to expose that.

---

## Task 2 — Generalization to Unseen Attacks

**Question.** Does liveness detection survive an attack type it never saw in training?

**Data split.** The same seven datasets as Task 1, with the **same subject split applied consistently across all of them** so comparisons are fair.

**Method.** Train on one attack setting using the training subjects; evaluate on the test portions of the *remaining* settings using the test subjects. E.g. train on (Positive, Set 1), test on (Positive, Set 2) … (Positive, Set 7). Average accuracy over all train→test combinations, then over folds.

**Metric.** Accuracy at the EER operating point.

> AuthG-Live needs no attack samples at all — its threshold comes from the genuine distribution — so for our method the accuracy is averaged across all attacks directly.

---

## Task 3 — Authentication Accuracy

**Question.** Can the system tell enrolled users apart?

**Data split.** Subject-independent. **Positive samples only** — the task is discriminating among genuine users. Each sample carries a subject ID (1–42) and an utterance ID (1–15).

**Method.** Train on the training subjects with subject and utterance labels. At test time, randomly select **one sample per utterance** from each test subject as the enrollment set (15 enrollment samples per subject); this selection is **fixed across all compared methods**. The rest form the test set. Predict subject identity per test sample.

**Metric.** Classification accuracy, averaged over folds.

---

## Task 4 — Cross-Utterance Authentication

**Question.** Can a user enrolled on a few phrases be recognized on phrases they never enrolled with? This is what makes fast, low-effort enrollment practical.

**Data split.** Identical to Task 3.

**Method.** Partition the 15 utterances into non-overlapping groups. Each group in turn serves as the enrollment set while the remaining utterances form the test set. Group selection is fixed across methods. Average accuracy over all configurations, then over folds.

**Metric.** Classification accuracy.

---

## Baselines

All baselines are adapted to multi-channel input so the comparison is like-for-like. Original single-channel implementations are also reported in the paper's appendix for reference.

### Liveness detection

| Method | AC | BC | SF | Feature | Model | Multi-channel adaptation |
| :-- | :-: | :-: | :-: | :-- | :-- | :-- |
| VOID | ✓ | – | – | Handcrafted + LPCC | SVM (RBF) | Per-channel extraction, features concatenated |
| He et al. (2024) | ✓ | – | – | Handcrafted + LPCC | SE-ResNet | Per-channel extraction, stacked; input layer widened |
| Boneauth | ✓ | ✓ | – | MFCC | Cosine similarity | BC paired with each AC channel; majority voting |
| Eve Said Yes | ✓ | ✓ | – | Pooled STFT | Temporal similarity | Same voting strategy as Boneauth |
| Li et al. (2021) | ✓ | – | ✓ | STFT energy + phase | CNN | Natively multi-channel; input layer adjusted |
| Cafield | – | – | ✓ | Fieldprint | GMM | Fieldprint vs. Channel 7 per channel, concatenated |
| Voshield | – | – | ✓ | Sound field dynamics | Residual CNN | SFD vs. Channel 7 per channel, stacked |
| **AuthG-Live (ours)** | – | – | ✓ | TDT + ERT | Cosine similarity | Native |

### Authentication

| Method | AC | BC | SF | Feature | Model | Multi-channel adaptation |
| :-- | :-: | :-: | :-: | :-- | :-- | :-- |
| Park et al. (2025) | ✓ | – | – | MFCC | LSTM | Per-channel MFCC stacked; input layer adjusted |
| Eve Said Yes | – | ✓ | – | CQT | CNN + adversarial learning | Features stacked across channels |
| Cafield | – | – | ✓ | Fieldprint | GMM | As in liveness setting |
| Voshield | – | – | ✓ | Sound field dynamics | CNN | Binary head replaced with FC + softmax; embeddings taken after the residual block |
| **AuthG-Net (ours)** | ✓ | ✓ | ✓ | log-Mel + TDT/ERT/EDF | CNN + domain-adversarial learning | Native |

---

## Ablations Reported in the Paper

Each follows Task 1 (liveness) and/or Task 3 (authentication), with 7-fold cross-validation repeated twice:

| Ablation | Settings |
| :-- | :-- |
| **Sampling rate** | 96 / 48 / 32 / 16 kHz (FIR low-pass + uniform downsampling; linear interpolation to recover temporal resolution for SF features) |
| **Modality subsets** | AC only · AC+BC · AC+SF · AC+BC+SF |
| **Channel count and placement** | 4-channel (Rokid-like), 5-channel (Ray-Ban Meta-like), 7-channel; symmetric vs. asymmetric layouts; Channel 7 fixed as AC reference |
| **Commodity product layouts** | Rokid Glasses (channels 2, 5, 10, 13 @ 16 kHz, reference = 5) · Ray-Ban Meta (channels 2, 5, 10, 13, 7 @ 16 kHz, reference = 7) |
| **Live deployment** | Raspberry Pi streaming; Level 1 (TDT/ERT at 24 kHz) and Level 2 (odd-frame reconstruction); latency, power, memory, accuracy |

### Two findings worth carrying into new work

1. **Asymmetry beats symmetry at equal channel count.** Human sound fields are approximately symmetric, so symmetric microphone layouts collapse spatial information: for sources near the symmetry plane, both sides receive near-identical signals and aTDT/aERT degenerate. A 4-channel asymmetric layout can beat a 5-channel symmetric one.
2. **Behind-the-ear microphones are always selected.** Their distance from the mouth makes them the most sensitive to time-delay and energy-ratio variation. Any new layout should keep at least one.
