import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from scipy.stats import norm, t

plt.style.use('ggplot')
MC_SIMS = 1000000
LAST_N_DAYS = 1500
INITIAL_PORT_VALUE = 10000000

amd_df = pd.read_csv('Data/AMD.csv', index_col=0)  # reading in stock data
brk_df = pd.read_csv('Data/BRK.B.csv', index_col=0)
spy_df = pd.read_csv('Data/SPY.csv', index_col=0)
nflx_df = pd.read_csv('Data/NFLX.csv', index_col=0)

# Calculating log returns
amd_df['Log Returns'] = np.log(amd_df['Adjusted Close']) - np.log(amd_df['Adjusted Close'].shift(1))
brk_df['Log Returns'] = np.log(brk_df['Adjusted Close']) - np.log(brk_df['Adjusted Close'].shift(1))
spy_df['Log Returns'] = np.log(spy_df['Adjusted Close']) - np.log(spy_df['Adjusted Close'].shift(1))
nflx_df['Log Returns'] = np.log(nflx_df['Adjusted Close']) - np.log(nflx_df['Adjusted Close'].shift(1))

# Cleaning dataset
amd_df.drop(columns=['Open', 'High', 'Low', 'Close', 'Volume',
                     'Dividend Amount', 'Split Coefficient'], inplace=True)
amd_df.drop(amd_df.tail(1).index, inplace=True)
pd.to_datetime(amd_df.index)
amd_df = amd_df.tail(LAST_N_DAYS)

brk_df.drop(columns=['Open', 'High', 'Low', 'Close', 'Volume',
                     'Dividend Amount', 'Split Coefficient'], inplace=True)
pd.to_datetime(brk_df.index)
brk_df = brk_df.tail(LAST_N_DAYS)

spy_df.drop(columns=['Open', 'High', 'Low', 'Close', 'Volume',
                     'Dividend Amount', 'Split Coefficient'], inplace=True)
pd.to_datetime(spy_df.index)
spy_df = spy_df.tail(LAST_N_DAYS)

nflx_df.drop(columns=['Open', 'High', 'Low', 'Close', 'Volume',
                      'Dividend Amount', 'Split Coefficient'], inplace=True)
pd.to_datetime(nflx_df.index)
nflx_df = nflx_df.tail(LAST_N_DAYS)


def plot_amd_returns():
    # To Do: graph prices
    # Plotting log returns over time

    fig1, ax1 = plt.subplots()
    # ax1.plot(amd_df.index, amd_df['Log Returns'])
    ax1.plot(amd_df.index, amd_df['Adjusted Close'])
    ax1.xaxis.set_major_locator(plt.MaxNLocator(50))
    ax1.set_xlim(amd_df.index.min(), amd_df.index.max())
    fig1.autofmt_xdate()

    fig1.suptitle('AMD', fontsize=16, y=0.92)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Share Price')

    plt.show()


