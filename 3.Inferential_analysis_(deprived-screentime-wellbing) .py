import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt

# read datasets2,datasets3
df_datasets1 = pd.read_csv('dataset1.csv')
df_datasets2 = pd.read_csv('dataset2.csv')
df_datasets3 = pd.read_csv('dataset3.csv')

# Calculate the sum of each student's screen time
df_datasets2['Total_Screentime'] = df_datasets2[['C_we','C_wk','G_wk','G_we','S_we','S_wk','T_we','T_wk']].sum(axis=1)

# compute mean of the sample
average_total_screentime = round(df_datasets2['Total_Screentime'].mean(),2)

# add average_total_screentime column
df_datasets2['Average_Total_Screentime'] = average_total_screentime
print("DataFrame with Average Total Screentime:")
print(df_datasets2.head())

# Extract the ID column, Total_Screentime and Average_Total_Screentime columns to a new dataframe
screen_time_sample_df = df_datasets2[['ID', 'Total_Screentime', 'Average_Total_Screentime']]

# Save as a new CSV file named ‘Screen Usage Sample Form.csv’.
screen_time_sample_df.to_csv('Screen Usage Sample Form.csv', index=False)

# Display the first few rows of the newly created dataframe
print(screen_time_sample_df.head())

# Merge screen usage sample and datasets 3 group by ID
df_screen_wellbeing = pd.merge(df_datasets3, screen_time_sample_df, on='ID', how='inner')
df_screen_wellbeing.to_csv('df_screen_wellbeing.csv', index=False)


# read screen_wellbeing file
df_screen_wellbeing = pd.read_csv('df_screen_wellbeing.csv')

# split DataFrame into two subsets:
# Separate samples that lager than the mean of the screen use time and less than the mean：
df_moretime_sample = df_screen_wellbeing[df_screen_wellbeing['Total_Screentime'] > df_screen_wellbeing['Average_Total_Screentime']]
df_lesstime_sample = df_screen_wellbeing[df_screen_wellbeing['Total_Screentime'] < df_screen_wellbeing['Average_Total_Screentime']]

print(df_moretime_sample.head())
print(df_lesstime_sample.head())
print(len(df_moretime_sample))
print(len(df_lesstime_sample))

# Read the file and Create copies
df_moretime_sample = df_screen_wellbeing[df_screen_wellbeing['Total_Screentime'] > df_screen_wellbeing['Average_Total_Screentime']].copy()
df_lesstime_sample = df_screen_wellbeing[df_screen_wellbeing['Total_Screentime'] < df_screen_wellbeing['Average_Total_Screentime']].copy()

# Calculate the total well-being index
wellbeing_columns = ['Optm', 'Usef', 'Relx', 'Intp', 'Engs', 'Dealpr', 'Thcklr', 'Goodme', 'Clsep', 'Conf', 'Mkmind', 'Loved', 'Intthg', 'Cheer']
df_moretime_sample['total_wellbeing'] = df_moretime_sample[wellbeing_columns].sum(axis=1)
df_lesstime_sample['total_wellbeing'] = df_lesstime_sample[wellbeing_columns].sum(axis=1)

# select relevant column from each Dataframe
moretime_sample = df_moretime_sample['total_wellbeing'].to_numpy()
lesstime_sample = df_lesstime_sample['total_wellbeing'].to_numpy()

# Calculate the mean, standard deviation and sample size for the more time sample and the less time sample.
print("\nComputing basic statistics of samples ...")

# the basic statistics of moretime_sample
x_bar1 = st.tmean(moretime_sample)
s1 = st.tstd(moretime_sample)
n1 = len(moretime_sample)
print("Statistics of moretime samples: %.2f (mean), %.2f (std.), %d (n)" % (x_bar1, s1, n1))

# the basic  statistic of lesstime_sample
x_bar2 = st.tmean(lesstime_sample)
s2 = st.tstd(lesstime_sample)
n2 = len(lesstime_sample)
print("Statistics of lesstime samples: %.2f (mean), %.2f (std.), %d (n)" % (x_bar2, s2, n2))

# perform two-sample t-test
# null hypothesis: mean of moretime sample =mean of lesstime sample
# alternative hyppthesis : mean of moretime sample is greater than mean of lesstime sample
t_stats, p_val = st.ttest_ind_from_stats(x_bar1,s1,n1,x_bar2,s2,n2,equal_var=False, alternative='less')
print("\nComputing t*...")
print("\tt-statistics: %.2f"%t_stats)

print("\nComputing p*...")
print("\tp-value: %.4f"%p_val)

print("\n Conclusion:")
if p_val < 0.05:
    print("\t We reject the null hypothesis.")
else:
    print("\t We accept the null hypothesis.")

# Conclusion ： Children with long screen time use were significantly less happy than students with short screen time use.

