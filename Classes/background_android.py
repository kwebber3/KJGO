from pandas import *
import pandas as pd
import random

MAX_SCORE = 1000
START_SCORE = 1

'''
JAPANESE_HEADER = "Japanese"
'''
KANJI_HEADER = "Kanji"
R_HEADER = "Reading"
ENGLISH_HEADER = "English"
K_SENTENCE_HEADER = "Japanese Example"
JP_SENTENCE_HEADER = "Example Reading"
ENG_SENTENCE_HEADER = "English Sentence"
L_SCORE_HEADER = "listening score"
S_SCORE_HEADER = "speaking score"
R_SCORE_HEADER = "reading score"
W_SCORE_HEADER = "writing score"

LS_AG_COlUMNS = {KANJI_HEADER: lambda x: list(x),
                ENGLISH_HEADER: lambda x: list(x),
                K_SENTENCE_HEADER: lambda x: list(x),
                JP_SENTENCE_HEADER: lambda x: list(x),
                ENG_SENTENCE_HEADER: lambda x: list(x),
                L_SCORE_HEADER: lambda x: list(x),
                S_SCORE_HEADER: lambda x: list(x),
                R_SCORE_HEADER: lambda x: list(x),
                W_SCORE_HEADER: lambda x: list(x)
                }

RW_AG_COlUMNS = {R_HEADER: lambda x: list(x),
                ENGLISH_HEADER: lambda x: list(x),
                K_SENTENCE_HEADER: lambda x: list(x),
                JP_SENTENCE_HEADER: lambda x: list(x),
                ENG_SENTENCE_HEADER: lambda x: list(x),
                L_SCORE_HEADER: lambda x: list(x),
                S_SCORE_HEADER: lambda x: list(x),
                R_SCORE_HEADER: lambda x: list(x),
                W_SCORE_HEADER: lambda x: list(x)
                }

ALL_COLUMNS = list(LS_AG_COlUMNS.keys())
ALL_COLUMNS.append(R_HEADER)
#print(len(ALL_COLUMNS))


MIN_SCORE = 7

def read_table_LS(filepath_or_buffer, delimiter="\t",encoding = "UTF-16"):
    x = read_table(filepath_or_buffer=filepath_or_buffer, delimiter=delimiter,encoding = encoding)

    print("grouping")

    x = x.groupby(R_HEADER, as_index=False).agg(LS_AG_COlUMNS)

    return x

def load_listening_dictionary(filename, sep = "\t"):
    x = read_table_LS(filepath_or_buffer=filename, delimiter=sep)
    
    dictionary = {}
    print("making dict")
    for number in range(0,MAX_SCORE):
        dictionary[number] = []
    print("populating dict")
    i = 1
    for index, row in x.iterrows():
       # print(row)
        this_score = int(max(row[L_SCORE_HEADER]))
        dictionary[this_score].append([row[KANJI_HEADER],row[R_HEADER],row[ENGLISH_HEADER],row[K_SENTENCE_HEADER],row[JP_SENTENCE_HEADER],row[ENG_SENTENCE_HEADER],row[S_SCORE_HEADER],row[R_SCORE_HEADER],row[W_SCORE_HEADER]])
        i = i + 1


    score_weights = update_weights(dictionary, i)
    return dictionary, score_weights, i

