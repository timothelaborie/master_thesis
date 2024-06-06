from __future__ import annotations
import pandas as pd ; import os ; import seaborn as sns ; from scipy import stats

main_path = r'/Users/cgrumbach/Documents/Paper - Bitcoin Pricing/Data Analysis'
if not os.path.exists(os.path.join(main_path)):
    os.makedirs(os.path.join(main_path))

df_data = pd.read_excel(os.path.join(main_path, 'Bitcoin Paper Datasheet.xlsx'), engine='openpyxl',
                        sheet_name='Correlation')
df_one, df_two = df_data['Month LOG BTC Return'], df_data['Month LOG Model Return']
df_one, df_two = df_one.dropna(), df_two.dropna()

''' Pearson correlation assumes the data is normally or symmetrically distributed, so we cannot use it.
However, Spearman does not make any assumption on the distribution of the data '''
''' Spearman test: -1, +1: a perfect negative/positive correlation between two variables, 0 no correlation
statistic: +- 0.1 to 0.3 means weak strength of the relationship
Null hypothesis is that two sets of data are linearly uncorrelated --> rejected (i.e. samples are correlated) if p<0.05 '''

spearman_test = stats.spearmanr(df_one, df_two)
print('Spearman test', spearman_test.statistic, spearman_test.pvalue)

''' Shapiro-Wilk test:  when the p-value is less than or equal to 0.05 (assuming a 95% confidence level), 
we reject the null hypothesis that the data was drawn from a normal distribution --> data not normal distribution'''
df_one, df_two = df_data['Log BTC Return'], df_data['LOG Model Return'] ; df_one, df_two = df_one.dropna(), df_two.dropna()
shapiro_test_one = stats.shapiro(df_one) ; shapiro_test_two = stats.shapiro(df_two)
print('Bitcoin log daily returns Shapiro-Wilk test:',shapiro_test_one.statistic, shapiro_test_one.pvalue)
print('mining log daily returns Shapiro-Wilk test:', shapiro_test_two.statistic, shapiro_test_two.pvalue)

# s = np.random.normal(0, 0.1, 1000)
# shapiro_test_one = stats.shapiro(s)
# print(shapiro_test_one)

# plt.hist(df_one, bins=100)
# plt.gca().set(title='Frequency Histogram', ylabel='Frequency');
# plt.show()
#
# plt.hist(df_two, bins=100)
# plt.gca().set(title='Frequency Histogram', ylabel='Frequency');
# plt.show()