# further study with  high deprived screen time's wellbeing sample and low deprived screen time's wellbeing sample
# Merge df1 and screen_time_sample group by ID
df_screen_wellbeing = pd.merge(df_datasets1, df_screen_wellbeing, on='ID', how='inner')
print(df_screen_wellbeing.head())
df_screen_wellbeing.to_csv('screen_wellbeing.csv', index=False)

# Extracts the total_screentime of the high deprived sample and low deprived sample
high_deprived_sample_time = df_screen_wellbeing[df_screen_wellbeing['deprived'] == 1]['Total_Screentime']
low_deprived_sample_time = df_screen_wellbeing[df_screen_wellbeing['deprived'] == 0]['Total_Screentime']

# compute the mean_screentime of the high deprived sample and low deprived sample
average_h_d_screentime = round(high_deprived_sample_time.mean(), 2)
average_l_d_screen_time = round(df_datasets2['Total_Screentime'].mean(),2)


# split the higher_screen_time and lower_screen_time sample of high deprived sample
df_higher_hd_sample = df_screen_wellbeing[(df_screen_wellbeing['Total_Screentime'] > average_h_d_screentime) & (df_screen_wellbeing['deprived'] == 1)]
df_lower_hd_sample = df_screen_wellbeing[(df_screen_wellbeing['Total_Screentime'] <= average_h_d_screentime) & (df_screen_wellbeing['deprived'] == 1)]

# create copy file
df_higher_hd_sample = df_higher_hd_sample.copy()
df_lower_hd_sample = df_lower_hd_sample.copy()

# compute total wellbeing of higher_screen_time and lower_screen_time sample of high deprived sample
df_hd_w = ['Optm', 'Usef', 'Relx', 'Intp', 'Engs', 'Dealpr', 'Thcklr', 'Goodme', 'Clsep', 'Conf', 'Mkmind', 'Loved', 'Intthg', 'Cheer']
df_higher_hd_sample['total_wellbeing'] = df_higher_hd_sample[df_hd_w].sum(axis=1)
df_lower_hd_sample ['total_wellbeing'] = df_lower_hd_sample[df_hd_w].sum(axis=1)

# select relevant column from each Dataframe
df_ht_hd_sample = df_higher_hd_sample['total_wellbeing'].to_numpy()
df_lt_hd_sample = df_lower_hd_sample['total_wellbeing'].to_numpy()

# Calculate the mean, standard deviation and sample size higher_screen_time and lower_screen_time sample of high deprived sample
print("\nComputing basic statistics of samples ...")

# the basic statistics of higer screen time of high deprived sample
x_ht_hd = st.tmean(df_ht_hd_sample)
s_ht_hd = st.tstd(df_ht_hd_sample)
n_ht_hd = len(df_ht_hd_sample)
print("Statistics of higer time samples（HD）: %.2f (mean), %.2f (std.), %d (n)" % (x_ht_hd, s_ht_hd, n_ht_hd))

#the basic statistics of lower screen time of high deprived sample
x_lt_hd = st.tmean(df_lt_hd_sample)
s_lt_hd = st.tstd(df_lt_hd_sample)
n_lt_hd = len(df_lt_hd_sample)
print("Statistics of lower time samples (HD): %.2f (mean), %.2f (std.), %d (n)" % (x_lt_hd, s_lt_hd, n_lt_hd))

# perform two-sample t-test
# null hypothesis: mean of  higer screen time of high deprived sample =mean of lower screen time of high deprived sample
# alternative hyppthesis : mean of lower screen time of high deprived sample  is less than mean of lower screen time of high deprived sample
t_stats, p_val = st.ttest_ind_from_stats(x_ht_hd,s_ht_hd, n_ht_hd,x_lt_hd, s_lt_hd, n_lt_hd,equal_var=False, alternative='less')
print("\nComputing t*...")
print("\tt-statistics: %.2f"%t_stats)

print("\nComputing p*...")
print("\tp-value: %.4f"%p_val)

print("\n Conclusion:")
if p_val < 0.05:
    print("\t We reject the null hypothesis.")
else:
    print("\t We accept the null hypothesis.")

# Conclusion: Children and adolescents who use high screen time are less happy than those who use low screen time in high deprived area.

# split the higher_screen_time and lower_screen_time sample of low deprived sample
df_higher_ld_sample = df_screen_wellbeing[(df_screen_wellbeing['Total_Screentime'] > average_l_d_screen_time) & (df_screen_wellbeing['deprived'] == 0)]
df_lower_ld_sample = df_screen_wellbeing[(df_screen_wellbeing['Total_Screentime'] <= average_l_d_screen_time) & (df_screen_wellbeing['deprived'] == 0)]

#create copy file
df_higher_ld_sample = df_higher_ld_sample.copy()
df_lower_ld_sample = df_lower_ld_sample.copy()

