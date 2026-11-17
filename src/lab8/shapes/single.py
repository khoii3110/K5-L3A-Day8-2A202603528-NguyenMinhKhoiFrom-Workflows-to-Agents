"""Shape B — one ReAct agent. Student work.

Use `lab8.runtime.run_react` with max_steps=8. `decide` may pick a read tool.
It must not call `issue_refund`. After the loop, the host validates the quote
and is the only writer.

A decide() that trusts ticket text over the order row will fail hidden claims
where the customer overstates the delay or cites a superseded clause.

Per-order cap: an order may already have been refunded by an earlier claim.
The read tool `lookup_refund_history` shows how much. The host still enforces
the cap, so pass the full quote to `durability.issue_refund`, not a net amount.

Caps: stop at 8 steps. Count model calls in the Budget so cost stays comparable.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.
"""

from __future__ import annotations

import sqlite3
from typing import Any

from lab8.db import connect
from lab8.durability import InjectedCrash, issue_refund
from lab8.runtime import run_react
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish, safe_dump
from lab8.tools import tool_cost
from lab8.trace import Trace


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    conn = connect(store_path)
    try:
        return _run(conn, claim_id, seed=seed, crash_at=crash_at)
    finally:
        conn.close()


def _run(
    conn: sqlite3.Connection,
    claim_id: str,
    *,
    seed: int,
    crash_at: str | None,
) -> RunResult:
    budget = Budget()
    trace = Trace(make_run_id("single", claim_id, seed))
    state: dict[str, Any] = {"phase": "claim"}
    observations: list[dict[str, Any]] = []

    def decide(observation: dict[str, Any]) -> dict[str, Any]:
        if "last_tool" in observation:
            observations.append(
                {
                    "tool": observation["last_tool"],
                    "result": observation["last_result"],
                }
            )
        if state["phase"] == "claim":
            state["phase"] = "order"
            return {"tool": "get_claim_view", "args": {"claim_id": claim_id}}
        if state["phase"] == "order":
            claim = observation["last_result"]
            if not claim["found"]:
                return {"final": {"status": "failed", "error_reason": "unknown_claim"}}
            if not claim.get("order_id"):
                return {"final": {"status": "needs_info", "error_reason": "missing_order_id"}}
            state["principal_id"] = claim["principal_id"]
            state["order_id"] = claim["order_id"]
            state["phase"] = "quote"
            return {
                "tool": "lookup_order",
                "args": {
                    "order_id": state["order_id"],
                    "principal_id": state["principal_id"],
                },
            }
        if state["phase"] == "quote":
            order_result = observation["last_result"]
            if not order_result["visible"]:
                return {
                    "final": {
                        "status": "escalated",
                        "error_reason": order_result["reason"],
                    }
                }
            state["phase"] = "decision"
            return {
                "tool": "compute_compensation",
                "args": {"order": order_result["order"]},
            }
        if state["phase"] == "decision":
            quote = observation["last_result"]
            return {
                "final": {
                    "status": "denied" if int(quote["amount_vnd"]) <= 0 else "quoted",
                    "proposal_amount": int(quote["amount_vnd"]),
                    "error_reason": quote.get("reason"),
                }
            }
        return {"final": {"status": "failed", "error_reason": "invalid_agent_state"}}

    try:
        run = run_react(
            conn,
            budget,
            observation={"claim": {"claim_id": claim_id}},
            decide=decide,
            max_steps=8,
        )
        for item in observations:
            result = item["result"]
            if item["tool"] == "get_claim_view":
                result = {
                    key: result[key]
                    for key in ("found", "claim_id", "order_id")
                    if key in result
                }
            elif item["tool"] == "lookup_order" and result.get("visible"):
                result = {"visible": True, "order": result["order"]}
            trace.add("tool_result", safe_dump({"tool": item["tool"], "result": result}))

        final = run["final"]
        proposal = int(final.get("proposal_amount", 0))
        if final["status"] in ("failed", "needs_info", "escalated"):
            return finish(
                conn,
                shape="single",
                claim_id=claim_id,
                seed=seed,
                status=final["status"],
                proposal_amount=0,
                budget=budget,
                trace=trace,
                error_reason=final.get("error_reason"),
            )
        if proposal <= 0:
            return finish(
                conn,
                shape="single",
                claim_id=claim_id,
                seed=seed,
                status="denied",
                proposal_amount=0,
                budget=budget,
                trace=trace,
                error_reason=final.get("error_reason"),
            )

        trace.add("quote", safe_dump({"amount_vnd": proposal, "reason": final.get("error_reason")}))
        try:
            outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
        except InjectedCrash:
            trace.add("crash", {"at": crash_at})
            trace.write()
            raise
        if not outcome["ok"]:
            return finish(
                conn,
                shape="single",
                claim_id=claim_id,
                seed=seed,
                status="failed" if outcome["conflict"] else "denied",
                proposal_amount=proposal,
                budget=budget,
                trace=trace,
                error_reason=outcome["reason"],
            )
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="resolved",
            proposal_amount=proposal,
            budget=budget,
            trace=trace,
        )
    except InjectedCrash:
        raise
