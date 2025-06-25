import streamlit as st
import matplotlib.pyplot as plt
import random

# Basic settings
st.set_page_config(page_title="Fretboard Cracker", layout="centered")
st.title("🎸 Fretboard Cracker")

# NOTE ORDER
NOTE_ORDER = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
open_notes = ["E", "B", "G", "D", "A", "E"]  # From string 6 (bottom) to string 1 (top)

# Enharmonic equivalents mapping
ENHARMONIC_EQUIVS = {
    "B#": "C", "E#": "F",
    "CB": "B", "FB": "E",
    "DB": "C#", "EB": "D#", "GB": "F#", "AB": "G#", "BB": "A#",
    "C#": "C#", "D#": "D#", "F#": "F#", "G#": "G#", "A#": "A#",
    "C": "C", "D": "D", "E": "E", "F": "F", "G": "G", "A": "A", "B": "B"
}

def normalize_note(note):
    return ENHARMONIC_EQUIVS.get(note.upper().replace("♯", "#").replace("♭", "B"), note.upper())

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
            if quiz_string == i and quiz_fret == fret:
                # Draw a red circle behind the label
                circle = plt.Circle((fret, y), 0.35, facecolor='none', edgecolor='red', linewidth=1.5)
                ax.add_patch(circle)
                label = note if mode == "Find fret from the note" else "?"
                ax.text(fret, y, label, ha='center', va='center', fontsize=18, color='red', fontweight='bold')
            # Uncomment this block if you want to show other notes:
            # else:
            #     ax.text(fret, y, note, ha='center', va='center', fontsize=16, color='black', fontweight='bold')

    for i in range(12):
        ax.axvline(i, color='gray', linewidth=0.5)
    for y in range(6):
        ax.hlines(y, -0.5, 11.5, color='black', linewidth=1)

    ax.set_title("Guitar Fretboard Quiz", fontsize=18)
    return fig

def draw_fretboard_interactive(target_string=None):
    fretboard = generate_fretboard()
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.set_xlim(-0.5, 11.5)
    ax.set_ylim(-0.5, 5.5)
    ax.set_xticks(range(12))
    ax.set_xticklabels([f"{i}" for i in range(12)], fontsize=14)
    ax.set_yticks(range(6))
    ax.set_yticklabels([f"String {6 - i}" for i in range(6)], fontsize=14)

    for i, string in enumerate(fretboard):
        y = 5 - i
        for fret, note in enumerate(string):
            if target_string is not None and i != target_string:
                continue  # only show the target string
            if fret in [0, 3, 5, 7, 9] and random.random() < 0.3:
                ax.text(fret, y, note, ha='center', va='center', fontsize=14, color='black')


    for i in range(12):
        ax.axvline(i, color='gray', linewidth=0.5)
    for y in range(6):
        if (5 - y) == target_string:
            ax.hlines(y, -0.5, 11.5, color='red', linewidth=1.5)
        else:
            ax.hlines(y, -0.5, 11.5, color='black', linewidth=1)

    ax.set_title("Guitar Fretboard (Target String Highlighted)", fontsize=18)
    return fig


# Streamlit mode toggle
mode = st.radio("Select mode:", ("Guess note from position (Graph)", "Find fret from the note"))

if "quiz_point" not in st.session_state:
    st.session_state.quiz_point = {
        "string": random.randint(0, 5),
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
        user_note = normalize_note(ans.strip())
        correct_note_std = normalize_note(correct_note)
        if user_note == correct_note_std:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. Correct answer is {correct_note}.")

elif mode == "Find fret from the note":
    fretboard = generate_fretboard()

    # 初始化 target question
    if "note_target" not in st.session_state:
        target_string = random.randint(0, 5)
        target_fret = random.randint(0, 11)
        note = fretboard[target_string][target_fret]
        st.session_state.note_target = {
            "string": target_string,
            "note": note
        }

    # 顯示提示
    target = st.session_state.note_target
    # display_string = 6 - target["string"]
    target_string_display = target["string"] + 1

    st.markdown(
        f"""
        <div style='font-size:24px; font-weight:500; padding: 8px 0;'>
            🎯 Find the note 
            <span style='color:#f0f0f0; background-color:#333; padding:3px 6px; border-radius:5px; font-family:monospace;'>{target['note']}</span>
            on <b>String {target_string_display}</b>
        </div>
        """,
        unsafe_allow_html=True
    )



    # 顯示 fretboard（只顯示目標弦）
    fig = draw_fretboard_interactive(target_string=target["string"])
    st.pyplot(fig)

    # 顯示 12 個按鈕代表 0~11 fret
    st.write("### Select the fret:")

    fret_options = list(range(12))
    selected_fret = st.selectbox("🎚️ Select the fret (0–11):", fret_options)

    if st.button("Submit Answer"):
        selected_note = fretboard[target["string"]][selected_fret]
        if normalize_note(selected_note) == normalize_note(target["note"]):
            st.success(f"✅ Correct! Fret {selected_fret} is {selected_note}.")
        else:
            st.error(f"❌ Incorrect. Fret {selected_fret} is {selected_note}, expected {target['note']}.")

    # if st.button("Next Question"):
    #     del st.session_state.note_target

if st.button("🔁 Next Question"):
    if mode == "Guess note from position (Graph)":
        st.session_state.quiz_point = {
            "string": random.randint(0, 5),
            "fret": random.randint(0, 11)
        }
    elif mode == "Find fret from the note":
        if "note_target" in st.session_state:
            del st.session_state.note_target
    st.rerun()
