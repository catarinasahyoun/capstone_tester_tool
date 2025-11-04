"""
Threshold engine (cumulative scoring)
- Robust to missing values
- Cumulative points out of 20 (configurable)
- Returns total_score, max_score, normalized_score and rationale
"""

from typing import Dict, List, Any, Tuple

# ----- Scoring scale (you can move this to configs/config.yaml later) -----
POINTS_PER_RULE = 2.0       # each rule can add up to 2 points
TOTAL_POINTS_TARGET = 20.0  # overall feel; not hard-capped (we also return max_score)

# ----- Rule bundles (same logic as before, trimmed to the essentials) -----
BUNDLES: Dict[str, Dict[str, Any]] = {
    "moisture_low": {
        "criteria": lambda s: s.get("moisture", 0) > 0 and s["moisture"] < 65,
        "rules": [
            {"prop": "fixed_carbon",    "type": "range", "min": 60, "max": 85, "w": 2, "msg": "FC 60–85%"},
            {"prop": "volatile_matter", "type": "max",   "max": 20,              "w": 2, "msg": "VM < 20%"},
            {"prop": "ash",             "type": "max",   "max": 20,              "w": 1, "msg": "Ash < 20%"},
            {"prop": "pH",              "type": "range", "min": 7.0, "max": 9.5, "w": 1, "msg": "Biochar pH 7–9.5"},
        ],
    },
    "moisture_high": {
        "criteria": lambda s: s.get("moisture", 0) >= 65,
        "rules": [
            {"prop": "fixed_carbon",    "type": "max", "max": 50,               "w": 1, "msg": "FC < 50%"},
            {"prop": "volatile_matter", "type": "min", "min": 30,               "w": 1, "msg": "VM > 30%"},
            {"prop": "ash",             "type": "min", "min": 40,               "w": 2, "msg": "Ash > 40%"},
            {"prop": "pH",              "type": "min", "min": 10,               "w": 2, "msg": "Biochar pH > 10"},
        ],
    },
    "acidic_soil": {
        "criteria": lambda s: s.get("pH", 7) < 6.0,
        "rules": [
            {"prop": "ash",         "type": "min",   "min": 25,              "w": 2, "msg": "Ash > 25% (liming)"},
            {"prop": "c_pct",       "type": "min",   "min": 50,              "w": 1, "msg": "C% > 50%"},
            {"prop": "h_pct",       "type": "max",   "max": 2.4,             "w": 1, "msg": "H% < 2.4%"},
            {"prop": "bet",         "type": "min",   "min": 200,             "w": 2, "msg": "BET > 200 m²/g"},
            {"prop": "pore_volume", "type": "min",   "min": 1.0,             "w": 1, "msg": "PV > 1.0 cm³/g"},
            {"prop": "pH",          "type": "min",   "min": 7.0,             "w": 2, "msg": "Biochar pH > 7"},
        ],
    },
    "basic_soil": {
        "criteria": lambda s: s.get("pH", 7) > 7.0,
        "rules": [
            {"prop": "ash",         "type": "max", "max": 10,               "w": 2, "msg": "Ash < 10%"},
            {"prop": "c_pct",       "type": "min", "min": 50,               "w": 1, "msg": "C% > 50%"},
            {"prop": "h_pct",       "type": "min", "min": 6,                "w": 1, "msg": "H% > 6%"},
            {"prop": "bet",         "type": "min", "min": 200,              "w": 2, "msg": "BET > 200 m²/g"},
            {"prop": "pore_volume", "type": "min", "min": 1.0,              "w": 1, "msg": "PV > 1.0 cm³/g"},
            {"prop": "pH",          "type": "max", "max": 6,                "w": 2, "msg": "Biochar pH < 6"},
        ],
    },
    "soc_too_high": {  # hard blocker
        "criteria": lambda s: s.get("SOC", 0) > 5,
        "rules": [
            {"prop": "fixed_carbon", "type": "max", "max": 1000, "w": 999, "critical": True, "msg": "SOC > 5% → do not apply"},
        ],
    },
    "soc_low": {
        "criteria": lambda s: s.get("SOC", 100) < 2.6,
        "rules": [
            {"prop": "volatile_matter", "type": "max",   "max": 15,             "w": 2, "msg": "VM < 15% (stability)"},
            {"prop": "ash",             "type": "range", "min": 20, "max": 30,  "w": 1, "msg": "Ash 20–30%"},
            {"prop": "c_pct",           "type": "min",   "min": 60,             "w": 2, "msg": "C% > 60%"},
            {"prop": "h_pct",           "type": "max",   "max": 6,              "w": 1, "msg": "H% ≤ 6%"},
            {"prop": "o_pct",           "type": "range", "min": 10, "max": 30,  "w": 1, "msg": "O% 10–30%"},
            {"prop": "o_c_ratio",       "type": "max",   "max": 0.4,            "w": 2, "msg": "O/C < 0.4"},
            {"prop": "pH",              "type": "max",   "max": 10,             "w": 1, "msg": "Biochar pH < 10"},
        ],
    },
    "saline_warning": {
        "criteria": lambda s: s.get("EC", 0) >= 4,
        "rules": [
            {"prop": "ash", "type": "max", "max": 20, "w": 2, "msg": "Ash < 20% (salinity)"},
            {"prop": "pH",  "type": "max", "max": 9.5,"w": 2, "msg": "Biochar pH < 9.5 (salinity)"},
        ],
    },
    "warm_climate": {
        "criteria": lambda s: s.get("temp", 0) >= 25,
        "rules": [
            {"prop": "ash",     "type": "min", "min": 3.07, "w": 1, "msg": "Ash > 3.07%"},
            {"prop": "moisture","type": "min", "min": 0.78, "w": 1, "msg": "Char moisture > 0.78%"},
            {"prop": "c_pct",   "type": "min", "min": 60,   "w": 1, "msg": "C% > 60%"},
            {"prop": "bet",     "type": "max", "max": 265,  "w": 1, "msg": "BET < 265 m²/g"},
        ],
    },
}