def export_listeningLibrary_to_txt(scored_dict,filename,delimiter ="\t", encoding = "UTF-16"):
    score_table = format_to_table_listening(scored_dict)    

   # print(score_table)

    #score_table = score_table.explode([KANJI_HEADER,ENGLISH_HEADER,K_SENTENCE_HEADER,JP_SENTENCE_HEADER,ENG_SENTENCE_HEADER,S_SCORE_HEADER,R_SCORE_HEADER,W_SCORE_HEADER])

    ##Let us say list_cols are the columns to be exploded
    list_cols = {KANJI_HEADER,ENGLISH_HEADER,K_SENTENCE_HEADER,JP_SENTENCE_HEADER,ENG_SENTENCE_HEADER,S_SCORE_HEADER,R_SCORE_HEADER,W_SCORE_HEADER}
    other_cols = list(set(score_table.columns) - set(list_cols))
    ##other_cols now contains all the remaining column names in the df
    ##we temporarily convert to set() to easily get the differences in 2 lists
    ##now explode the list_cols using a loop
    exploded = [score_table[col].explode() for col in list_cols]
    ##now we have long list of exploded values. Print to see the format
    ##This statement creates pairs of the exploded cols
    ##zip command is used to create the pairs
    ##dict puts it in an appropriate format from which a dataframe can be created
    ##Please print the individual outputs of each command to understand the flow
    df2 = pd.DataFrame(dict(zip(list_cols, exploded)))
    ##Now merge back the other_cols as well
    df2 = score_table[other_cols].merge(df2, how="right", left_index=True, right_index=True)
    ##lastly, re-create the original column order
    df2 = df2.loc[:, score_table.columns]

    df2.to_csv(filename, sep = delimiter,encoding = encoding,index=False)

def format_to_table_listening(scored_dictionary):
    values = {}
    i = 0
    for eachScore in scored_dictionary.keys():
        for eachCard in scored_dictionary[eachScore]:
           # print(eachCard)
            thisRow = eachCard
            thisRow.append(str(eachScore))
            values.update({i:thisRow})
            i = i + 1
    return(pd.DataFrame(values.values(),columns=[KANJI_HEADER,R_HEADER,ENGLISH_HEADER,K_SENTENCE_HEADER,JP_SENTENCE_HEADER,ENG_SENTENCE_HEADER,S_SCORE_HEADER,R_SCORE_HEADER,W_SCORE_HEADER,L_SCORE_HEADER]))

def get_card(current_score, last_score, my_scored_cards, score_weights):
   # print(current_score)
    num = 0
    #print(last_score)
    if not my_scored_cards[current_score] == []:
        if (len(my_scored_cards[current_score])>1):
            num = random.randrange(0, len(my_scored_cards[current_score])-1,1)
        else:
            num = 0
        current_card = my_scored_cards[current_score][num]
        selected = True
        
    else:#README Something wrong here
        selected = False
        
        while current_score < len(score_weights) - 1 and not selected:
            current_score = current_score + 1
            if current_score != last_score and my_scored_cards[current_score] != []:
                if len(my_scored_cards[current_score]) > 1:
                    num = random.randrange(0, len(my_scored_cards[current_score])-1,1)
                else:
                    num = 0
                current_card = my_scored_cards[current_score][num]
                selected = True
        if selected == False and my_scored_cards[START_SCORE] != []:
            if len(my_scored_cards[START_SCORE]) > 1:
                num = random.randrange(0, len(my_scored_cards[START_SCORE])-1,1)
            else:
                num = 0
            current_card = my_scored_cards[START_SCORE][num]
            current_score = START_SCORE
        elif selected == False and my_scored_cards[MAX_SCORE-1] != []:
            if len(my_scored_cards[MAX_SCORE-1]) > 1:
                num = random.randrange(0, len(my_scored_cards[MAX_SCORE-1])-1,1)
            else:
                num = 0
            current_card = my_scored_cards[MAX_SCORE-1][num]           
            current_score = MAX_SCORE-1
        elif (selected == False and last_score != 0) and my_scored_cards[0] != []:
            if len(my_scored_cards[0]) > 1:
                num = random.randrange(0, len(my_scored_cards[0])-1,1) 
            else:
                num = 0
            current_card = my_scored_cards[0][num]            
            current_score = 0
            selected = True
            #print("This is " + str(current_score) + "not" + str(last_score))
        elif selected == False and my_scored_cards[START_SCORE] != []:
            current_score = START_SCORE
            if len(my_scored_cards[START_SCORE])> 1:
                num = random.randrange(0, len(my_scored_cards[START_SCORE])-1,1)
            else:
                num = 0
            current_card = my_scored_cards[START_SCORE][num]
        elif selected == True:
            pass
        else:
            if last_score != -1:
                if len(my_scored_cards[last_score])>1:
                    num = random.randrange(0, len(my_scored_cards[last_score])-1,1)
                else:
                    num = 0
                current_card = my_scored_cards[last_score][num]
                current_score = last_score
                #print("***")
            else: #last_score = -1
                num = -1
                current_card = None
                current_score = -1
    if current_score != -1 and (current_score == last_score) and len(my_scored_cards[last_score]) == 1 and len(my_scored_cards[0]) > 0:
            if len(my_scored_cards[0]) > 1:
                num = random.randrange(0, len(my_scored_cards[0])-1,1) 
            else:
                num = 0
            current_card = my_scored_cards[0][num]            
            current_score = 0
            selected = True
    
    return current_score, current_card, num


