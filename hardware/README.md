# Hardware — Coming Soon

Frame models and a parts-sourcing guide for the DIY smart-glasses sensing prototype used to collect AuthGlass, so that the platform can be rebuilt from commercially available components.

<p align="center">
  <img src="../docs/assets/prototype.jpg" alt="Prototype: 14 AC microphones + 2 BC VPUs on an eyeglass frame" width="90%">
</p>

## Specification

| | |
| :-- | :-- |
| Frame dimensions | 167.0 mm (length) × 145.3 mm (width) |
| Air-conduction microphones | 14 × Infineon IM73D122V01 (omnidirectional) |
| Bone-conduction VPUs | 2 × Sonion VPU14AA01 |
| Channels | 16, synchronized |
| Sampling rate | 96 kHz |
| Interconnect | Bundled flexible flat cables (FFC) to the acquisition board |
| Streaming | TCP to host PC |

### Microphone placement

- **5 per temple** — spatial spread along the arms; the behind-the-ear positions turn out to be the most informative for sound-field features, being furthest from the mouth.
- **1 above each lens.**
- **2 at the centre** — one facing downward (Channel 7, the AC reference for all SF features), one facing forward.
- **1 BC VPU per nose pad** — symmetric placement mitigates the degradation caused by asymmetric skin contact. Temple-interior placement was tried first and rejected: weak signals plus spike noise from poor contact and hair friction.

The FFC bundle running through the temple is deliberate — it reduces crosstalk between channels.

## What lands here

- `cad/` — frame models (STEP + source) for the eyeglass frame, including the microphone and nose-pad mounting positions
- `SOURCING.md` — bill of materials with manufacturer part numbers and where to obtain each component: the air-conduction microphones, the bone-conduction VPUs, the multi-channel acquisition board, and the flexible flat cables
- `ASSEMBLY.md` — assembly and calibration guide for putting the frame together with the sourced parts

**Scope note.** This directory covers the frame models and component sourcing. Custom board designs are not part of the release; the prototype is reproducible from the frame models plus commercially available parts listed in `SOURCING.md`.

⭐ Watch this repository to be notified when the files land.
