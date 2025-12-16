"""
Data helpers for the Sheet Metal Brazing Streamlit app.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import pdfplumber  # type: ignore
except Exception:  # pragma: no cover - optional dependency for offline parsing
    pdfplumber = None

import requests

# Document references (external + expected local copies)
DOC_LINKS: Dict[str, Dict[str, str]] = {
    "MIL-SD-248D": {
        "external": "https://u.dianyuan.com/bbs/u/39/1142217644.pdf",
        "local": "files/MIL-SD-248D.pdf",
    },
    "MIL-S-23284A": {
        "external": "https://www.dcma.mil/Portals/31/Documents/NPP/MIL-S-23284A.pdf",
        "local": "files/MIL-S-23284A.pdf",
    },
}


def _extract_pdf_tables(pdf_path: Path, min_rows: int = 2) -> Tuple[List[List[str]], List[str]]:
    """Extract basic tables and trailing footnotes from a PDF if possible."""

    if pdfplumber is None or not pdf_path.exists():
        return [], []

    tables: List[List[str]] = []
    footnotes: List[str] = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Collect tables with at least ``min_rows`` rows.
                for table in page.extract_tables():
                    if not table or len(table) < min_rows:
                        continue
                    # Flatten header gaps and strip whitespace.
                    cleaned = [[(cell or "").strip() for cell in row] for row in table]
                    tables.append([" | ".join(row) for row in cleaned])

                # Collect candidate footnotes at bottom of the page.
                text_lines = page.extract_text(layout=True, x_density=5, y_density=5) or ""
                for line in text_lines.splitlines():
                    if line.strip().startswith(("*", "Note", "NOTE")):
                        footnotes.append(line.strip())
    except Exception:
        # Gracefully degrade if the PDF is malformed or partially downloaded.
        return [], []

    # Remove duplicates while preserving order.
    seen = set()
    deduped_footnotes: List[str] = []
    for note in footnotes:
        if note not in seen:
            seen.add(note)
            deduped_footnotes.append(note)

    return tables, deduped_footnotes


def load_milstd248_tables() -> Dict[str, List[str]]:
    """Attempt to load MIL-STD-248D tables and footnotes from a local copy.

    Returns a dict with two lists: ``tables`` (rows formatted for rendering)
    and ``footnotes`` for downstream display.
    """

    pdf_path = Path(DOC_LINKS["MIL-SD-248D"]["local"])
    tables, footnotes = _extract_pdf_tables(pdf_path)
    return {"tables": tables, "footnotes": footnotes}

BASE_FILLER_MATERIALS: List[Dict[str, str]] = [
    {
        "Base Material": "Low-carbon steel sheet",
        "Filler Metals": "AWS A5.18 ER70S-6; AWS A5.20 E71T-1",
        "Process": "GMAW, FCAW, GTAW",
        "Guiding Spec": "MIL-SD-248D",
    },
    {
        "Base Material": "Austenitic stainless steel",
        "Filler Metals": "AWS A5.9 ER308L/ER309L; AWS A5.22 E308LT",
        "Process": "GTAW, GMAW-P, SMAW",
        "Guiding Spec": "MIL-SD-248D",
    },
    {
        "Base Material": "Aluminum alloys (5xxx/6xxx)",
        "Filler Metals": "AWS A5.10 ER4043; AWS A5.10 ER5356",
        "Process": "GMAW, GTAW",
        "Guiding Spec": "MIL-S-23284A",
    },
    {
        "Base Material": "Nickel-base alloys",
        "Filler Metals": "AWS A5.14 ERNiCr-3; BNi-2 brazing alloy",
        "Process": "GTAW, brazing",
        "Guiding Spec": "MIL-S-23284A",
    },
]

INSPECTION_CHECKLIST: List[Dict[str, str]] = [
    {
        "Category": "Joint preparation",
        "Characteristic": "Edges deburred, fit-up within specified root opening, backing/consumable inserts per WPS",
        "Why it matters": "Controls penetration and prevents inclusions or lack of fusion",
    },
    {
        "Category": "Cleanliness",
        "Characteristic": "No oil, oxide, paint, or mill scale; solvent wiped per process instructions",
        "Why it matters": "Prevents porosity and incomplete fusion, especially critical for GTAW/GMAW on aluminum",
    },
    {
        "Category": "Filler verification",
        "Characteristic": "Filler classification, diameter, heat/lot match WPS and MIL filler list",
        "Why it matters": "Ensures mechanical properties and corrosion resistance align with base metal",
    },
    {
        "Category": "Preheat/interpass",
        "Characteristic": "Measured with contact pyrometer or temp stick; documented within WPS limits",
        "Why it matters": "Prevents hydrogen cracking and controls distortion",
    },
    {
        "Category": "Shielding gas",
        "Characteristic": "Type, purity, flow rate per WPS; hoses purged; dew point controlled for aluminum",
        "Why it matters": "Protects molten pool from contamination and nitrogen/oxygen pickup",
    },
    {
        "Category": "Visual weld quality",
        "Characteristic": "Bead profile, reinforcement, undercut, arc strikes, overlap within acceptance per MIL-SD-248D",
        "Why it matters": "Visual cues often correlate with internal quality and dimensional control",
    },
    {
        "Category": "Dimensional/GD&T",
        "Characteristic": "Flatness, perpendicularity, hole position check against drawing feature control frames",
        "Why it matters": "Assures assembly interchangeability and fit for bonded/brazed structures",
    },
]

WELDING_LIMITATIONS: List[Dict[str, str]] = [
    {
        "Process": "GTAW",
        "Forms": "Sheet, tube, light gauge extrusions",
        "Positions": "All (1G/2G/3G/4G, 1F-4F)",
        "Limitations": "Use direct current electrode negative for most alloys; AC with balance control for aluminum; backing or purge required on full-penetration joints",
    },
    {
        "Process": "GMAW-P",
        "Forms": "Sheet and thin plate with spray or pulsed transfer",
        "Positions": "Flat, horizontal, limited vertical-up",
        "Limitations": "Preferred for controlled heat input; short-circuit only where allowed by WPS for thin gage and fillets",
    },
    {
        "Process": "FCAW-G",
        "Forms": "Structural shapes, thicker sheet assemblies",
        "Positions": "All position with appropriate classification",
        "Limitations": "Requires external shielding; restrict for thin sheet due to higher heat and spatter",
    },
    {
        "Process": "Brazing (torch/furnace)",
        "Forms": "Lap joints, hem flanges, honeycomb core skins",
        "Positions": "Primarily flat/fixtured",
        "Limitations": "Gap uniformity critical; flux selection and post-cleaning per filler manufacturer and spec",
    },
]

MATERIAL_THICKNESS_LIMITS: List[Dict[str, str]] = [
    {
        "Process": "GTAW",
        "Thickness Qualified": "0.020 in to 0.500 in depending on test coupon",
        "Notes": "Use backing for full-penetration under 0.125 in; pulse recommended for thin aluminum",
    },
    {
        "Process": "GMAW-P",
        "Thickness Qualified": "0.063 in to 0.750 in",
        "Notes": "Spray/pulsed transfer for >0.125 in; short-circuit limited to sheet if procedure qualified",
    },
    {
        "Process": "Brazing",
        "Thickness Qualified": "0.010 in to 0.125 in typical for sheet lap joints",
        "Notes": "Control joint gap (0.002-0.006 in) and capillary action; thicker sections require soak control",
    },
]

ASSEMBLY_TESTS: List[Dict[str, str]] = [
    {
        "Assembly Test": "Macroetch",
        "Requirement": "Sectioned sample shows full penetration/filler distribution; fusion to root/backing",
        "When": "Each procedure qualification and periodic audit per MIL-SD-248D",
    },
    {
        "Assembly Test": "Fillet break/face bend",
        "Requirement": "No open defects >1/8 in; sound fusion at root",
        "When": "Performance qualification for fillet positions",
    },
    {
        "Assembly Test": "Proof/pressure test",
        "Requirement": "Leak-tight to drawing requirement (e.g., 1.5x design pressure)",
        "When": "Tanks/ducting; procedure demonstration",
    },
]

FILLER_COMBINATIONS: List[Dict[str, str]] = [
    {
        "Base Metal": "Carbon steel",
        "Filler": "ER70S-6 / E7018",
        "Process": "GMAW / SMAW",
        "Notes": "Suitable for structural sheet; low hydrogen electrodes for restraint",
    },
    {
        "Base Metal": "304/316 stainless",
        "Filler": "ER308L / ER309L",
        "Process": "GTAW / GMAW-P",
        "Notes": "Use ER309L when welding dissimilar or cladding",
    },
    {
        "Base Metal": "6061-T6",
        "Filler": "ER4043 (general), ER5356 (higher strength)",
        "Process": "GTAW / GMAW",
        "Notes": "Avoid ER5356 if service >150°F where stress corrosion risk exists",
    },
    {
        "Base Metal": "Nickel alloys",
        "Filler": "ERNiCr-3; BNi-2 for brazing",
        "Process": "GTAW / Brazing",
        "Notes": "Maintain inert backing; control heat input for precipitate-hardened grades",
    },
]

QUALIFICATION_LIMITS: List[Dict[str, str]] = [
    {
        "Test": "Groove weld procedure",
        "Limitation": "Qualified thickness range per coupon (e.g., 0.250 in qualifies 0.125-0.500 in); position qualified separately",
    },
    {
        "Test": "Fillet weld performance",
        "Limitation": "Welder qualified for equal or smaller fillet size and same or easier position",
    },
    {
        "Test": "Brazing procedure",
        "Limitation": "Qualified base-metal thickness ±50% of test coupon; joint type limited to tested configuration",
    },
    {
        "Test": "Brazing performance",
        "Limitation": "Operator limited to process, filler, joint type, and base-metal thickness tested",
    },
]

PERFORMANCE_EVAL: List[Dict[str, str]] = [
    {
        "Evaluation": "Visual examination",
        "Requirement": "No cracks, lack of fusion, excessive reinforcement, or undercut per acceptance criteria",
    },
    {
        "Evaluation": "Bend tests",
        "Requirement": "Root/face bends with no open defects >1/8 in in tensile surface",
    },
    {
        "Evaluation": "Radiography/UT",
        "Requirement": "Where specified for critical joints; must meet volumetric acceptance per MIL-SD-248D",
    },
]

BRAZING_REQUIREMENTS: List[Dict[str, str]] = [
    {
        "Topic": "Base material cleanliness",
        "Requirement": "Oxide removal and solvent cleaning immediately prior to brazing; avoid chloride residues",
    },
    {
        "Topic": "Brazing alloy",
        "Requirement": "BNi-2 for nickel alloys; BAlSi-4/BAlSi-1 for aluminum; follow flow/clearance guidance",
    },
    {
        "Topic": "Flux/atmosphere",
        "Requirement": "Use appropriate flux for torch brazing; vacuum or argon for furnace/inert brazing",
    },
    {
        "Topic": "Post-braze cleaning",
        "Requirement": "Remove flux residues; inspect for voids and flow completeness via section or NDI",
    },
]

BRAZING_QUALIFICATION: List[Dict[str, str]] = [
    {
        "Item": "Brazing alloys for PQ",
        "Requirement": "Use production filler type and thickness range; document heat/lot",
    },
    {
        "Item": "Performance test specimens",
        "Requirement": "Lap shear coupons sized to joint design; furnace/torch cycle recorded",
    },
    {
        "Item": "Thickness qualified",
        "Requirement": "Test coupon thickness qualifies 0.5x to 2x of tested thickness for same alloy family",
    },
    {
        "Item": "Axial load / torque",
        "Requirement": "Demonstrate joint can meet calculated load or torque from design allowables; fixture and record peak values",
    },
]

GD_T_CALL_OUTS: List[Dict[str, str]] = [
    {"Callout": "Flatness (⏤)", "Use": "Control skin panels after brazing to prevent oil-canning"},
    {"Callout": "Perpendicularity (⌖)", "Use": "Maintain flange-to-web alignment on formed channels"},
    {"Callout": "Position (⌀)", "Use": "Locate pierced holes for fasteners and brazed inserts"},
    {"Callout": "Profile of a surface (∩)", "Use": "Capture aerodynamic surface after forming/brazing"},
]

# Engineering equations and their metadata for solver page
@dataclass
class EngineeringEquation:
    name: str
    expression: str
    variables: Dict[str, str]


EQUATIONS: List[EngineeringEquation] = [
    EngineeringEquation(
        name="Shear flow between bonded plates",
        expression="tau - V*Q/(I*b)",
        variables={
            "tau": "Shear stress (psi)",
            "V": "Shear force (lbf)",
            "Q": "First moment of area about the neutral axis (in^3)",
            "I": "Moment of inertia of the section (in^4)",
            "b": "Width of the bond line (in)",
        },
    ),
    EngineeringEquation(
        name="Punching force",
        expression="F - (t * L * S_s)",
        variables={
            "F": "Punching force (lbf)",
            "t": "Sheet thickness (in)",
            "L": "Total length of cut/perimeter (in)",
            "S_s": "Shear strength of material (psi)",
        },
    ),
    EngineeringEquation(
        name="Air bending force (approximate)",
        expression="F - (k * S_t * t**2 * W / (8 * V_d))",
        variables={
            "F": "Force per unit length (lbf/in)",
            "k": "Die/geometry factor (≈1.33 for V-die air bend)",
            "S_t": "Tensile strength (psi)",
            "t": "Sheet thickness (in)",
            "W": "Part width engaged (in)",
            "V_d": "V-die opening (in)",
        },
    ),
]


def resolved_docs() -> List[Dict[str, str]]:
    """Return document links plus local availability info."""
    rows: List[Dict[str, str]] = []
    for title, links in DOC_LINKS.items():
        local_path = Path(links["local"])
        size = local_path.stat().st_size if local_path.exists() else 0
        rows.append(
            {
                "Document": title,
                "External Link": links["external"],
                "Local Copy": str(local_path),
                "Exists Locally": "Yes" if local_path.exists() else "No",
                "File Size (bytes)": size,
            }
        )
    return rows


def download_references() -> List[Tuple[str, bool, str]]:
    """Attempt to download missing reference PDFs and return status entries.

    Each tuple: (document title, success flag, message)
    """
    results: List[Tuple[str, bool, str]] = []
    for title, links in DOC_LINKS.items():
        local_path = Path(links["local"])
        if local_path.exists():
            results.append((title, True, "Already present"))
            continue

        try:
            response = requests.get(links["external"], timeout=30)
            response.raise_for_status()
            local_path.parent.mkdir(parents=True, exist_ok=True)
            local_path.write_bytes(response.content)
            results.append((title, True, f"Downloaded to {local_path}"))
        except Exception as exc:  # pragma: no cover - network dependent
            results.append((title, False, f"Download failed: {exc}"))
    return results
