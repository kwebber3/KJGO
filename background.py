from pandas import *
import pandas as pd

MAX_SCORE = 6000
START_SCORE = 1
JAPANESE_HEADER = "Japanese"
ENGLISH_HEADER = "English"
JP_SENTENCE_HEADER = "Japanese Example"
ENG_SENTENCE_HEADER = "English Sentence"
L_SCORE_HEADER = "listening score"
S_SCORE_HEADER = "speaking score"

KANJI_HEADER = "Kanji"
R_HEADER = "Reading"
R_SCORE_HEADER = "reading score"
W_SCORE_HEADER = "writing score"
E_SENT_HEADER = "Example Sentence"
E_SENT_R_HEADER = "Example Sentence Reading"

MIN_SCORE = 10

def load_listening_dictionary(filename, sep = "\t"):
    x = read_table(filepath_or_buffer=filename, delimiter=sep)
    
    dictionary = {}

    for number in range(0,MAX_SCORE):
        dictionary[number] = []

    i = 1
    for index, row in x.iterrows():
        this_score = row[L_SCORE_HEADER]
        dictionary[this_score].append([row[JAPANESE_HEADER],row[ENGLISH_HEADER],row[JP_SENTENCE_HEADER],row[ENG_SENTENCE_HEADER],row[S_SCORE_HEADER]])
        i = i + 1

    score_weights = update_weights(dictionary, i)
    return dictionary, score_weights, i
def export_listeningLibrary_to_txt(scored_dict,filename,delimiter ="\t"):
    score_table = format_to_table_listening(scored_dict)
    score_table.to_csv(filename, sep = delimiter)
def format_to_table_listening(scored_dictionary):
    values = {}
    i = 0
    for eachScore in scored_dictionary.keys():
        for eachCard in scored_dictionary[eachScore]:
            thisRow = eachCard
            thisRow.append(eachScore)
            values.update({i:thisRow})
            i = i + 1
    return(pd.DataFrame(values.values(),columns=[JAPANESE_HEADER, ENGLISH_HEADER, JP_SENTENCE_HEADER, ENG_SENTENCE_HEADER,S_SCORE_HEADER,L_SCORE_HEADER]))

def load_speaking_dictionary(filename, sep = "\t"):
    x = read_table(filepath_or_buffer=filename, delimiter=sep)
    
    dictionary = {}
    
    for number in range(0,MAX_SCORE):
        dictionary[number] = []
    
    i = 1
    for index, row in x.iterrows():
        this_score = row[S_SCORE_HEADER]
        if (row[L_SCORE_HEADER] < MIN_SCORE):
            this_score = 0
        dictionary[this_score].append([row[JAPANESE_HEADER],row[ENGLISH_HEADER],row[JP_SENTENCE_HEADER],row[ENG_SENTENCE_HEADER],row[L_SCORE_HEADER]])
        i = i + 1

    score_weights = update_weights(dictionary, i )

    return dictionary, score_weights, i
def export_speakingLibrary_to_txt(scored_dict,filename,delimiter ="\t"):
    score_table = format_to_table_speaking(scored_dict)
    score_table.to_csv(filename, sep = delimiter)
def format_to_table_speaking(scored_dictionary):
    values = {}
    i = 0
    for eachScore in scored_dictionary.keys():
        for eachCard in scored_dictionary[eachScore]:
            thisRow = eachCard
            thisRow.append(eachScore)
            values.update({i:thisRow})
            i = i + 1
    return(pd.DataFrame(values.values(),columns=[JAPANESE_HEADER, ENGLISH_HEADER, JP_SENTENCE_HEADER, ENG_SENTENCE_HEADER,L_SCORE_HEADER,S_SCORE_HEADER]))

def load_reading_dictionary(filename, sep = "\t"):
    x = read_table(filepath_or_buffer=filename, delimiter=sep)
    
    dictionary = {}
    
    
    for number in range(0,MAX_SCORE):
        dictionary[number] = []
    
    i = 1
    for index, row in x.iterrows():
        this_score = row[R_SCORE_HEADER]
        dictionary[this_score].append([row[KANJI_HEADER],row[ENGLISH_HEADER],row[E_SENT_HEADER],row[E_SENT_R_HEADER],row[ENG_SENTENCE_HEADER],row[W_SCORE_HEADER],row[R_HEADER]])
        i = i + 1
        
    score_weights = update_weights(dictionary, i )

    return dictionary, score_weights, i
def export_readingLibrary_to_txt(scored_dict,filename,delimiter ="\t"):
    score_table = format_to_table_reading(scored_dict)
    score_table.to_csv(filename, sep = delimiter)
