import streamlit as st
import random

# Basic settings
st.set_page_config(page_title="Fretboard Cracker", layout="centered")
st.title("🎸 Fretboard Cracker")

# Static fretboard map (string 6 to 1, frets 0~24)
fretboard_map = {
    6: ["E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E"],
    5: ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A"],
    4: ["D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D"],
    3: ["G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G"],
    2: ["B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],
    1: ["E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E"]
}

# Mode selection
mode = st.radio("Select a mode:", ("Mode 1: Guess note from position", "Mode 2: Guess fret from note"))

if "quiz" not in st.session_state:
    st.session_state.quiz = None
    st.session_state.answer = ""

# Generate a new quiz question
def new_quiz(max_fret=24):
    string_num = random.randint(1, 6)
    fret_num = random.randint(0, max_fret)
    note = fretboard_map[string_num][fret_num]
    st.session_state.quiz = {
        "string": string_num,
        "fret": fret_num,
        "note": note
    }
    st.session_state.answer = ""

# Display quiz and input fields
if mode == "Mode 1: Guess note from position":
    if st.button("Generate New Question") or st.session_state.quiz is None:
        new_quiz()

    q = st.session_state.quiz
    st.subheader(f"String {q['string']}, Fret {q['fret']}: What is the note?")
    ans = st.text_input("Enter the note (e.g., C, D#, A#):", key="mode1")

    if st.button("Submit Answer (Mode 1)"):
        if ans:
            correct = q['note'].upper() == ans.strip().upper()
            st.write(f"\n✅ Correct!" if correct else f"\n❌ Incorrect, the correct answer is {q['note']}")
        else:
            st.warning("Please enter a note first.")

elif mode == "Mode 2: Guess fret from note":
    if st.button("Generate New Question") or st.session_state.quiz is None:
        string_num = random.randint(1, 6)
        fret_num = random.randint(0, 12)  # Only frets 0-12
        note = fretboard_map[string_num][fret_num]
        st.session_state.quiz = {
            "string": string_num,
            "fret": fret_num,
            "note": note
        }
        st.session_state.answer = ""

    q = st.session_state.quiz
    st.subheader(f"On string {q['string']}, where is the note {q['note']}?")
    guess = st.number_input("Enter fret number (0–12):", min_value=0, max_value=12, step=1, key="mode2")

    if st.button("Submit Answer (Mode 2)"):
        correct = (q['fret'] % 12) == guess
        st.write(f"✅ Correct!" if correct else f"❌ Incorrect, the correct fret is {q['fret']}")