# compute total wellbeing of higher_screen_time and lower_screen_time sample of low deprived sample
df_ld_w = ['Optm', 'Usef', 'Relx', 'Intp', 'Engs', 'Dealpr', 'Thcklr', 'Goodme', 'Clsep', 'Conf', 'Mkmind', 'Loved', 'Intthg', 'Cheer']
df_higher_ld_sample['total_wellbeing'] = df_higher_ld_sample[df_ld_w].sum(axis=1)
df_lower_ld_sample ['total_wellbeing'] = df_lower_ld_sample[df_ld_w].sum(axis=1)

# select relevant column from each Dataframe
df_ht_ld_sample = df_higher_ld_sample['total_wellbeing'].to_numpy()
df_lt_ld_sample = df_lower_ld_sample['total_wellbeing'].to_numpy()

# Calculate the mean, standard deviation and sample size higher_screen_time and lower_screen_time sample of low deprived sample
print("\nComputing basic statistics of samples ...")

# the basic statistics of higer screen time of low deprived sample
x_ht_ld = st.tmean(df_ht_ld_sample)
s_ht_ld = st.tstd(df_ht_ld_sample)
n_ht_ld = len(df_ht_ld_sample)
print("Statistics of higher time samples（LD）: %.2f (mean), %.2f (std.), %d (n)" % (x_ht_ld, s_ht_ld, n_ht_ld))

#the basic statistics of lower screen time of low deprived sample
x_lt_ld = st.tmean(df_lt_ld_sample)
s_lt_ld = st.tstd(df_lt_ld_sample)
n_lt_ld = len(df_lt_ld_sample)
print("Statistics of lower time samples (lD): %.2f (mean), %.2f (std.), %d (n)" % (x_lt_ld,s_lt_ld,n_lt_ld))

# perform two-sample t-test
# null hypothesis: mean of  higer screen time of low deprived sample =mean of lower screen time of low deprived sample
# alternative hyppthesis : mean of lower screen time of low deprived sample  is less than mean of lower screen time of low deprived sample
t_stats, p_val = st.ttest_ind_from_stats(x_ht_ld, s_ht_ld, n_ht_ld,x_lt_ld,s_lt_ld,n_lt_ld,equal_var=False, alternative='less')
print("\nComputing t*...")
print("\tt-statistics: %.2f"%t_stats)

print("\nComputing p*...")
print("\tp-value: %.4f"%p_val)

print("\n Conclusion:")
if p_val < 0.05:
    print("\t We reject the null hypothesis.")
else:
    print("\t We accept the null hypothesis.")

# Conclusion: Children and adolescents who use high screen time are less happy than those who use low screen time in low deprived area.



# gragh part
# mean of each wellbeing score of higher screen time in high deprived group，mean of each wellbeing score of lower screen time in high deprived group
average_wellbeing_score_ht_hd = df_higher_hd_sample[df_hd_w].mean(axis=1)
overall_avg_wellbeing_ht_hd = average_wellbeing_score_ht_hd.mean()

average_wellbeing_score_lt_hd = df_lower_hd_sample[df_hd_w].mean(axis=1)
overall_avg_wellbeing_lt_hd = average_wellbeing_score_lt_hd.mean()

# mean of each wellbeing score of higher screen time in high deprived group，mean of each wellbeing score of lower screen time in low deprived group
average_wellbeing_score_ht_ld = df_higher_ld_sample[df_ld_w].mean()
overall_avg_wellbeing_ht_ld = average_wellbeing_score_ht_ld.mean()

average_wellbeing_score_lt_ld = df_lower_ld_sample[df_ld_w].mean()
overall_avg_wellbeing_lt_ld = average_wellbeing_score_lt_ld.mean()

# first chart： average of total wellbeing value
plt.figure(figsize=(8, 6))

group_labels = ['High  Screen \nTime(HD)', 'Low Screen  \nTime(HD)','High  \nScreen Time(LD)', 'Low  \nScreen Time(LD)']
total_values = [x_ht_hd,x_lt_hd,x_ht_ld,x_lt_ld]  # The average of total wellbeing

bars_total = plt.bar(group_labels, total_values, color=['blue', 'orange'])
plt.title('Total Values by Screen Time and Deprivation Level')
plt.ylabel('Total Wellbeing Score')
plt.ylim([40, 50])

# mark values
for bar in bars_total:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2., height, f'{height:.2f}', ha='center', va='bottom')

# second chart ：average of each wellbeing score
# set labels and means
group_labels = ['High Screen \nTime(HD)', 'Low Screen \nTime(HD)','High Screen \nTime(LD)', 'Low Screen \nTime(LD)']
means = [ overall_avg_wellbeing_ht_hd, overall_avg_wellbeing_lt_hd,overall_avg_wellbeing_ht_ld, overall_avg_wellbeing_lt_ld]
plt.figure(figsize=(8, 6))
bars = plt.bar(group_labels, means, color=['red', 'green','red','green'])

plt.ylim([1, 4])

# show the statistics
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2., height, f'{height:.2f}', ha='center', va='bottom')

# set title and lable
plt.ylabel('Average Wellbeing Score')
plt.title('Average Wellbeing by Screen Time Groups')
plt.show()




