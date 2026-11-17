"""M4 regression for the ticket-trust trace case."""

import time

from lab8.db import connect
from lab8.metrics import trial_pass
from lab9.variant_agent import make_shape
from tests.conftest import BY_ID


def test_fixed_shape_uses_database_delay(public_db, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    started_at = time.time()
    result = make_shape("fixed_trace_regression", {"no_override"})(
        "C-002", seed=11, store_path=str(public_db)
    )
    conn = connect(public_db)
    try:
        passed, reason = trial_pass(
            result.as_dict(),
            BY_ID["C-002"]["expected"],
            conn,
            started_at=started_at,
        )
    finally:
        conn.close()

    assert passed, reason