def load_speaking_dictionary(filename, sep = "\t"):
    x = read_table_LS(filepath_or_buffer=filename, delimiter=sep)
    
    dictionary = {}

    for number in range(0,MAX_SCORE):
        dictionary[number] = []

    i = 1
    for index, row in x.iterrows():
       # print(row)
        this_score = int(max(row[S_SCORE_HEADER]))
        dictionary[this_score].append([row[KANJI_HEADER],row[R_HEADER],row[ENGLISH_HEADER],row[K_SENTENCE_HEADER],row[JP_SENTENCE_HEADER],row[ENG_SENTENCE_HEADER],row[L_SCORE_HEADER],row[R_SCORE_HEADER],row[W_SCORE_HEADER]])
        i = i + 1

    score_weights = update_weights(dictionary, i)
    return dictionary, score_weights, i

def export_speakingLibrary_to_txt(scored_dict,filename,delimiter ="\t", encoding = "UTF-16",index=False):
    score_table = format_to_table_speaking(scored_dict)    

   # print(score_table)

    #score_table = score_table.explode([KANJI_HEADER,ENGLISH_HEADER,K_SENTENCE_HEADER,JP_SENTENCE_HEADER,ENG_SENTENCE_HEADER,R_SCORE_HEADER,W_SCORE_HEADER,L_SCORE_HEADER])

    ##Let us say list_cols are the columns to be exploded
    list_cols = {KANJI_HEADER,ENGLISH_HEADER,K_SENTENCE_HEADER,JP_SENTENCE_HEADER,ENG_SENTENCE_HEADER,R_SCORE_HEADER,W_SCORE_HEADER,L_SCORE_HEADER}
    other_cols = list(set(score_table.columns) - set(list_cols))
    ##other_cols now contains all the remaining column names in the df
    ##we temporarily convert to set() to easily get the differences in 2 lists
    ##now explode the list_cols using a loop
    exploded = [score_table[col].explode() for col in list_cols]
    ##now we have long list of exploded values. Print to see the format
    ##This statement creates pairs of the exploded cols
    ##zip command is used to create the pairs
    ##dict puts it in an appropriate format from which a dataframe can be created
    ##Please print the individual outputs of each command to understand the flow
    df2 = pd.DataFrame(dict(zip(list_cols, exploded)))
    ##Now merge back the other_cols as well
    df2 = score_table[other_cols].merge(df2, how="right", left_index=True, right_index=True)
    ##lastly, re-create the original column order
    df2 = df2.loc[:, score_table.columns]


    df2.to_csv(filename, sep = delimiter,encoding = encoding,index=False)

def format_to_table_speaking(scored_dictionary):
    values = {}
    i = 0
    for eachScore in scored_dictionary.keys():
        for eachCard in scored_dictionary[eachScore]:
           # print(eachCard)
            thisRow = eachCard
            thisRow.append(str(eachScore))
            values.update({i:thisRow})
            i = i + 1
    return(pd.DataFrame(values.values(),columns=[KANJI_HEADER,R_HEADER,ENGLISH_HEADER,K_SENTENCE_HEADER,JP_SENTENCE_HEADER,ENG_SENTENCE_HEADER,L_SCORE_HEADER,R_SCORE_HEADER,W_SCORE_HEADER,S_SCORE_HEADER]))

