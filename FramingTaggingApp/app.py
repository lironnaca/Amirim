import sys
import pandas as pd
import streamlit as st
from streamlit import session_state

INDEX = "index"

INSTRUCRIONS = """
You will encounter sentences with a positive framing, followed by four additional sentences,
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
        while (session_state[INDEX] < len(data) and (
               data.at[session_state[INDEX], 'isFirst'] == 'X' or
               data.at[session_state[INDEX], 'isSecond'] == 'X' or
               data.at[session_state[INDEX], 'isThird'] == 'X' or
               data.at[session_state[INDEX], 'isForth'] == 'X'
        )):
            session_state.index += 1

def update(data, index, csv_filename, col):
    data.at[index, col] = 'X'
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
      st.markdown(f"### Sentence : {data.at[index, 'Sentence']}")
      firstSentence = data.at[index, 'First']
      secondSentence = data.at[index, 'Second']
      thirdSentence = data.at[index, 'Third']
      fourthSentence = data.at[index, 'Fourth']


      st.markdown(f"### Sentence : {firstSentence}")
      fisrt_button = st.button("First", use_container_width=True, on_click=lambda: update(data, index, csv_filename, "isFirst"))

      st.markdown(f"### Sentence : {secondSentence}")
      second_button = st.button("Second", use_container_width=True, on_click=lambda: update(data, index, csv_filename, "isSecond"))

      st.markdown(f"### Sentence : {thirdSentence}")
      third_button = st.button("Third", use_container_width=True, on_click=lambda: update(data, index, csv_filename, "isThird"))

      st.markdown(f"### Sentence : {fourthSentence}")
      fourth_button = st.button("Fourth", use_container_width=True, on_click=lambda: update(data, index, csv_filename, "isFourth"))



      st.markdown(f"### Sentence : {data.at[index, 'Sentence']}")

      st.metric("How Many Sentence You Did:", st.session_state.index)

    else:
        st.markdown("## Great job!")
        st.write("You've finished classifying all sentences!")

if __name__ == '__main__':
    main()
