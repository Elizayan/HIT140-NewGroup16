import statistics as st
import scipy.stats as stats
import numpy as np
import scipy as sp
import pandas as pd
import math 
import matplotlib.pyplot as plt


#read csv into dataframe
df1 = pd.read_csv("dataset1.csv")
df2 = pd.read_csv("dataset2.csv")
df3 = pd.read_csv("dataset3.csv")

merged_df = pd.merge(df1, df2, on ="ID")
merged_df = pd.merge(merged_df, df3, on ="ID")

merged_df.to_csv("merged_dataset.csv", index=False)

# Load the merged dataset
file_path = 'merged_dataset.csv'
data = pd.read_csv(file_path)

# Calculate average weekly screen time
data['avg_screen_time'] = (data['C_wk'] + data['C_we'] + data['G_wk'] + data['G_we'] + data['S_wk'] + data['S_we'] + data['T_wk'] + data['T_we']) / 8

# List of well-being columns
well_being_columns = ['Optm', 'Usef', 'Relx', 'Intp', 'Engs', 'Dealpr', 'Thcklr', 'Goodme', 'Clsep', 'Conf', 'Mkmind', 'Loved', 'Intthg', 'Cheer']

# Calculate average well-being score for each respondent
data['avg_well_being'] = data[well_being_columns].mean(axis=1)

#devide data into male and female groups
male_data = data[data['gender'] == 1]
female_data = data[data['gender'] == 0]

# Calculate average screen time for males and females
average_screen_time_male = male_data['avg_screen_time'].mean()
average_screen_time_female = female_data['avg_screen_time'].mean()

# Calculate average well-being for males and females
average_well_being_male = male_data['avg_well_being'].mean()
average_well_being_female = female_data['avg_well_being'].mean()

# Print the average screen time result for male and female
print("Average Screen Time for Males:", average_screen_time_male)
print("Average Screen Time for Females:", average_screen_time_female)

# Print the average well-being result for male and female
print("Average Well-Being Score for Males:", average_well_being_male)
print("Average Well-Being Score for Females:", average_well_being_female)



# Conduct a Hypotheses test:
# Hypotheses Test according average screen time and well-being scores for male and female
# Null Hypotheses (H₀) : No significant effect of screen time on well-being
# Alternative Hypotheses (H₁) : Screen time significantly affects well-being
# Standerd p-value is: alpha = 0.05
# We will use a two-sample t-test to compare the means between the two groups


# Data for screen time and well-being
categories = ['Average Screen Time', 'Average Well-Being']
male_averages = [average_screen_time_male, average_well_being_male]
female_averages = [average_screen_time_female, average_well_being_female]

# Set a threshold for high and low screen time
screen_time_threshold = data['avg_screen_time'].median()

# Divide the male group into high and low screen time based on the threshold
male_high_screen_time = male_data[male_data['avg_screen_time'] > screen_time_threshold]['avg_well_being']
male_low_screen_time = male_data[male_data['avg_screen_time'] <= screen_time_threshold]['avg_well_being']

# Divide the female group into high and low screen time based on the threshold
female_high_screen_time = female_data[female_data['avg_screen_time'] > screen_time_threshold]['avg_well_being']
female_low_screen_time = female_data[female_data['avg_screen_time'] <= screen_time_threshold]['avg_well_being']

# Perform t-test for males 
t_stat_male, p_value_male = stats.ttest_ind(male_high_screen_time, male_low_screen_time)
print(f"T-test results for males: T-statistic = {t_stat_male}, P-value = {p_value_male}")

# Perform t-test for females 
t_stat_female, p_value_female = stats.ttest_ind(female_high_screen_time, female_low_screen_time)
print(f"T-test results for females: T-statistic = {t_stat_female}, P-value = {p_value_female}")

# The p-values
alpha = 0.05
if p_value_male < alpha:
    print("For males, reject the null hypothesis: Screen time significantly affects well-being.")
else:
    print("For males, fail to reject the null hypothesis: No significant effect of screen time on well-being.")

if p_value_female < alpha:
    print("For females, reject the null hypothesis: Screen time significantly affects well-being.")
else:
    print("For females, fail to reject the null hypothesis: No significant effect of screen time on well-being.")

# Showing the graph of average well-being for high and low screen time

# Data for plotting: average well-being for high and low screen time
male_high_avg_well_being = male_high_screen_time.mean()
male_low_avg_well_being = male_low_screen_time.mean()

female_high_avg_well_being = female_high_screen_time.mean()
female_low_avg_well_being = female_low_screen_time.mean()

categories = ['High Screen Time', 'Low Screen Time']

# Data for males and females
male_averages = [male_high_avg_well_being, male_low_avg_well_being]
female_averages = [female_high_avg_well_being, female_low_avg_well_being]


fig, ax = plt.subplots(figsize=(6, 6))

# Bar width
bar_width = 0.25
index = np.arange(len(categories))

# Plot bars for males and females
bars_male = plt.bar(index, male_averages, bar_width, label='Males', color='blue')
bars_female = plt.bar(index + bar_width, female_averages, bar_width, label='Females', color='pink')

# Add labels and title
plt.xlabel('Screen Time Categories')
plt.ylabel('Average Well-Being Scores')
plt.title('Average Well-Being by Gender and Screen Time')
plt.xticks(index + bar_width / 2, categories)
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()



    

    