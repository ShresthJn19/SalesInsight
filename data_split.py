import pandas as pd

# Load your dataset
data = pd.read_csv('Amazon Sale Report.csv')

# split data into 4 parts with 25,000 rows each
part_1 = data.iloc[:25000]
part_2 = data.iloc[25000:50000]
part_3 = data.iloc[50000:75000]
part_4 = data.iloc[75000:100000]

# save each part as a separate file
part_1.to_csv('Report_P1.csv', index=False)
part_2.to_csv('Report_P2.csv', index=False)
part_3.to_csv('Report_P3.csv', index=False)
part_4.to_csv('Report_P4.csv', index=False)

print("Dataset split into 4 parts with 25,000 rows each.")