def calculate_loss_stats_amd():
    losses_array = np.array(amd_df['Log Returns']*-INITIAL_PORT_VALUE)
    losses_array = losses_array[len(losses_array)-252:]  # using last years worth of data

    # historical approach
    historical_var = np.quantile(losses_array, [0.95, 0.99])
    print(f'The historical one year 95% VaR for AMD is ${round(historical_var[0], 2)}')
    print(f'The historical one year 99% VaR for AMD is ${round(historical_var[1], 2)}')
    print("==================================================================")

    # parametric approach (Gaussian)
    mu = amd_df['Log Returns'].tail(252).mean()
    sigma = amd_df['Log Returns'].tail(252).std()
    varnorm95 = (-INITIAL_PORT_VALUE*mu) + (INITIAL_PORT_VALUE*sigma) * norm.ppf(0.95)
    varnorm99 = (-INITIAL_PORT_VALUE*mu) + (INITIAL_PORT_VALUE*sigma) * norm.ppf(0.99)
    print(f'The normal parametric one year 95% VaR for AMD is ${round(varnorm95, 2)}')
    print(f'The normal parametric one year 99% VaR for AMD is ${round(varnorm99, 2)}')
    print("==================================================================")

    # parametric approach (t-student)
    nu = 4
    vart95 = (-INITIAL_PORT_VALUE*mu) + (INITIAL_PORT_VALUE*sigma) * np.sqrt((nu-2) / nu) * t.ppf(0.95, nu)
    vart99 = (-INITIAL_PORT_VALUE*mu) + (INITIAL_PORT_VALUE*sigma) * np.sqrt((nu-2) / nu) * t.ppf(0.99, nu)
    print(f'The t-student parametric one year 95% VaR for AMD is ${round(vart95, 2)}')
    print(f'The t-student parametric one year 99% VaR for AMD is ${round(vart99, 2)}')
    print("==================================================================")

    # monte-carlo method (Gaussian)
    normal_gen_losses_array = np.random.normal(-INITIAL_PORT_VALUE*mu, INITIAL_PORT_VALUE*sigma, MC_SIMS)
    var_norm_mc = np.quantile(normal_gen_losses_array, [0.95, 0.99])
    print(f'The MC normal estimated one year 95% VaR for AMD is ${round(var_norm_mc[0], 2)}')
    print(f'The MC normal estimated one year 99% VaR for AMD is ${round(var_norm_mc[1], 2)}')
    print("==================================================================")

    # monte-carlo method (t-student)
    t_gen_losses_array = (-INITIAL_PORT_VALUE*mu) + (INITIAL_PORT_VALUE*sigma) * np.sqrt((nu-2)/nu) * np.random.standard_t(nu, size=MC_SIMS)
    var_t_mc = np.quantile(t_gen_losses_array, [0.95, 0.99])
    print(f'The MC t-student estimated one year 95% VaR for AMD is ${round(var_t_mc[0], 2)}')
    print(f'The MC t-student estimated one year 99% VaR for AMD is ${round(var_t_mc[1], 2)}')
    print("==================================================================")

    # ES using historical method
    es95_array = losses_array > historical_var[0]
    es99_array = losses_array > historical_var[1]
    es95_hist = sum(losses_array * es95_array) / sum(es95_array)
    es99_hist = sum(losses_array * es99_array) / sum(es99_array)
    print(f'The historical one year 95% ES for AMD is ${round(es95_hist, 2)}')
    print(f'The historical one year 99% ES for AMD is ${round(es99_hist, 2)}')
    print("==================================================================")

    # ES using parametric approach (Gaussian)
    es95_normal = (-INITIAL_PORT_VALUE*mu) + ((INITIAL_PORT_VALUE*sigma*norm.pdf(norm.ppf(0.95))) / 0.05)
    es99_normal = (-INITIAL_PORT_VALUE*mu) + ((INITIAL_PORT_VALUE*sigma*norm.pdf(norm.ppf(0.99))) / 0.01)
    print(f'The normal parametric one year 95% ES for AMD is ${round(es95_normal, 2)}')
    print(f'The normal parametric one year 99% ES for AMD is ${round(es99_normal, 2)}')
    print("==================================================================")

    # ES using parametric approach (t-student)
    es95_t = (-INITIAL_PORT_VALUE*mu) + (INITIAL_PORT_VALUE*sigma*(nu+(t.ppf(0.95, nu))**2)) / (((nu-1) * t.pdf(t.ppf(0.95, nu), nu)) / 0.05)
    es99_t = (-INITIAL_PORT_VALUE*mu) + (INITIAL_PORT_VALUE*sigma*(nu+(t.ppf(0.99, nu))**2)) / (((nu-1) * t.pdf(t.ppf(0.99, nu), nu)) / 0.01)
    print(f'The t-student parametric one year 95% ES for AMD is ${round(es95_t, 2)}')
    print(f'The t-student parametric one year 99% ES for AMD is ${round(es99_t, 2)}')
    print("==================================================================")

    # ES monte-carlo method (Gaussian)
    excess_var_95_losses = normal_gen_losses_array > var_norm_mc[0]
    es95_mc_norm = sum(normal_gen_losses_array * excess_var_95_losses) / sum(excess_var_95_losses)
    excess_var_99_losses = normal_gen_losses_array > var_norm_mc[1]
    es99_mc_norm = sum(normal_gen_losses_array * excess_var_99_losses) / sum(excess_var_99_losses)
    print(f'The MC normal estimated one year 95% ES for AMD is ${round(es95_mc_norm, 2)}')
    print(f'The MC normal estimated one year 99% ES for AMD is ${round(es99_mc_norm, 2)}')
    print("==================================================================")

    # ES monte-carlo method (Gaussian)
    excess_var_95_losses_t = t_gen_losses_array > var_t_mc[0]
    es95_mc_t = sum(t_gen_losses_array * excess_var_95_losses_t) / sum(excess_var_95_losses_t)
    excess_var_99_losses_t = t_gen_losses_array > var_t_mc[1]
    es99_mc_t = sum(t_gen_losses_array * excess_var_99_losses_t) / sum(excess_var_99_losses_t)
    print(f'The MC t-student estimated one year 95% ES for AMD is ${round(es95_mc_t, 2)}')
    print(f'The MC t-student estimated one year 99% ES for AMD is ${round(es99_mc_t, 2)}')
    print("==================================================================")

    # ==================== Backtesting VaR ====================
    # Historical VaR
    exceeded_95_hist_array = losses_array > historical_var[0]
    exceeded_95_hist = sum(exceeded_95_hist_array)
    exceeded_95_hist_s = (exceeded_95_hist - (len(losses_array)*0.05)) / np.sqrt(len(losses_array)*0.95*0.05)
    print(f'Our test statistic for historic 95% VaR is {round(exceeded_95_hist_s, 4)}, so we do not reject our null hypothesis.')
    exceeded_99_hist_array = losses_array > historical_var[1]
    exceeded_99_hist = sum(exceeded_99_hist_array)
    exceeded_99_hist_s = (exceeded_99_hist - (len(losses_array)*0.01)) / np.sqrt(len(losses_array)*0.99*0.01)
    print(f'Our test statistic for historic 99% VaR is {round(exceeded_99_hist_s, 4)}, so we do not reject our null hypothesis.')
    print("==================================================================")

    # Parametric (Gaussian)
    exceeded_95_normal_array = losses_array > varnorm95
    exceeded_95_norm = sum(exceeded_95_normal_array)
    exceeded_95_norm_s = (exceeded_95_norm - (len(losses_array)*0.05)) / np.sqrt(len(losses_array)*0.95*0.05)
    print(f'Our test statistic for normal 95% VaR is {round(exceeded_95_norm_s, 4)}, so we do not reject our null hypothesis.')
    exceeded_99_normal_array = losses_array > varnorm99
    exceeded_99_norm = sum(exceeded_99_normal_array)
    exceeded_99_norm_s = (exceeded_99_norm - (len(losses_array)*0.01)) / np.sqrt(len(losses_array)*0.99*0.01)
    print(f'Our test statistic for normal 99% VaR is {round(exceeded_99_norm_s, 4)}, so we do not reject our null hypothesis.')
    print("==================================================================")

    # Parametric t-student
    exceeded_95_t_array = losses_array > vart95
    exceeded_95_t = sum(exceeded_95_t_array)
    exceeded_95_t_s = (exceeded_95_t - (len(losses_array)*0.05)) / np.sqrt(len(losses_array)*0.95*0.05)
    print(f'Our test statistic for t-student 95% VaR is {round(exceeded_95_t_s, 4)}, so we do not reject our null hypothesis.')
    exceeded_99_t_array = losses_array > vart99
    exceeded_99_t = sum(exceeded_99_t_array)
    exceeded_99_t_s = (exceeded_99_t - (len(losses_array)*0.01)) / np.sqrt(len(losses_array)*0.99*0.01)
    print(f'Our test statistic for t-student 99% VaR is {round(exceeded_99_t_s, 4)}, so we do not reject our null hypothesis.')
    print("==================================================================")

    # MC Gaussian
    exceeded_95_mcg_array = losses_array > var_norm_mc[0]
    exceeded_95_mcg = sum(exceeded_95_mcg_array)
    exceeded_95_mcg_s = (exceeded_95_mcg - (len(losses_array)*0.05)) / np.sqrt(len(losses_array)*0.95*0.05)
    print(f'Our test statistic for MC (Gaussian) 95% VaR is {round(exceeded_95_mcg_s, 4)}, so we do not reject our null hypothesis.')
    exceeded_99_mcg_array = losses_array > var_norm_mc[1]
    exceeded_99_mcg = sum(exceeded_99_mcg_array)
    exceeded_99_mcg_s = (exceeded_99_mcg - (len(losses_array)*0.01)) / np.sqrt(len(losses_array)*0.99*0.01)
    print(f'Our test statistic for MC (Gaussian) 99% VaR is {round(exceeded_99_mcg_s, 4)}, so we do not reject our null hypothesis.')
    print("==================================================================")

    # MC t-student
    exceeded_95_mct_array = losses_array > var_t_mc[0]
    exceeded_95_mct = sum(exceeded_95_mct_array)
    exceeded_95_mct_s = (exceeded_95_mct - (len(losses_array)*0.05)) / np.sqrt(len(losses_array)*0.95*0.05)
    print(f'Our test statistic for MC (t-student) 95% VaR is {round(exceeded_95_mct_s, 4)}, so we do not reject our null hypothesis.')
    exceeded_99_mct_array = losses_array > var_t_mc[1]
    exceeded_99_mct = sum(exceeded_99_mct_array)
    exceeded_99_mct_s = (exceeded_99_mct - (len(losses_array)*0.01)) / np.sqrt(len(losses_array)*0.99*0.01)
    print(f'Our test statistic for MC (t-student) 99% VaR is {round(exceeded_99_mct_s, 4)}, so we do not reject our null hypothesis.')
    print("==================================================================")


