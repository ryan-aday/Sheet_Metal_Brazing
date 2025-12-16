# Sheet Metal Brazing Streamlit App

This repository contains a multipage Streamlit app that summarizes guidance inspired by MIL-SD-248D and MIL-S-23284A. The app provides quick references for sheet metal welding and brazing, qualification limits, inspection checklists, and engineering equations.

## Running the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

Use the Streamlit sidebar to navigate the pages:

- **Materials, Fillers, and Drawings**: Base and filler materials with associated processes, GD&T callouts, and document links (with an on-page download helper for the PDFs).
 - **Materials, Fillers, and Drawings**: Base and filler materials with associated processes, GD&T callouts, document links (with an on-page download helper for the PDFs), and automatic extraction of MIL-SD-248D tables/footnotes when a local copy is present.
- **Inspection & Procedure Limits**: Inspection checklist, welding procedure limitations, and material thickness limits.
- **Procedure & Performance Qualification**: Filler/process combinations, qualification test limitations, evaluation methods, and assembly test requirements.
- **Brazing Requirements**: Brazing material/alloy requirements and qualification notes including axial load/torque reminders.
- **Sheet Metal Engineering Equations**: Sympy-powered solver for shear, punching force, and bending equations.

## Reference files

Place local copies of the specifications in the `files/` directory with the following filenames:

- `files/MIL-SD-248D.pdf`
- `files/MIL-S-23284A.pdf`

If the files are present, the app will flag them as available and automatically display any tables/footnotes parsed from MIL-SD-248D; otherwise, it will remind you to download them manually.

You can also click **Attempt to download missing PDFs** on the "Materials, Fillers, and Drawings" page. The helper uses the external links above and will report any proxy or network errors so you know whether to download the files manually instead.
