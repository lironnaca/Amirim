import sys
import pandas as pd
import streamlit as st
from streamlit import session_state

INDEX = "index"

INSTRUCRIONS = """

You will encounter sentences with a positive framing, followed by three additional sentences,
 each introducing a framing.
  Select the one that effectively transforms the sentiment to negative while preserving the
   essence of the original statement.
"""

def load_data(csv_filename):
    data = pd.read_csv(csv_filename)
    return data

def save_data(data, csv_filename):
    data.to_csv(csv_filename, index=False)


def initialize_session_state(data, session_state) -> None:
    if INDEX not in session_state:
        session_state[INDEX] = 0
        while (session_state[INDEX] < len(data) and data.at[session_state[INDEX], 'answer'] in ["not suitable", "positive", "negative"]):
            session_state.index += 1

def update(data, index, csv_filename):
    data.at[index, data] = 'X'
    session_state.index += 1
    save_data(data, csv_filename)



def main():
    csv_filename = sys.argv[1]

    st.title("Best Framing Tagger")

    data = load_data(csv_filename)

    initialize_session_state(data, st.session_state)

    index = session_state.index

    if index < len(data):
      expander = st.expander(label="See Instructions")
      expander.write(INSTRUCRIONS)
      st.markdown(f"### Sentence : {data.at[index, 'base_sentence']}")
      firstSentence = data.at[index, 'first']
      secondSentence = data.at[index, 'second']
      thirdSentence = data.at[index, 'third']

      st.markdown(f"### Sentence : {firstSentence}")
      st.markdown(f"### Sentence : {secondSentence}")
      st.markdown(f"### Sentence : {thirdSentence}")


      st.markdown(f"### Sentence : {data.at[index, 'base_sentence']}")
      positive_button = st.button("First", use_container_width=True, on_click=lambda: update('first', index, csv_filename))
      negative_button = st.button("Second", use_container_width=True, on_click=lambda: update('second', index, csv_filename))
      neutral_button = st.button("Third", use_container_width=True, on_click=lambda: update('third"', index, csv_filename))

      st.metric("How Many Sentence You Did:", st.session_state.index)

    else:
        st.markdown("## Great job!")
        st.write("You've finished classifying all sentences!")

if __name__ == '__main__':
    main()