def get_card_speaking(current_score, last_card, my_scored_cards, score_weights):
   # print(current_score)
    #print(last_score)
    num = 0
    selected= False
    if not my_scored_cards[current_score] == []:
        i = 0
        for eachCard in my_scored_cards[current_score]:
            if int(max(eachCard[-3])) > MIN_SCORE and eachCard != last_card:
                selected = True
                num = i
                current_card = eachCard
                break
            i = i + 1
    if selected==True:
        pass
    else:#README Something wrong here
        selected = False
        #print(max(my_scored_cards.keys()))
        while current_score > 0 and not selected:
            i = 0
            for eachCard in my_scored_cards[current_score]:
                if int(max(eachCard[-3])) > MIN_SCORE and eachCard != last_card:
                    selected = True
                    num = i
                    current_card = eachCard
                    break
                i = i + 1
            if selected == True:
                break
            else:
                current_score = current_score - 1
        
        if selected == False:
            while current_score < len(my_scored_cards) and not selected:
                i = 0
                for eachCard in my_scored_cards[current_score]:
                    if int(max(eachCard[-3])) > MIN_SCORE and eachCard != last_card:
                        selected = True
                        num = i
                        current_card = eachCard
                        break
                    i = i + 1
                if selected == True:
                    break
                else:
                    current_score = current_score + 1
    if selected == True:
        state = "GOOD"
    else:
        current_card = "ERROR"
        current_score = None
        state = "ERROR"
            
    return current_score, current_card, state, num



def read_table_RW(filepath_or_buffer, delimiter="\t",encoding = "UTF-16"):
    x = read_table(filepath_or_buffer=filepath_or_buffer, delimiter=delimiter,encoding = encoding)

    print("loading")

    x = x.groupby(KANJI_HEADER, as_index=False).agg(RW_AG_COlUMNS)

    return x


def load_reading_dictionary(filename, sep = "\t"):
    x = read_table_RW(filepath_or_buffer=filename, delimiter=sep)
    
    dictionary = {}

    for number in range(0,MAX_SCORE):
        dictionary[number] = []

    i = 1
    for index, row in x.iterrows():
       # print(row)
        this_score = int(max(row[R_SCORE_HEADER]))
        dictionary[this_score].append([row[KANJI_HEADER],row[R_HEADER],row[ENGLISH_HEADER],row[K_SENTENCE_HEADER],row[JP_SENTENCE_HEADER],row[ENG_SENTENCE_HEADER],row[L_SCORE_HEADER],row[S_SCORE_HEADER],row[W_SCORE_HEADER]])
        i = i + 1

    score_weights = update_weights(dictionary, i)
    return dictionary, score_weights, i

def export_readingLibrary_to_txt(scored_dict,filename,delimiter ="\t", encoding = "UTF-16",index=False):
    score_table = format_to_table_reading(scored_dict)    

   # print(score_table)

    #score_table = score_table.explode([R_HEADER,ENGLISH_HEADER,K_SENTENCE_HEADER,JP_SENTENCE_HEADER,ENG_SENTENCE_HEADER,L_SCORE_HEADER,S_SCORE_HEADER,W_SCORE_HEADER])
    ##Let us say list_cols are the columns to be exploded
    list_cols = {R_HEADER,ENGLISH_HEADER,K_SENTENCE_HEADER,JP_SENTENCE_HEADER,ENG_SENTENCE_HEADER,L_SCORE_HEADER,S_SCORE_HEADER,W_SCORE_HEADER}
    other_cols = list(set(score_table.columns) - set(list_cols))
    ##other_cols now contains all the remaining column names in the df
    ##we temporarily convert to set() to easily get the differences in 2 lists
    ##now explode the list_cols using a loop
    exploded = [score_table[col].explode() for col in list_cols]
    ##now we have long list of exploded values. Print to see the format
    ##This statement creates pairs of the exploded cols
    ##zip command is used to create the pairs
    ##dict puts it in an appropriate format from which a dataframe can be created
    ##Please print the individual outputs of each command to understand the flow
    df2 = pd.DataFrame(dict(zip(list_cols, exploded)))
    ##Now merge back the other_cols as well
    df2 = score_table[other_cols].merge(df2, how="right", left_index=True, right_index=True)
    ##lastly, re-create the original column order
    df2 = df2.loc[:, score_table.columns]

    df2.to_csv(filename, sep = delimiter,encoding = encoding,index=False)

