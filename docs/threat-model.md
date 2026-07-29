# Threat Model

> 🚧 Placeholder documentation ahead of the artifact release. Content follows the IMWUT 2026 paper.

<p align="center">
  <img src="assets/threat-model.png" alt="Voice authentication pipeline and threat model" width="100%">
</p>

## 1. Why voice on smart glasses

Compared with the alternatives available on head-worn devices, voice is the only modality that is simultaneously effort-free, hands-free, supported by commodity hardware, and cheap to run:

| Modality | Explicit task | Extra effort | Hands-free | Continuous auth. | Commodity HW | Energy |
| :-- | :-: | :-: | :-: | :-- | :-: | :-- |
| Touch (password) | ✓ | ✓ | ✗ | No | ✓ | Low |
| Touch (fingerprint) | ✓ | ✗ | ✗ | Event-driven | ✗ | Low |
| Gaze (password) | ✓ | ✓ | ✓ | No | ✗ | High |
| Gaze (implicit task) | ✗ | ✗ | ✓ | No | ✗ | High |
| Iris recognition | ✓ | ✓ | ✓ | No | ✗ | High |
| Facial biometrics | ✗ | ✗ | ✓ | Continuous | ✗ | High |
| Skull biometrics | ✗ | ✗ | ✓ | Continuous | ✗ | Medium |
| **Voice** | ✗ | ✗ | ✓ | Event-driven | ✓ | Low |

Voice authentication is *event-driven* rather than continuous — but that matches how people actually use smart glasses, which is command by command. Authentication rides along with interaction the user was going to perform anyway.

## 2. Authentication Pipeline

**Enrollment (once).** The user records a small set of voice samples. Acoustic embeddings are extracted and stored as user-specific templates.

**Operation (per command).**

1. A voice command arrives and implicitly triggers authentication.
2. **Liveness detection** verifies the signal came from a live speaker *wearing the device*, rejecting replayed or externally injected audio.
3. **Authentication** matches the extracted features against the enrolled template.
4. The command executes only if both stages pass.

**Fallback.** Environmental noise, intra-user variation, and device conditions all cause occasional false rejections. A fallback channel — for example a password on a paired trusted smartphone — preserves usability. It is less hands-free, but it is only reached in the rare failure case, and it also raises the bar for high-risk operations.

## 3. Adversarial Scenarios

The reference setting is a realistic smart-glasses deployment, e.g. an industrial worker whose hands are occupied.

### (1) Environmental injection attacks → *should fail liveness*

An attacker injects malicious voice commands into the environment via loudspeaker — TTS output, recordings of the user, or AI-generated voice — hoping to trigger unintended operations. Nothing about the signal originates from a live wearer.

### (2) Non-wearer voice attacks → *should fail liveness*

Commands are spoken near the device while the legitimate user is not wearing it (e.g. the glasses are on a table). The speech is real, but the on-body speaking condition is absent.

### (3) Advanced spoofing with the user's voice → *should fail liveness*

The attacker has recordings of the target and reproduces them through high-quality playback systems or humanoid simulators. The *content* is convincing; the coupled acoustics of human speech production and head anatomy are not reproducible.

### (4) Device theft and impersonation → *should fail authentication*

The attacker physically obtains the glasses and wears them — for example a co-worker reaching for unauthorized data. This produces genuinely live speech and may well pass liveness detection. The attacker's voice characteristics, however, differ from the enrolled user, so rejection is expected at the authentication stage.

## 4. Attacker Capabilities

We assume the attacker:

- **(a)** cannot compromise or manipulate the enrollment process or stored templates;
- **(b)** may gain physical access to the device, but cannot tamper with internal data streams or bypass the sensing pipeline;
- **(c)** can obtain recordings of the target user's voice, e.g. from public or environmental sources;
- **(d)** cannot faithfully reproduce the user's physiological acoustic signature — vocal tract dynamics, bone-conducted signals, and head-related sound-field patterns.

Assumption (d) is what the AuthGlass features are built to exploit, and attack setting 1 (KEMAR torso–mouth simulator) is the dataset's stress test of exactly that assumption.

## 5. Out of Scope

- **Post-authentication misuse.** A device authenticated and then left unattended is not covered. Because voice authentication is event-driven, identity is verified per command rather than continuously; closing this gap needs complementary mechanisms such as continuous authentication or wearing detection.
- **Exhaustive attack coverage.** Adaptive replay, multi-source injection, and high-fidelity voice synthesis are not represented in the current dataset.
- **Noisy in-the-wild conditions.** Data collection is controlled; robustness under environmental noise is not evaluated or optimized.

## 6. Dataset ↔ Threat Model Mapping

| Scenario | Instantiated by |
| :-- | :-- |
| (1) Environmental injection | Attack settings 2–7 (loudspeaker at 6 positions/distances) |
| (2) Non-wearer voice | Attack settings 2–7 (device not on a live head) |
| (3) Advanced spoofing | Attack setting 1 (KEMAR torso–mouth simulator wearing the glasses) |
| (4) Theft and impersonation | Genuine data from 42 subjects, each acting as an impostor against the others |
