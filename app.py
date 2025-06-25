import streamlit as st
import matplotlib.pyplot as plt
import random

# Basic settings
st.set_page_config(page_title="Fretboard Cracker", layout="centered")
st.title("🎸 Fretboard Cracker")

# NOTE ORDER
NOTE_ORDER = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
open_notes = ["E", "B", "G", "D", "A", "E"]  # From string 6 (bottom) to string 1 (top)

# Generate 12-fret fretboard
def generate_fretboard():
    fretboard = []
    for note in open_notes:
        start = NOTE_ORDER.index(note)
        fretboard.append([NOTE_ORDER[(start + i) % 12] for i in range(12)])
    return fretboard  # Keep order: String 6 to String 1

# Draw fretboard with quiz point
def draw_fretboard(quiz_string=None, quiz_fret=None, mode="guess_note"):
    fretboard = generate_fretboard()
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.set_xlim(-0.5, 11.5)
    ax.set_ylim(-0.5, 5.5)
    ax.set_xticks(range(12))
    ax.set_xticklabels([f"{i}" for i in range(12)], fontsize=14)
    ax.set_yticks(range(6))
    ax.set_yticklabels([f"String {6 - i}" for i in range(6)], fontsize=14)

    for i, string in enumerate(fretboard):  # i = 0 (String 6), ..., 5 (String 1)
        y = 5 - i  # Reverse vertical position: 0 → top, 5 → bottom
        for fret, note in enumerate(string):
            color = 'black'
            if quiz_string == i and quiz_fret == fret:
                # Draw a red circle behind the label
                circle = plt.Circle((fret, y), 0.35, facecolor='none', edgecolor='red', linewidth=1.5)
                ax.add_patch(circle)
                label = note if mode == "show_answer" else "?"
                ax.text(fret, y, label, ha='center', va='center', fontsize=18, color='red', fontweight='bold')
            # else:
            #     ax.text(fret, y, note, ha='center', va='center', fontsize=16, color='black', fontweight='bold')

    for i in range(12):
        ax.axvline(i, color='gray', linewidth=0.5)
    for y in range(6):
        ax.hlines(y, -0.5, 11.5, color='black', linewidth=1)

    ax.set_title("Guitar Fretboard Quiz", fontsize=18)
    return fig

# Streamlit mode toggle
mode = st.radio("Select mode:", ("Guess note from position (Graph)", "Show answer"))

# Random quiz location
if "quiz_point" not in st.session_state or st.button("New Question"):
    st.session_state.quiz_point = {
        "string": random.randint(0, 5),  # 0 = string 6, ..., 5 = string 1
        "fret": random.randint(0, 11)
    }

q = st.session_state.quiz_point

# Draw with or without answer
if mode == "Guess note from position (Graph)":
    fig = draw_fretboard(quiz_string=q['string'], quiz_fret=q['fret'], mode="guess_note")
    st.pyplot(fig)
    ans = st.text_input("What is the note at red dot? (e.g., C, D#, A#):")
    correct_note = generate_fretboard()[q['string']][q['fret']]
    if st.button("Submit Answer"):
        if ans.strip().upper() == correct_note:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. Correct answer is {correct_note}.")

elif mode == "Show answer":
    fig = draw_fretboard(quiz_string=q['string'], quiz_fret=q['fret'], mode="show_answer")
    st.pyplot(fig)
