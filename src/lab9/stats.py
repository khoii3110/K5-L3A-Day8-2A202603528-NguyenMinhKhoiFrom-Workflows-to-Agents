"""Statistics students implement (M2 judge calibration, M4 paired bootstrap).

Rules: a judge is a classifier -- measure it like one. A higher mean is not
"better" until the paired CI of the difference excludes 0.
Reference values to self-check are in tests/test_lab9_stats.py.
"""

from __future__ import annotations

from collections.abc import Sequence
import math

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """tp/fp/fn/tn with FAIL as positive."""
    h, j = _paired_labels(human, judge)
    return {
        "tp": sum(a == POS and b == POS for a, b in zip(h, j)),
        "fp": sum(a != POS and b == POS for a, b in zip(h, j)),
        "fn": sum(a == POS and b != POS for a, b in zip(h, j)),
        "tn": sum(a != POS and b != POS for a, b in zip(h, j)),
    }


def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    counts = confusion(human, judge)
    precision_denominator = counts["tp"] + counts["fp"]
    recall_denominator = counts["tp"] + counts["fn"]
    precision = counts["tp"] / precision_denominator if precision_denominator else 0.0
    recall = counts["tp"] / recall_denominator if recall_denominator else 0.0
    return precision, recall


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """kappa = (p_o - p_e) / (1 - p_e). Raise ValueError when undefined (p_e == 1):
    a constant judge has no signal and must FAIL calibration, not pass on a technicality."""
    h, j = _paired_labels(human, judge)
    n = len(h)
    observed = sum(a == b for a, b in zip(h, j)) / n
    human_fail = sum(label == POS for label in h) / n
    judge_fail = sum(label == POS for label in j) / n
    expected = human_fail * judge_fail + (1 - human_fail) * (1 - judge_fail)
    if expected == 1:
        raise ValueError("Cohen's kappa is undefined when expected agreement is 1")
    return (observed - expected) / (1 - expected)


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    """Correct an observed failure rate for judge error; clip to [0, 1]."""
    values = (observed_rate, sensitivity, specificity)
    if any(not math.isfinite(value) or not 0 <= value <= 1 for value in values):
        raise ValueError("observed rate, sensitivity, and specificity must be between 0 and 1")
    denominator = sensitivity + specificity - 1
    if denominator == 0:
        raise ValueError("true rate is undefined when sensitivity + specificity equals 1")
    corrected = (observed_rate + specificity - 1) / denominator
    return min(1.0, max(0.0, corrected))


def paired_bootstrap(a: Sequence[float], b: Sequence[float], *, n_resamples: int = 1000,
                     rng: int = 2027, confidence: float = 0.95) -> tuple[float, float, float]:
    """a[i], b[i] = per-item mean over seeds, SAME items, SAME order.
    Return (mean(a)-mean(b), lo, hi) with scipy.stats.bootstrap(paired=True, method="percentile",
    rng=numpy.random.default_rng(rng)). If a == b everywhere return (0.0, 0.0, 0.0)."""
    import numpy as np
    from scipy.stats import bootstrap

    left = np.asarray(a, dtype=float)
    right = np.asarray(b, dtype=float)
    if left.ndim != 1 or right.ndim != 1 or left.size == 0 or left.size != right.size:
        raise ValueError("paired samples must be non-empty one-dimensional sequences of equal length")
    if not np.isfinite(left).all() or not np.isfinite(right).all():
        raise ValueError("paired samples must contain only finite values")
    if n_resamples < 1:
        raise ValueError("n_resamples must be positive")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    differences = left - right
    observed = float(np.mean(differences))
    if np.all(differences == 0):
        return 0.0, 0.0, 0.0
    result = bootstrap(
        (left, right),
        statistic=lambda x, y: np.mean(x - y),
        n_resamples=n_resamples,
        confidence_level=confidence,
        method="percentile",
        paired=True,
        vectorized=False,
        rng=np.random.default_rng(rng),
    )
    return observed, float(result.confidence_interval.low), float(result.confidence_interval.high)


def _paired_labels(human: Sequence[str], judge: Sequence[str]) -> tuple[list[str], list[str]]:
    if len(human) != len(judge) or not human:
        raise ValueError("human and judge labels must be non-empty sequences of equal length")
    h = [str(label).strip().upper() for label in human]
    j = [str(label).strip().upper() for label in judge]
    if any(label not in ("PASS", "FAIL") for label in (*h, *j)):
        raise ValueError("labels must be PASS or FAIL")
    return h, j


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    # TODO M6
    raise NotImplementedError


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    # TODO M6
    raise NotImplementedError