# ----- helpers --------------------------------------------------------------

def _score_min(v: float, m: float) -> float:
    if v is None: return 0.5
    return 1.0 if v >= m else max(0.0, v / m)

def _score_max(v: float, M: float) -> float:
    if v is None: return 0.5
    return 1.0 if v <= M else max(0.0, 1 - (v - M) / max(M, 1e-9))

def _score_range(v: float, a: float, b: float) -> float:
    if v is None: return 0.5
    if a <= v <= b: return 1.0
    d = min(abs(v - a), abs(v - b))
    tol = max(0.1 * (b - a), 1e-6)
    return max(0.0, 1 - d / tol)

def _score_rule(value: Any, rule: Dict[str, Any]) -> float:
    t = rule["type"]
    if t == "min":   return _score_min(value, rule["min"])
    if t == "max":   return _score_max(value, rule["max"])
    if t == "range": return _score_range(value, rule["min"], rule["max"])
    return 0.0

def _select_bundles(soil: Dict[str, Any]) -> List[str]:
    return [k for k, b in BUNDLES.items() if b["criteria"](soil)]

def evaluate_one(bio: Dict[str, Any], soil: Dict[str, Any]) -> Dict[str, Any]:
    active = _select_bundles(soil)
    total_pts, max_pts = 0.0, 0.0
    rationale: List[str] = []
    hard_fail = False

    for key in active:
        for r in BUNDLES[key]["rules"]:
            w = float(r.get("w", 1.0))
            max_pts += w * POINTS_PER_RULE

            val = bio.get(r["prop"])
            s01 = _score_rule(val, r)            # 0..1
            pts = s01 * w * POINTS_PER_RULE      # 0..(w*2)

            if r.get("critical") and s01 < 0.8:
                hard_fail = True
                rationale.append(f"⚠ {r['msg']} (critical) → 0 pts")
            else:
                shown = "None" if val is None else f"{val}"
                rationale.append(f"{r['msg']}: {r['prop']}={shown} → +{pts:.2f} pts")
                total_pts += pts

    if hard_fail:
        return {
            "biochar_id": bio.get("id"),
            "name": bio.get("name"),
            "total_score": 0.0,
            "max_score": max_pts,
            "normalized_score": 0.0,
            "active": active,
            "messages": rationale,
        }

    norm = (total_pts / max_pts) if max_pts > 0 else 0.0
    return {
        "biochar_id": bio.get("id"),
        "name": bio.get("name"),
        "total_score": round(total_pts, 2),
        "max_score": round(max_pts, 2),
        "normalized_score": round(norm, 3),
        "active": active,
        "messages": rationale,
    }

def evaluate_soil_against_biochars(soil: Dict[str, Any], biochars: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results = [evaluate_one(b, soil) for b in biochars]
    return sorted(results, key=lambda x: (x["total_score"], x["normalized_score"]), reverse=True)
