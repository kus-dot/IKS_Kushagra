import math
import csv
import html
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import streamlit as st
import io

# -----------------------------
# Sanskrit syllable processing
# -----------------------------
VOWELS = "अआइईउऊऋएऐओऔ"
MATRAS = "ािीुूृेैोौ"

def verse_to_LG_and_syllables(verse):
    syllables = []
    LG = []
    current = ""

    for ch in verse:
        if ch.isspace():
            continue

        current += ch

        if ch in VOWELS:
            syllables.append(current)
            LG.append('G' if ch in "आईऊएऐओऔ" else 'L')
            current = ""

        elif ch in MATRAS:
            syllables.append(current)
            LG.append('G' if ch in "ाीूेैोौ" else 'L')
            current = ""

    return syllables, LG

# -----------------------------
# Shannon entropy
# -----------------------------
def shannon_entropy(LG):
    total = len(LG)
    if total == 0:
        return 0
    counts = Counter(LG)
    entropy = 0
    for v in counts.values():
        p = v / total
        entropy -= p * math.log2(p)
    return round(entropy, 3)

# -----------------------------
# Transition matrix
# -----------------------------
def transition_matrix(LG):
    mat = {('L','L'):0, ('L','G'):0, ('G','L'):0, ('G','G'):0}
    for a, b in zip(LG, LG[1:]):
        mat[(a,b)] += 1
    return mat

# -----------------------------
# Pāda split
# -----------------------------
def split_padas(LG, parts=4):
    size = max(1, len(LG) // parts)
    return [LG[i*size:(i+1)*size] for i in range(parts)]

# -----------------------------
# Pingala recursion
# -----------------------------
def pingala_count(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Sanskrit Chandas Analyzer", layout="centered")

st.title("Sanskrit Chandas & Prosody Analyzer")
st.write("Enter a Sanskrit śloka to analyze Laghu–Guru structure, entropy, transitions, and Pingala metrics.")

verse = st.text_area("Enter Sanskrit Verse", height=120)

if st.button("Analyze Verse") and verse.strip():

    sylls, LG = verse_to_LG_and_syllables(verse)
    total = len(LG)
    counts = Counter(LG)

    lcount = counts.get('L', 0)
    gcount = counts.get('G', 0)

    ratio = round(gcount / total, 2) if total else 0
    heaviness = (
        "Heavy" if ratio > 0.5 else
        "Balanced" if ratio >= 0.4 else
        "Light"
    )

    entropy = shannon_entropy(LG)
    trans = transition_matrix(LG)
    padas = split_padas(LG)

    # -----------------------------
    # Text outputs (terminal equivalent)
    # -----------------------------
    st.subheader("LG Sequence")
    st.code(" ".join(LG))

    st.subheader("Summary Metrics")
    st.write(f"**Laghu (L):** {lcount}")
    st.write(f"**Guru (G):** {gcount}")
    st.write(f"**Guru/Laghu Ratio:** {ratio}")
    st.write(f"**Meter Heaviness:** {heaviness}")
    st.write(f"**Shannon Entropy:** {entropy}")
    st.write(f"**Pingala Count (n={total}):** {pingala_count(total)}")

    # -----------------------------
    # CSV download
    # -----------------------------
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["Index", "Syllable", "L/G"])
    for i, (s, g) in enumerate(zip(sylls, LG), start=1):
        writer.writerow([i, s, g])

    st.download_button(
        label="Download CSV",
        data=csv_buffer.getvalue(),
        file_name="verse_analysis.csv",
        mime="text/csv"
    )

    # -----------------------------
    # Plot 1: Binomial
    # -----------------------------
    fig1, ax1 = plt.subplots(figsize=(4,3))
    ax1.bar(["Laghu (L)", "Guru (G)"], [lcount, gcount])
    ax1.set_ylabel("Count")
    ax1.set_title("Laghu vs Guru Count")
    st.pyplot(fig1)

    # -----------------------------
    # Plot 2: Transition Heatmap
    # -----------------------------
    heatmap = np.array([
        [trans[('L','L')], trans[('L','G')]],
        [trans[('G','L')], trans[('G','G')]]
    ])

    fig2, ax2 = plt.subplots(figsize=(4,3))
    im = ax2.imshow(heatmap)
    plt.colorbar(im, ax=ax2)
    ax2.set_xticks([0,1])
    ax2.set_yticks([0,1])
    ax2.set_xticklabels(['L','G'])
    ax2.set_yticklabels(['L','G'])
    ax2.set_xlabel("Next syllable")
    ax2.set_ylabel("Current syllable")
    ax2.set_title("Laghu–Guru Transition Heatmap")

    for i in range(2):
        for j in range(2):
            ax2.text(j, i, heatmap[i,j], ha='center', va='center')

    st.pyplot(fig2)

    # -----------------------------
    # Plot 3: Pāda-wise distribution
    # -----------------------------
    pada_L = [p.count('L') for p in padas]
    pada_G = [p.count('G') for p in padas]
    x = np.arange(len(padas))

    fig3, ax3 = plt.subplots(figsize=(6,3))
    ax3.bar(x-0.2, pada_L, width=0.4, label='L')
    ax3.bar(x+0.2, pada_G, width=0.4, label='G')
    ax3.set_xticks(x)
    ax3.set_xticklabels([f"Pāda {i+1}" for i in x])
    ax3.set_ylabel("Count")
    ax3.set_title("Pāda-wise Laghu–Guru Distribution")
    ax3.legend()

    st.pyplot(fig3)

    # -----------------------------
    # Plot 4: Pingala sequence
    # -----------------------------
    xs = list(range(1, total + 1))
    ys = [pingala_count(x) for x in xs]

    fig4, ax4 = plt.subplots(figsize=(5,3))
    ax4.plot(xs, ys, marker='o')
    ax4.set_xlabel("n (syllable length)")
    ax4.set_ylabel("Pingala count")
    ax4.set_title("Pingala Recursive Count")
    ax4.grid(True)

    st.pyplot(fig4)
