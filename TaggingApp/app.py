import sys
import pandas as pd
import streamlit as st
from streamlit import session_state

INDEX = "index"

INSTRUCRIONS = """
Welcome to the Base-Sentences Sentiment Tagger!

In this task, we focus on tagging sentences to serve as base sentences. These sentences will act as a foundation upon which we will later apply framing effects. Framing effects refer to the phenomenon where the presentation of information influences individuals' perceptions and reactions. Let's dive into the details of this mission.

Tagging Options:
1. The sentence is not suitable as a base sentence:
   - Tag: `Not Suitable`
   - Explanation: Use this tag when the sentence is unsuitable as a base. This could be due to various factors like a framing effect won't effectively change the sentiment of the reader, sentence being too long, too short, not appropriate, with netural sentiment.

2. The sentence will be a good base sentence, and the sentiment is positive:
   - Tag: `Positive Base`
   - Explanation: Assign this tag to sentences that have a strong but not excessively strong positive sentiment.

3. The sentence will be a good base sentence, and the sentiment is negative:
   - Tag: `Negative Base`
   - Explanation: Tag sentences with a strong but not overly strong negative sentiment. These sentences will serve as a base for applying negative framing effects.


Mission Guidelines:
- Consider Length and Appropriateness: Assess the suitability of sentences as base sentences, considering factors like length and appropriateness. We don't want the sentences to be very long, as the framing will then make them even longer.
- Balance Strength: Ensure that the sentiment strength is notable but not extreme, providing a suitable base for framing effects.

Your contributions in tagging these sentences will play a crucial role in refining the understanding of framing effects in natural language processing. Thank you for your participation in this mission!
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

def update(data, index, tag, csv_filename):
    data.at[index, 'answer'] = tag
    session_state.index += 1
    save_data(data, csv_filename)



def main():
    csv_filename = sys.argv[1]

    st.title("Base Sentences Tagger")

    data = load_data(csv_filename)

    initialize_session_state(data, st.session_state)

    index = session_state.index

    if index < len(data):
      expander = st.expander(label="See Instructions")
      expander.write(INSTRUCRIONS)
      st.markdown(f"### Sentence : {data.at[index, 'sentence_text']}")
      positive_button = st.button("Not Suitable", use_container_width=True, on_click=lambda: update(data, index, "not suitable", csv_filename))
      negative_button = st.button("Positive Base", use_container_width=True, on_click=lambda: update(data, index, "positive", csv_filename))
      neutral_button = st.button("Negative Base", use_container_width=True, on_click=lambda: update(data, index, "negative", csv_filename))

      st.metric("How Many Sentence You Did:", st.session_state.index)

    else:
        st.markdown("## Great job!")
        st.write("You've finished classifying all sentences!")

if __name__ == '__main__':
    main()