def format_to_table_reading(scored_dictionary):
    values = {}
    i = 0
    for eachScore in scored_dictionary.keys():
        for eachCard in scored_dictionary[eachScore]:
           # print(eachCard)
            thisRow = eachCard
            thisRow.append(str(eachScore))
            values.update({i:thisRow})
            i = i + 1
    return(pd.DataFrame(values.values(),columns=[KANJI_HEADER,R_HEADER,ENGLISH_HEADER,K_SENTENCE_HEADER,JP_SENTENCE_HEADER,ENG_SENTENCE_HEADER,L_SCORE_HEADER,S_SCORE_HEADER,W_SCORE_HEADER,R_SCORE_HEADER]))

def get_card_reading(current_score, last_card, my_scored_cards, score_weights):
   # print(current_score)
    #print(last_score)
    num = 0
    selected= False
    if not my_scored_cards[current_score] == []:
        i = 0
        for eachCard in my_scored_cards[current_score]:
            if int(max(eachCard[-2])) > MIN_SCORE and eachCard != last_card:
                selected = True
                num = i
                current_card = eachCard
                break
            i = i + 1
    if selected==True:
        pass
    else:#README Something wrong here
        selected = False
        #print(max(my_scored_cards.keys()))
        while current_score > 0 and not selected:
            i = 0
            for eachCard in my_scored_cards[current_score]:
                if int(max(eachCard[-2])) > MIN_SCORE and eachCard != last_card:
                    selected = True
                    num = i
                    current_card = eachCard
                    break
                i = i + 1
            if selected == True:
                break
            else:
                current_score = current_score - 1
        
        if selected == False:
            while current_score < len(my_scored_cards) and not selected:
                i = 0
                for eachCard in my_scored_cards[current_score]:
                    if int(max(eachCard[-2])) > MIN_SCORE and eachCard != last_card:
                        selected = True
                        num = i
                        current_card = eachCard
                        break
                    i = i + 1
                if selected == True:
                    break
                else:
                    current_score = current_score + 1
    if selected == True:
        state = "GOOD"
    else:
        current_card = "ERROR"
        current_score = None
        state = "ERROR"
            
    return current_score, current_card, state, num


def load_writing_dictionary(filename, sep = "\t"):
    x = read_table_RW(filepath_or_buffer=filename, delimiter=sep)
    
    dictionary = {}

    for number in range(0,MAX_SCORE):
        dictionary[number] = []

    i = 1
    for index, row in x.iterrows():
       # print(row)
        this_score = int(max(row[W_SCORE_HEADER]))
        dictionary[this_score].append([row[KANJI_HEADER],row[R_HEADER],row[ENGLISH_HEADER],row[K_SENTENCE_HEADER],row[JP_SENTENCE_HEADER],row[ENG_SENTENCE_HEADER],row[L_SCORE_HEADER],row[S_SCORE_HEADER],row[R_SCORE_HEADER]])
        i = i + 1

    score_weights = update_weights(dictionary, i)
    return dictionary, score_weights, i

