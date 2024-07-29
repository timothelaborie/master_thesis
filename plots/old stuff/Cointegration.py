from __future__ import annotations
import pandas as pd ; import os ; import numpy as np ; import matplotlib.pyplot as plt ; from sklearn import linear_model
from statsmodels.tsa.vector_ar.vecm import coint_johansen ; from statsmodels.regression.linear_model import OLS
from statsmodels.tsa.adfvalues import mackinnoncrit, mackinnonp ; from statsmodels.tsa.tsatools import lagmat

main_path = r'/Users/cgrumbach/Documents/Paper - Bitcoin Pricing/Data Analysis'
if not os.path.exists(os.path.join(main_path)):
    os.makedirs(os.path.join(main_path))
df_data = pd.read_excel(os.path.join(main_path, 'Bitcoin Paper Datasheet.xlsx'), engine='openpyxl',
                        sheet_name='Co-Integration')

df_one, df_two = df_data['y1 = LOG BTC'], df_data['y2 = LOG Model'] ; df_one, df_two = df_one.dropna(), df_two.dropna()
count_row = df_one.shape[0] ; chosen_lag = 7 ; row_transition = 1554
# df_one = df_one.iloc[row_transition:] ; df_two = df_two.iloc[row_transition:] # for only after regime transition
df_one = df_one.iloc[:-(count_row - row_transition)] ; df_two = df_two.iloc[:-(count_row - row_transition)] # before

def aug_dickey_fuller(x, max_lag: int | None = None, specific_lag: int | None = None):
    """
    Augmented Dickey-Fuller test (Dickey & Fuller 1979) with no constant and no trend, with the lag indicators:
    - Akaike information criterion (AIC) (Akaike 1974).
    - Bayesian information criterion (BIC) (Schwarz 1978).
    - Ng & Perron information criterion: set lag = maxlag, and reduce lag until |t-stat| > 1.645 (Ng and Perron 1995).

    - First, the function gives all critical values for 1%, 5% and 10% significance levels (MacKinnon 2010).
    - Second, it tells which lag is preferred for AIC (Akaike 1974), BIC (Schwarz 1978) and (Ng & Perron 1995) tests.
    - Third, the function prints all AIC, BIC, t-stat and p-value (MacKinnon 1994) for all lag values that are smaller
    than max_lag, which is determined using Schwert (1989) rule of thumb.
        - If test statistic > critical values, we cannot reject the null hypothesis -> non-stationary
        - If test statistic < critical values, we can reject the null hypothesis -> stationary
    - Fourth, optionally, a specific lag value can be chosen and the function returns AIC, BIC, t-stat and p-value
    (MacKinnon 1994) for this lag value, and conclusion on the results is given.
    """
    ''' Warnings for max_lag '''
    number_observations = x.shape[0]  # 100 * (maxlag / 12) ** 4
    if max_lag is None:
        max_lag = int(12*(number_observations/100)**(1/4))
        if max_lag < 0: raise ValueError('sample size is too short to use selected regression component')
    elif max_lag > int(12*(count_row/100)**(1/4)):
        raise ValueError('max_lag is too big, it must satifies Schwert (1989) rule of thumb')
    print('max_lag is: ', max_lag)

    ''' Estimating critical values '''
    critical_values = mackinnoncrit(N=1, regression='n', nobs=number_observations)
    print("{: >20} {: >10} {: >10} {: >10}".format('significance level', '1%', '5%', '10%'))
    print("{: >20} {: >10.3f} {: >10.3f} {: >10.3f}".format('critical values', critical_values[0], critical_values[1],
                                                            critical_values[2]))

    ''' Building a datasheet of results '''
    xdiff = np.diff(x) ; xdall = lagmat(xdiff[:, None], max_lag, trim="both", original="in")
    number_observations = xdall.shape[0]
    xdall[:, 0] = x[-number_observations - 1: -1] ; xdshort = xdiff[-number_observations:]
    fullRHS = xdall ; start_lag = fullRHS.shape[1] - xdall.shape[1] + 1 ; results, t_stats = {}, {}
    for lag in range(start_lag, start_lag + max_lag + 1):
        mod_instance = OLS(xdshort, fullRHS[:, :lag], start_lag, max_lag)
        results[lag] = mod_instance.fit()
        resols = OLS(xdshort, xdall[:, : lag + 1]).fit()
        t_stats[lag] = resols.tvalues[0]

    ''' Estimating best information criterion (and corresponding lag) for AIC, BIC and Ng & Perron '''
    best_information_criterion_AIC, best_lag_AIC = min((v.aic, k) for k, v in results.items())
    print('The minimum obtained with the AIC was: ', best_information_criterion_AIC, ' at lag: ', best_lag_AIC)
    best_information_criterion_BIC, best_lag_BIC = min((v.bic, k) for k, v in results.items())
    print('The minimum obtained with the BIC was: ', best_information_criterion_BIC, ' at lag: ', best_lag_BIC)
    stop = 1.6448536269514722 ; best_lag_NgPerron = start_lag + max_lag ; best_information_criterion_NgPerron = 0
    for lag in range(start_lag + max_lag -1, start_lag, -1):
        best_information_criterion_NgPerron = t_stats[lag]
        best_lag_NgPerron = lag
        if np.abs(best_information_criterion_NgPerron) >= stop:
            break
    print('The Ng and Perron (1995) information criterion is satisfied at lag:', best_lag_NgPerron, 'with t-stat: ',
          best_information_criterion_NgPerron)

    ''' Printing prints all AIC, BIC, t-stat and p-value for all lag values that are smaller than max_lag '''
    print("{: >5} {: >15} {: >15} {: >10} {: >20}".format('lag', 'AIC', 'BIC', 't-stat', 'p-value'))
    for lag in range(start_lag, start_lag + max_lag):
        t_stat = t_stats[lag]
        pvalue = mackinnonp(t_stat, regression='n', N=1)
        print("{: >5} {: >15.3f} {: >15.3f} {: >10.3f} {: >20.10f}".format(lag, results[lag].aic, results[lag].bic,
                                                                          t_stat, pvalue))
        # plt.plot(results[lag].fittedvalues)
        # plt.show()
        # print(results[lag].summary)
    ''' Returns value when specific lag is given'''
    if specific_lag is not None:
        if specific_lag < 0:
            raise ValueError('specific_lag cannot be negative')
        elif specific_lag > int(12 * (count_row / 100) ** (1 / 4)):
            raise ValueError('specific_lag is too big, it must satifies Schwert (1989) criterion')
        t_stat_specific = t_stats[specific_lag]
        pvalue_specific = mackinnonp(t_stat_specific, regression='n', N=1)
        print("For the specific lag value you entered:")
        print("{: >5} {: >15} {: >15} {: >10} {: >20}".format('lag', 'AIC', 'BIC', 't-stat', 'p-value'))
        print("{: >5} {: >15.3f} {: >15.3f} {: >10.3f} {: >20.10f}".format(specific_lag, results[specific_lag].aic,
                                                                          results[specific_lag].bic,
                                                                          t_stat_specific, pvalue_specific))
        if t_stat_specific < critical_values[2]:
            if t_stat_specific < critical_values[1]:
                if t_stat_specific < critical_values[0]:
                    print('Reject null hypothesis at a significance level of 1%, process is stationary')
                else:
                    print('Reject null hypothesis at a significance level of 5%, process is stationary')
            else:
                print('Reject null hypothesis at a significance level of 10%, process is stationary')
        else:
            print('Cannot reject null hypothesis, process is non-stationary')
        return specific_lag, results[specific_lag].aic, results[specific_lag].bic, t_stat_specific, pvalue_specific

