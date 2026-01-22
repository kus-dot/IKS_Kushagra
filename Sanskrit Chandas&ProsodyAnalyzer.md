# Sanskrit Chandas & Prosody Analyzer (Streamlit)

This project is an interactive **Sanskrit prosody (Chandas) analysis tool** built using **Python and Streamlit**.  
It analyzes a given Sanskrit verse (śloka) and computes its **Laghu–Guru (L/G) syllabic structure**, along with statistical and visual metrics inspired by classical and modern analysis techniques.

The tool is intended for:
- Sanskrit prosody exploration
- Computational linguistics experiments
- Digital humanities and research demos
- Educational visualization of metrical patterns

---

## Features

- Laghu–Guru syllable extraction
- LG sequence visualization
- Laghu vs Guru count and ratio
- Meter heaviness classification (Light / Balanced / Heavy)
- Shannon entropy of syllable sequence
- Laghu–Guru transition matrix (heatmap)
- Pāda-wise syllable distribution
- Pingala (Fibonacci-based) metrical count
- CSV export of syllable-level data
- Fully interactive web interface using Streamlit

---

## How to Run Locally

```bash
pip install streamlit
streamlit run app.py
