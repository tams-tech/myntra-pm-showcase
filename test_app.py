"""
test_app.py
Automated verification tests for Myntra StyleGen & FitSense showcase.
Verifies data integrity, intent parsing, search ranking, FitSense calibration, and analytics formulas.
"""

import os
import sys
import json

# Ensure utf-8 encoding on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from app.modules.search_engine import StyleGenSearchEngine
from app.modules.fitsense import FitSenseEngine
from app.modules.metrics_dashboard import (
    calculate_two_proportion_z_test,
    create_funnel_chart,
    create_return_reasons_chart,
    create_roi_waterfall
)


def run_all_tests():
    print("=== Starting Automated Verification Suite ===\n")
    
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    catalog_path = os.path.join(curr_dir, "app", "data", "catalog.json")
    sim_path = os.path.join(curr_dir, "app", "data", "analytics_sim.json")
    
    # 1. Test Dataset Loading
    assert os.path.exists(catalog_path), f"Missing catalog file at {catalog_path}"
    assert os.path.exists(sim_path), f"Missing simulation file at {sim_path}"
    
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    assert len(catalog) >= 15, f"Catalog items count too low: {len(catalog)}"
    print(f"[PASS] Step 1: Catalog Loaded Successfully ({len(catalog)} items).")
    
    with open(sim_path, "r", encoding="utf-8") as f:
        sim_data = json.load(f)
    assert "ab_test_results" in sim_data, "Missing A/B test results in sim data"
    print("[PASS] Step 2: Simulation Data Loaded Successfully.")
    
    # 2. Test Search & Intent Extraction
    engine = StyleGenSearchEngine(catalog)
    intent = engine.extract_intent("beach wedding guest floral dress under 4000")
    assert intent["budget"] == 4000, f"Expected budget 4000, got {intent['budget']}"
    assert intent["occasion"] == "Festive/Wedding", f"Expected occasion Festive/Wedding, got {intent['occasion']}"
    print(f"[PASS] Step 3: Intent Extraction Verified: {intent}")
    
    results = engine.search("olive casual shirt under 2000", top_k=5)
    assert len(results) > 0, "Search returned 0 results for valid query"
    top_item, score = results[0]
    print(f"[PASS] Step 4: Search Execution Verified (Top item: {top_item['title']} - Score: {score:.3f})")
    
    # 3. Test Outfit Bundling
    bundle = engine.build_outfit_bundle(top_item, max_bundle_budget=5000)
    assert bundle["total_items"] >= 2, f"Expected at least 2 items in bundle, got {bundle['total_items']}"
    assert bundle["bundle_price"] < bundle["original_total"], "Bundle discount not applied"
    print(f"[PASS] Step 5: Outfit Bundling Verified ({bundle['total_items']} items, Bundle Price: Rs. {bundle['bundle_price']}, Savings: Rs. {bundle['savings']})")
    
    # 4. Test FitSense Sizing Normalization
    fitsense = FitSenseEngine()
    # Test case: Zara (True to size) M -> Roadster (Runs small) should recommend size L!
    rec = fitsense.calculate_recommendation("Zara", "M", "Roadster", fit_preference="Regular")
    assert rec["recommended_size"] == "L", f"Expected Roadster recommended size L, got {rec['recommended_size']}"
    assert rec["confidence_pct"] >= 90.0, f"Expected confidence >= 90%, got {rec['confidence_pct']}"
    print(f"[PASS] Step 6: FitSense Cross-Brand Calibration Verified (Zara M -> Roadster {rec['recommended_size']}, Confidence: {rec['confidence_pct']}%)")
    
    # Test case: Zara M -> Anouk (Runs large) should recommend size S!
    rec_anouk = fitsense.calculate_recommendation("Zara", "M", "Anouk", fit_preference="Regular")
    assert rec_anouk["recommended_size"] == "S", f"Expected Anouk recommended size S, got {rec_anouk['recommended_size']}"
    print(f"[PASS] Step 7: FitSense Down-Sizing Calibration Verified (Zara M -> Anouk {rec_anouk['recommended_size']})")
    
    # 5. Test Analytics & Experimentation Calculations
    ctrl = sim_data["ab_test_results"]["Control"]
    v_c = sim_data["ab_test_results"]["Variant_C"]
    z_res = calculate_two_proportion_z_test(ctrl["orders"], ctrl["sessions"], v_c["orders"], v_c["sessions"])
    assert z_res["significant"] is True, "Expected conversion lift to be statistically significant"
    print(f"[PASS] Step 8: Two-Proportion Z-Test Verified (Lift: +{z_res['lift_pct']}%, Z-Score: {z_res['z_score']}, p-value: {z_res['p_value']})")
    
    roi = create_roi_waterfall(orders_per_month=4000000, current_return_rate=32.0, reduction_points=3.5, cost_per_return=210)
    assert roi["annual_savings_cr"] > 0, "ROI calculation error"
    print(f"[PASS] Step 9: Financial ROI Calculation Verified (Projected Annual Savings: Rs. {roi['annual_savings_cr']} Crores)")
    
    # 6. Test Plotly Chart Generators
    f_chart = create_funnel_chart(sim_data["ab_test_results"])
    assert f_chart is not None, "Funnel chart creation failed"
    
    r_chart = create_return_reasons_chart(sim_data["return_reasons_breakdown"])
    assert r_chart is not None, "Return reasons chart creation failed"
    print("[PASS] Step 10: Plotly Visualization Generators Verified.")
    
    print("\n[DONE] ALL 10 VERIFICATION TESTS PASSED SUCCESSFULLY! The PM Showcase is 100% Operational.")


if __name__ == "__main__":
    run_all_tests()