def format_to_table_reading(scored_dictionary):
    values = {}
    i = 0
    for eachScore in scored_dictionary.keys():
        for eachCard in scored_dictionary[eachScore]:
            thisRow = eachCard
            thisRow.append(eachScore)
            values.update({i:thisRow})
            i = i + 1
    return(pd.DataFrame(values.values(),columns=[KANJI_HEADER, ENGLISH_HEADER, E_SENT_HEADER, E_SENT_R_HEADER, ENG_SENTENCE_HEADER,W_SCORE_HEADER,R_HEADER,R_SCORE_HEADER]))

def load_writing_dictionary(filename, sep = "\t"):
    x = read_table(filepath_or_buffer=filename, delimiter=sep)
    
    dictionary = {}

    for number in range(0,MAX_SCORE):
        dictionary[number] = []
        
    i = 1
    for index, row in x.iterrows():
        this_score = row[W_SCORE_HEADER]
        if (row[R_SCORE_HEADER] < MIN_SCORE):
            this_score = 0
        dictionary[this_score].append([row[KANJI_HEADER],row[ENGLISH_HEADER],row[E_SENT_HEADER],row[E_SENT_R_HEADER],row[ENG_SENTENCE_HEADER],row[R_SCORE_HEADER],row[R_HEADER]])
        i = i + 1
        
    score_weights = update_weights(dictionary, i )

    return dictionary, score_weights, i
def export_writingLibrary_to_txt(scored_dict,filename,delimiter ="\t"):
    score_table = format_to_table_writing(scored_dict)
    score_table.to_csv(filename, sep = delimiter)
def format_to_table_writing(scored_dictionary):
    values = {}
    i = 0
    for eachScore in scored_dictionary.keys():
        for eachCard in scored_dictionary[eachScore]:
            thisRow = eachCard
            thisRow.append(eachScore)
            values.update({i:thisRow})
            i = i + 1
    return(pd.DataFrame(values.values(),columns=[KANJI_HEADER, ENGLISH_HEADER, E_SENT_HEADER, E_SENT_R_HEADER, ENG_SENTENCE_HEADER,R_SCORE_HEADER,R_HEADER,W_SCORE_HEADER]))

def get_card(current_score, last_score, my_scored_cards, score_weights):
   # print(current_score)
    #print(last_score)
    if not my_scored_cards[current_score] == []:
        current_card = my_scored_cards[current_score][0]
    
    else:
        selected = False
        if (selected == False and last_score != 0 and last_score != START_SCORE) and not my_scored_cards[0] == []:
            current_card = my_scored_cards[0][0]
            current_score = 0
            selected = True
            #print("This is " + str(current_score) + "not" + str(last_score))
        else:
            current_score = START_SCORE
        while current_score < len(score_weights) - 1 and not selected:
            current_score = current_score + 1
            if current_score != last_score and not my_scored_cards[current_score] == []:
                current_card = my_scored_cards[current_score][0]
                selected = True
        if selected == False and not my_scored_cards[START_SCORE] == []:
            current_card = my_scored_cards[START_SCORE][0]
            current_score = last_score
        elif selected == False and not my_scored_cards[MAX_SCORE] == []:
            current_card = my_scored_cards[MAX_SCORE][0]
            current_score = last_score
        elif selected == True:
            pass
        else:
            current_card = my_scored_cards[last_score][0]
            current_score = last_score
            #print("***")
    return current_score, current_card
def get_card_advanced(current_score, last_score, my_scored_cards, score_weights):
    #print(current_score)
    state = "GOOD"
    if not my_scored_cards[current_score] == []:
        current_card = my_scored_cards[current_score][0]
    
    else:
        selected = False
        while current_score > 1 and not selected:
            current_score = current_score - 1
            if current_score != last_score and not my_scored_cards[current_score] == []:
                current_card = my_scored_cards[current_score][0]
                selected = True
        while current_score < len(score_weights) - 1 and not selected:
            current_score = current_score + 1
            if current_score != last_score and not my_scored_cards[current_score] == []:
                current_card = my_scored_cards[current_score][0]
                selected = True
        if selected == False and last_score >= 0:
            current_card = my_scored_cards[last_score]
            current_score = last_score
            #print("***")
        else:
            current_card = "ERROR"
            current_score = last_score
            state = "ERROR"
            
    return current_score, current_card, state

def update_weights(dictionary, i):
    
    score_distribution = {}
    
    score_weights = []

    for number in range(0,MAX_SCORE):
        score_distribution[number] = len(dictionary[number]) + 1

    score_distribution[0] = 1
    
    for number in range(1,MAX_SCORE):
        score_weights.append(score_distribution[number]/(number+1)/i)

    return score_weights