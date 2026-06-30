"""
Family Office Control Stack Core Module
Stateless strategic orchestration engine for ultra-high-net-worth principal management.
"""

import sys
from pydantic import BaseModel, Field

# =====================================================================
# 1. NESTED RULE STRUCTS
# =====================================================================
class AssetNode(BaseModel):
    entity_type: str
    allocation_pct: float = Field(..., ge=0.0, le=100.0)
    jurisdiction: str

class ControlStructure(BaseModel):
    structure_id: str
    tier_depth: int = Field(..., gt=0)
    nodes: list[AssetNode]
    max_exposure_limit: float

# =====================================================================
# 2. COMPLIANCE TREE EVALUATOR
# =====================================================================
class ComplianceEvaluator:
    """Immutable rule matrix evaluating structural allocations."""
    
    @staticmethod
    def verify_guardrails(structure: ControlStructure) -> dict:
        violations = []
        total_allocation = sum(node.allocation_pct for node in structure.nodes)
        
        if total_allocation > 100.0:
            violations.append("TOTAL_ALLOCATION_EXCEEDS_100_PCT")
            
        for node in structure.nodes:
            if node.allocation_pct > structure.max_exposure_limit:
                violations.append(f"EXPOSURE_VIOLATION_{node.jurisdiction}")
                
        return {
            "structure_id": structure.structure_id,
            "is_compliant": len(violations) == 0,
            "detected_violations": violations
        }

# =====================================================================
# 3. SELF-CONTAINED UNIT TEST SUITE
# =====================================================================
def run_test_suite():
    print("[INIT] Running Family Office Control Stack Compliance Engine...")
    
    # Model a synthetic multi-tiered Delaware / Cayman corporate shell structure
    synthetic_tree = ControlStructure(
        structure_id="STR-LLC-DE-01",
        tier_depth=2,
        max_exposure_limit=75.0,
        nodes=[
            AssetNode(entity_type="Delaware_LLC", allocation_pct=60.0, jurisdiction="US-DE"),
            AssetNode(entity_type="Foreign_Exempt_Trust", allocation_pct=40.0, jurisdiction="KY-KYM")
        ]
    )
    
    report = ComplianceEvaluator.verify_guardrails(synthetic_tree)
    
    # Assert logical determinism
    assert report["is_compliant"] is True
    assert len(report["detected_violations"]) == 0
    
    print("[SUCCESS] Operational guardrail logic confirmed stable.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_test_suite()
    else:
        print("Family Office Control Stack Active. Run with '--test' to verify rules.")

