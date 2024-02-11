import pandas as pd
import random
if __name__ == '__main__':
    csv_files = ['../TaggingApp/Sentences/TempleteOneWithNegativeVerbs.csv',
                 '../TaggingApp/Sentences/TempleteOneWithPositiveVerbs.csv',
                 '../TaggingApp/Sentences/TempleteTwoWithNegativeAdjectives.csv',
                 '../TaggingApp/Sentences/TempleteTwoWithPositiveAdjectives.csv']

    dfs = [pd.read_csv(file) for file in csv_files]
    combined_df = pd.concat(dfs, ignore_index=True)

    positive_sentences = combined_df[combined_df['answer'] == 'positive']['sentence_text'].tolist()
    negative_sentences = combined_df[combined_df['answer'] == 'negative']['sentence_text'].tolist()

    selected_positive_sentences = random.sample(positive_sentences, 50)
    selected_negative_sentences = random.sample(negative_sentences, 50)

    final_df = pd.DataFrame({'sentence': selected_positive_sentences + selected_negative_sentences,
                             'label': ['positive'] * 50 + ['negative'] * 50})

    final_df.to_csv('testData.csv', index=False)
