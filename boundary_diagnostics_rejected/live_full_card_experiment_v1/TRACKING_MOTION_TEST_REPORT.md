# Detector-Assisted Tracking Motion Test

The test uses synthetic verified full-card candidates and detector/flow sequences
to exercise the tracker state machine. It does not replace physical-camera
validation.

| Scenario | Result | Reacquisition |
|---|---|---:|
| Stationary card | Verified and stable | N/A |
| Slow horizontal movement | Tracking verified | N/A |
| Slow vertical movement | Tracking verified | N/A |
| Sudden horizontal movement | Old lock discarded; new lock verified | 5 frames |
| Sudden vertical movement | Old lock discarded; new lock verified | 5 frames |
| Sudden diagonal movement | Old lock discarded; new lock verified | 5 frames |
| Rotation while moving | Tracking verified | N/A |
| Leave and return elsewhere | Lost, then new lock verified | 5 frames |
| Partial/outside frame | Lost, then new lock verified | 5 frames |
| Obstruction | Lost, then new lock verified | 5 frames |
| Face/unrelated-object replacement | Lost, then new lock verified | 5 frames |
| Brief disappearance | Lost, then new lock verified | 5 frames |
| Several-second absence | Lost, then new lock verified | 5 frames |

During sudden movement and disappearance, no stale `tracked_points` are emitted.
The five-frame reacquisition duration is the existing consecutive-detection
requirement, not a grace period for the old boundary.

Across all scenarios, stale-boundary frames were **0** and false locks were
**0**. Loss was declared on the first frame with no valid full-card candidate;
reacquisition required five consecutive fresh candidates.
