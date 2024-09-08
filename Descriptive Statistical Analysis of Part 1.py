import pandas as pd
import matplotlib.pyplot as plt

dataset1 = pd.read_csv('dataset1.csv')
dataset2 = pd.read_csv('dataset2.csv')

dataset1 = dataset1.sort_values(by='ID')
dataset2 = dataset2.sort_values(by='ID')

merged_data = pd.merge(dataset1, dataset2, on='ID')

merged_data.to_csv('merged_data 1and2.csv', index=False)

data = pd.read_csv('merged_data 1and2.csv')

data['Total_we'] = data[['C_we', 'G_we', 'S_we', 'T_we']].sum(axis=1)
data['Total_wk'] = data[['C_wk', 'G_wk', 'S_wk', 'T_wk']].sum(axis=1)
data['Total_time'] = data['Total_we'] + data['Total_wk']

groups = {
    'male': data[data['gender'] == 1],
    'female': data[data['gender'] == 0],
    'majority': data[data['minority'] == 0],
    'minority': data[data['minority'] == 1],
    'deprived': data[data['deprived'] == 1],
    'non-deprived': data[data['deprived'] == 0]
}

summary_list = []

for group_name, group_data in groups.items():
    count = group_data.shape[0]  # 每个类别的总人数
    summary_list.append({
        'Group': group_name,
        'Count': count,
        'Total_time': group_data['Total_time'].sum(),
        'Average_time': group_data['Total_time'].sum() / count if count != 0 else 0,
        'Total_we': group_data['Total_we'].sum(),
        'Average_we': group_data['Total_we'].sum() / count if count != 0 else 0,
        'Total_wk': group_data['Total_wk'].sum(),
        'Average_wk': group_data['Total_wk'].sum() / count if count != 0 else 0,
        'Total_C_we': group_data['C_we'].sum(),
        'Average_C_we': group_data['C_we'].sum() / count if count != 0 else 0,
        'Total_C_wk': group_data['C_wk'].sum(),
        'Average_C_wk': group_data['C_wk'].sum() / count if count != 0 else 0,
        'Total_G_we': group_data['G_we'].sum(),
        'Average_G_we': group_data['G_we'].sum() / count if count != 0 else 0,
        'Total_G_wk': group_data['G_wk'].sum(),
        'Average_G_wk': group_data['G_wk'].sum() / count if count != 0 else 0,
        'Total_S_we': group_data['S_we'].sum(),
        'Average_S_we': group_data['S_we'].sum() / count if count != 0 else 0,
        'Total_S_wk': group_data['S_wk'].sum(),
        'Average_S_wk': group_data['S_wk'].sum() / count if count != 0 else 0,
        'Total_T_we': group_data['T_we'].sum(),
        'Average_T_we': group_data['T_we'].sum() / count if count != 0 else 0,
        'Total_T_wk': group_data['T_wk'].sum(),
        'Average_T_wk': group_data['T_wk'].sum() / count if count != 0 else 0
    })

summary_df = pd.DataFrame(summary_list)

summary_df.to_excel('summary_table_with_total_time.xlsx', index=False)


# Load the data
summary_df = pd.read_excel('summary_table_with_total_time.xlsx')

# Define the plotting function
def plot_bar_chart(data, group_column, value_columns, title, xlabel, ylabel, legend_labels):
    plt.figure(figsize=(13, 6))
    x = range(len(value_columns))

    # Plot two sets of bars
    plt.bar(x, data.iloc[0][value_columns], width=0.4, label=legend_labels[0], color='#99CCFF')
    plt.bar([i + 0.4 for i in x], data.iloc[1][value_columns], width=0.4, label=legend_labels[1], color='#FFCC99')

    # Set titles and labels
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks([i + 0.2 for i in x], value_columns, rotation=45)
    plt.legend()

    # Display values on bars
    for i in x:
        plt.text(i, data.iloc[0][value_columns].values[i], round(data.iloc[0][value_columns].values[i], 2), ha='center', va='bottom')
        plt.text(i + 0.4, data.iloc[1][value_columns].values[i], round(data.iloc[1][value_columns].values[i], 2), ha='center', va='bottom')

    # Adjust layout
    plt.tight_layout()
    plt.show()

# Select data for different groups
male_female = summary_df[summary_df['Group'].isin(['male', 'female'])]
minority_majority = summary_df[summary_df['Group'].isin(['majority', 'minority'])]
deprived_non_deprived = summary_df[summary_df['Group'].isin(['deprived', 'non-deprived'])]

# Update columns to put Total_time and Average_time at the beginning
total_columns = ['Total_time', 'Total_we', 'Total_wk', 'Total_C_we', 'Total_C_wk', 'Total_G_we', 'Total_G_wk',
                 'Total_S_we', 'Total_S_wk', 'Total_T_we', 'Total_T_wk']

average_columns = ['Average_time', 'Average_we', 'Average_wk', 'Average_C_we', 'Average_C_wk', 'Average_G_we',
                   'Average_G_wk', 'Average_S_we', 'Average_S_wk', 'Average_T_we', 'Average_T_wk']

# Plot total time by gender (Male vs Female)
plot_bar_chart(male_female, 'Group', total_columns, 'Total Time by Gender', 'Time Categories', 'Total Time', ['Male', 'Female'])

# Plot average time by gender (Male vs Female)
plot_bar_chart(male_female, 'Group', average_columns, 'Average Time by Gender', 'Time Categories', 'Average Time', ['Male', 'Female'])

# Plot total time by minority status (Minority vs Majority)
plot_bar_chart(minority_majority, 'Group', total_columns, 'Total Time by Minority Status', 'Time Categories', 'Total Time', ['Majority', 'Minority'])

# Plot average time by minority status (Minority vs Majority)
plot_bar_chart(minority_majority, 'Group', average_columns, 'Average Time by Minority Status', 'Time Categories', 'Average Time', ['Majority', 'Minority'])

# Plot total time by deprivation status (Deprived vs Non-Deprived)
plot_bar_chart(deprived_non_deprived, 'Group', total_columns, 'Total Time by Deprivation Status', 'Time Categories', 'Total Time', ['Deprived', 'Non-Deprived'])

# Plot average time by deprivation status (Deprived vs Non-Deprived)
plot_bar_chart(deprived_non_deprived, 'Group', average_columns, 'Average Time by Deprivation Status', 'Time Categories', 'Average Time', ['Deprived', 'Non-Deprived'])
