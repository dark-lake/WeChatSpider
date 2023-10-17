import pandas as pd

data = pd.read_csv("dainlidashuju.csv",encoding='utf-8',error_bad_lines=False)
value = data[['title', 'link']]
value.drop_duplicates(subset=['title'],keep='first', inplace=True)
name = ['title', 'link']
test = pd.DataFrame(columns=name, data=value)
test.to_csv("output.csv", mode='a', encoding='utf-8',index=False)