''' Proving that data are non-stationary with ADF '''
print('\n ADF FOR BITCOIN PRICE TO TEST STATIONARITY')
adf_one = aug_dickey_fuller(df_one, specific_lag=chosen_lag)
print('\n ADF FOR MINING COSTS TO TEST STATIONARITY')
adf_two = aug_dickey_fuller(df_two, specific_lag=chosen_lag)

''' Engle-Granger cointegration test using ADF test '''
print('\n ENGLE-GRANGER TEST')
# 1st Step: regression for determining alpha, beta and spread
regression = linear_model.LinearRegression()
x_constant = pd.concat([df_two, pd.Series([1]*len(df_two), index=df_two.index)], axis=1)
regression.fit(x_constant.values, df_one.values)
beta, alpha = regression.coef_[0], regression.intercept_  ; print('beta is', beta, 'and alpha is', alpha)

# 2nd Step: check if the spread is stationary with ADF
spread = df_one - beta*df_two - alpha
spread.plot(figsize =(15,10)) ; plt.ylabel('spread') ; plt.show()
adf = aug_dickey_fuller(spread, specific_lag=chosen_lag)

''' Johansen test for cointegration '''
print('\n JOHANSEN TEST: 1st row is r=0, 2nd row is r<=1')
def johansen(res):
    """
    Johansen Test (Johansen 1991, 1995) for co-integration.
    - Null hypothesis (no cointegration, rank r=0) rejected if max_eig_stat or trace_stat bigger than critical values.
    - Alternative hypothesis (cointegration, r<=1) accepted if max_eig_stat or trace_stat smaller than critical values.
    - If you reject both r = 0 and r <= 1 that means r = 2, meaning the two series are stationary, so no cointegration.
    https://www.statsmodels.org/dev/generated/statsmodels.tsa.vector_ar.vecm.coint_johansen.html
    """
    output = pd.DataFrame([res.lr2, res.lr1], index=['max_eig_stat',"trace_stat"]) ; print(output.T)
    print("Critical values(90%, 95%, 99%) of max_eig_stat (r=0 then r<=1): ", res.cvm[0], res.cvm[1])
    print("Critical values(90%, 95%, 99%) of trace_stat (r=0 then r<=1): ", res.cvt[0], res.cvt[1])
df_johansen = pd.DataFrame({'y':df_one, 'x':df_two})
johansen_result = coint_johansen(df_johansen, det_order=-1, k_ar_diff=chosen_lag) ; johansen(johansen_result)