def port_construction():
    ret_array = np.column_stack((spy_df['Log Returns'], brk_df['Log Returns'], nflx_df['Log Returns']))
    mean = np.mean(ret_array, axis=0)
    cov = np.cov(np.transpose(ret_array))

    weights_1 = np.array([(1/3), (1/3), (1/3)])
    weights_2 = np.array([0.5, 0.25, 0.25])

    mean_ret_port1 = np.dot(weights_1, np.transpose(mean))
    mean_ret_port2 = np.dot(weights_2, np.transpose(mean))

    vol_port_1 = np.sqrt(np.dot(np.dot(weights_1, cov), np.transpose(weights_1)))
    vol_port_2 = np.sqrt(np.dot(np.dot(weights_2, cov), np.transpose(weights_2)))

    norm_var95_port1 = np.dot(-INITIAL_PORT_VALUE*weights_1, mean)+(vol_port_1*INITIAL_PORT_VALUE*norm.ppf(0.95))
    norm_var99_port1 = np.dot(-INITIAL_PORT_VALUE*weights_1, mean)+(vol_port_1*INITIAL_PORT_VALUE*norm.ppf(0.99))
    print(f'The multivariate normal 95% VaR for Port 1 is: ${round(norm_var95_port1, 2)}')
    print(f'The multivariate normal 99% VaR for Port 1 is: ${round(norm_var99_port1, 2)}')
    print('******************************************************************')

    norm_var95_port2 = np.dot(-INITIAL_PORT_VALUE*weights_2, mean)+(vol_port_1*INITIAL_PORT_VALUE*norm.ppf(0.95))
    norm_var99_port2 = np.dot(-INITIAL_PORT_VALUE*weights_2, mean)+(vol_port_1*INITIAL_PORT_VALUE*norm.ppf(0.99))
    print(f'The multivariate normal 95% VaR for Port 2 is: ${round(norm_var95_port2, 2)}')
    print(f'The multivariate normal 99% VaR for Port 2 is: ${round(norm_var99_port2, 2)}')


