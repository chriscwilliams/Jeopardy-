import pandas as pd
import datetime

pd.set_option('display.max_colwidth', -1)

dataset = pd.read_csv('jeopardy.csv')

# Rename Columns in dataset and remove space before column names add underscore to enable dot notation access as well as bracket notation
dataset = dataset.rename(columns={
  'Show Number': 'show_number',
  ' Air Date': 'air_date',
  ' Round': 'round',
  ' Category': 'category',
  ' Value': 'value',
  ' Question': 'question',
  ' Answer': 'answer'
})

# Function that filers the dataset for questions that contains all of the words in a list of words
def word_filter(data, lst):
  return data.loc[data.question.apply(
    lambda x: all(word.lower() in x.lower() for word in lst)
  )]

# Convert air_date column to datetime format
dataset.air_date = pd.to_datetime(dataset.air_date)

# Remove the $ and comma in the value column and then convert it to numeric
dataset.value = dataset.value.apply(lambda x: x.replace('$', ''))
dataset.value = dataset.value.apply(lambda x: x.replace(',', ''))
dataset.value = dataset.value.apply(lambda x: x if x != 'None' else 0)
dataset.value = pd.to_numeric(dataset.value)

# Number of unique answers.. I had trouble with this function so I got help from the codecademy solution :/
def unique_answers(data, lst):
  filtered = word_filter(data, lst)
  results = filtered.groupby('answer').value.count().reset_index()
  return results.sort_values(by='value',ascending=False)

# Questions about computers from 90s vs 2000s

# Filter by word 'computer'
cpu_questions = word_filter(dataset, ['Computer'])
# Select rows between 1990 and 1999
cpu_90s = cpu_questions[(cpu_questions.air_date > datetime.datetime(1900, 1, 1)) & (cpu_questions.air_date < datetime.datetime(1999, 12, 31))]
# Select rows after 1999
cpu_2000s = cpu_questions[(cpu_questions.air_date > datetime.datetime(2000, 1, 1))]

# Answer to the question about how many questions about computers there were in the 90s vs 2000s
print('During the 1990s there were {0} questions about computers and during the 2000s there were {1} questions about computers.'.format(len(cpu_90s), len(cpu_2000s)))

# View Dataset and columns
print(dataset.columns)
print(dataset.dtypes)