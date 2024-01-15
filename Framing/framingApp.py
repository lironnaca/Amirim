import time
import csv
import pandas as pd
import sys
import openai

def createFraming(filePath, promptForPos, promptForNeg):
    with open(filePath, mode='r', newline='') as file:
        df = pd.read_csv(filePath, encoding='unicode_escape')

        for index, row in df.iterrows():
            sentence = row["sentence_text"]

            dic = [{"role": "user", "content": promptForPos}]
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=dic)
            posReply = chat.choices[0].message.content.split("\n")

            dic = [{"role": "user", "content": promptForNeg}]
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=dic)
            negReply = chat.choices[0].message.content.split("\n")

            df.at[index, 'Positive Framing'] = posReply
            df.at[index, 'Negative Framing'] = negReply

if __name__ == '__main__':
    openAIKey = sys.argv[1]
    filePath = sys.argv[2]
    promptForPos = sys.argv[3]
    promptForNeg = sys.argv[4]