def brk_analysis():

    # Finding momements of the log returns
    brk_mean = brk_df['Log Returns'].mean()
    brk_var = brk_df['Log Returns'].var()
    brk_skew = brk_df['Log Returns'].skew()
    brk_kur = brk_df['Log Returns'].kurtosis()
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print(f'The mean of BRK.B log returns is: {round(brk_mean, 6)}')
    print(f'The variance of BRK.B log returns is: {round(brk_var, 6)}')
    print(f'The skewness of BRK.B log returns is: {round(brk_skew, 6)}')
    print(f'The kurtosis of BRK.B log returns is: {round(brk_kur, 6)}')
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    # Gaussian kernel density function
    data = brk_df['Log Returns']
    kde = stats.gaussian_kde(data)
    x = np.linspace(data.min(), data.max(), 1000)
    p = kde(x)

    fig2, ax2 = plt.subplots()
    ax2.plot(x, p)
    ax2.plot(x, stats.norm.pdf(x, brk_mean, np.sqrt(brk_var)))
    fig2.suptitle('BRK.B Log Return Empirical Distribution and Normal Distribution', y=0.92)
    ax2.set_xlabel('Log Return')
    ax2.set_ylabel('Probability')
    ax2.legend(['Empirical PDE', 'Gaussian PDE'])
    plt.show()

    # KS Tests
    normal_d, normal_p_value = stats.kstest(brk_df['Log Returns'], 'norm')
    print(f'The p-value for the normal KS Test is {normal_p_value}. Thus, reject null hypothesis.')
    t_d, t_p_value = stats.kstest(brk_df['Log Returns'], 't', args=(4, brk_mean))
    print(f'The p-value for the t-student KS Test is {normal_p_value}. Thus, reject null hypothesis.')


brk_analysis()
# port_construction()
# calculate_loss_stats_amd()
# plot_amd_returns()