def export_writingLibrary_to_txt(scored_dict,filename,delimiter ="\t", encoding = "UTF-16",index=False):
    score_table = format_to_table_writing(scored_dict)    

   # print(score_table)

    #score_table = score_table.explode([R_HEADER,ENGLISH_HEADER,K_SENTENCE_HEADER,JP_SENTENCE_HEADER,ENG_SENTENCE_HEADER,L_SCORE_HEADER,S_SCORE_HEADER,R_SCORE_HEADER])
    ##Let us say list_cols are the columns to be exploded
    list_cols = {R_HEADER,ENGLISH_HEADER,K_SENTENCE_HEADER,JP_SENTENCE_HEADER,ENG_SENTENCE_HEADER,L_SCORE_HEADER,S_SCORE_HEADER,R_SCORE_HEADER}
    other_cols = list(set(score_table.columns) - set(list_cols))
    ##other_cols now contains all the remaining column names in the df
    ##we temporarily convert to set() to easily get the differences in 2 lists
    ##now explode the list_cols using a loop
    exploded = [score_table[col].explode() for col in list_cols]
    ##now we have long list of exploded values. Print to see the format
    ##This statement creates pairs of the exploded cols
    ##zip command is used to create the pairs
    ##dict puts it in an appropriate format from which a dataframe can be created
    ##Please print the individual outputs of each command to understand the flow
    df2 = pd.DataFrame(dict(zip(list_cols, exploded)))
    ##Now merge back the other_cols as well
    df2 = score_table[other_cols].merge(df2, how="right", left_index=True, right_index=True)
    ##lastly, re-create the original column order
    df2 = df2.loc[:, score_table.columns]

    df2.to_csv(filename, sep = delimiter,encoding = encoding,index=False)

def format_to_table_writing(scored_dictionary):
    values = {}
    i = 0
    for eachScore in scored_dictionary.keys():
        for eachCard in scored_dictionary[eachScore]:
           # print(eachCard)
            thisRow = eachCard
            thisRow.append(str(eachScore))
            values.update({i:thisRow})
            i = i + 1
    return(pd.DataFrame(values.values(),columns=[KANJI_HEADER,R_HEADER,ENGLISH_HEADER,K_SENTENCE_HEADER,JP_SENTENCE_HEADER,ENG_SENTENCE_HEADER,L_SCORE_HEADER,S_SCORE_HEADER,R_SCORE_HEADER,W_SCORE_HEADER]))

def get_card_writing(current_score, last_card, my_scored_cards, score_weights):
   # print(current_score)
    #print(last_score)
    num = 0
    selected= False
    if not my_scored_cards[current_score] == []:
        i = 0
        for eachCard in my_scored_cards[current_score]:
            if int(max(eachCard[-1])) > MIN_SCORE and eachCard != last_card:
                selected = True
                num = i
                current_card = eachCard
                break
            i = i + 1
    if selected==True:
        pass
    else:#README Something wrong here
        selected = False
        #print(max(my_scored_cards.keys()))
        while current_score > 0 and not selected:
            i = 0
            for eachCard in my_scored_cards[current_score]:
                if int(max(eachCard[-1])) > MIN_SCORE and eachCard != last_card:
                    selected = True
                    num = i
                    current_card = eachCard
                    break
                i = i + 1
            if selected == True:
                break
            else:
                current_score = current_score - 1
        
        if selected == False:
            while current_score < len(my_scored_cards) and not selected:
                i = 0
                for eachCard in my_scored_cards[current_score]:
                    if int(max(eachCard[-1])) > MIN_SCORE and eachCard != last_card:
                        selected = True
                        num = i
                        current_card = eachCard
                        break
                    i = i + 1
                if selected == True:
                    break
                else:
                    current_score = current_score + 1
    if selected == True:
        state = "GOOD"
    else:
        current_card = "ERROR"
        current_score = None
        state = "ERROR"
            
    return current_score, current_card, state, num


def update_weights(dictionary, i):
    
    score_distribution = {}
    
    score_weights = []

    for number in range(0,MAX_SCORE):
        score_distribution[number] = len(dictionary[number]) + 1

    score_distribution[0] = 1
    
    for number in range(1,MAX_SCORE):
        score_weights.append(score_distribution[number]/(number+1)/i)

    return score_weights