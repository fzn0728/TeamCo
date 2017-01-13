import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns # improves plot aesthetics
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as mtick


def _invert(x, limits):
    """inverts a value x on a scale from
    limits[0] to limits[1]"""
    return limits[1] - (x - limits[0])

def _scale_data(data, ranges):
    """scales data[1:] to ranges[0],
    inverts if the scale is reversed"""
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        assert (y1 <= d <= y2) or (y2 <= d <= y1)
    x1, x2 = ranges[0]
    d = data[0]
    if x1 > x2:
        d = _invert(d, (x1, x2))
        x1, x2 = x2, x1
    sdata = [d]
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        if y1 > y2:
            d = _invert(d, (y1, y2))
            y1, y2 = y2, y1
        sdata.append((d-y1) / (y2-y1) 
                     * (x2 - x1) + x1)
    return sdata

class ComplexRadar():
    '''Generate the radar object, give necessary feature
    '''
    def __init__(self, fig, variables, ranges,
                 n_ordinate_levels=6):
        angles = np.arange(0, 360, 360./len(variables))

        axes = [fig.add_axes([0.05,0.12,0.95,0.75],polar=True,
                label = "axes{}".format(i)) 
                for i in range(len(variables))]
        l, text = axes[0].set_thetagrids(angles, 
                                         labels=variables)
        [txt.set_rotation(angle-90) for txt, angle 
             in zip(text, angles)]
        for ax in axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)
        for i, ax in enumerate(axes):
            grid = np.linspace(*ranges[i], 
                               num=n_ordinate_levels)[:-1] # Ignore the last grid label and grid since they will overlap with the edge of the radar chart 
            gridlabel = ["{}".format(round(x,2)) 
                         for x in grid]
            if ranges[i][0] > ranges[i][1]:
                grid = grid[::-1] # hack to invert grid
                          # gridlabels aren't reversed
            gridlabel[0] = "" # clean up origin
            ax.set_rgrids(grid, labels=gridlabel,
                         angle=angles[i])
            #ax.spines["polar"].set_visible(False)
            ax.set_ylim(*ranges[i])
        # variables for plotting
        self.angle = np.deg2rad(np.r_[angles, angles[0]])
        self.ranges = ranges
        self.ax = axes[0]
    def plot(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.ax.plot(self.angle, np.r_[sdata, sdata[0]], *args, **kw)
    def fill(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.ax.fill(self.angle, np.r_[sdata, sdata[0]], *args, **kw)


def radar_plot(dataframe, chart_name, legend_loc):
    '''Plot the Radar chart and make several modification on legend, title and etc.
    
    Args:
        dataframe is the dataframe for plotting, static data table
        chart_name is the title u want to give for this radar chart
    '''
    variables = tuple(list(dataframe.index))
    d = {}
    ranges = [None] * (len(dataframe.index))
    for j in range(len(dataframe.columns)):
        d["{0}".format(dataframe.columns[j])] = tuple(list(dataframe.iloc[:,j].values))
        for i in range(len(dataframe.index)):
            # ranges[i] = tuple((0.8*min(dataframe.iloc[i,:].values), 1.05*max(dataframe.iloc[i,:].values))) # For future use if you want to change axe according to different variable
            ranges[i] = tuple((0.8*np.min(dataframe.values), 1.05*np.max(dataframe.values)))
    # plotting
    plt.style.use('fivethirtyeight')
    fig1 = plt.figure(figsize=(8, 8))
    radar = ComplexRadar(fig1, variables, ranges)
    
    for j in dataframe.columns:
        radar.plot(d[j], label = str(j), alpha=0.7, linewidth=2)
        # radar.fill(d[j], alpha=0.2)
    radar.ax.legend(loc=legend_loc,prop={'size':8})
    plt.figtext(0.50, 0.965, chart_name, \
                ha='center', color='black', weight='bold', size='large')
    plt.show()   
    return fig1


def graph_gen(pdf_name, index_name, rolling_annual_return_df, cum_return_df, rolling_alpha_df, \
              rolling_beta_df, rolling_corr_df, rolling_sharpe_ratio_df, rolling_sortino_ratio_df, \
              rolling_omega_ratio_df, dd_df, Beta_df, Beta_df_p, Beta_df_np, Corr_df, Corr_df_p, Corr_df_np):
    '''Generate the graph according to the requirement and save them into one single pdf file.
    
    Args:
        pdf_name is the name of output pdf file
        index_name is the columns names and we should draw lines based on that
        Others are all dataframe names given from previous output
    '''
    ### Graph for result
    with PdfPages(pdf_name) as pdf:
        plt.style.use('fivethirtyeight')
        # Annual return
        # a = rolling_annual_return_df[['TeamCo Client Composite', 'HFRI Fund Weighted Composite Index', 'HFRI Fund of Funds Composite Index']].plot(title='36 Months Rolling Annualized Return')
        fig, ax = plt.subplots()
        for j in index_name:
            if j == 'TeamCo Client Composite':
                plt.plot(rolling_annual_return_df.index,(rolling_annual_return_df[[j]]), linewidth=4, label=j)
            else:
                plt.plot(rolling_annual_return_df.index,(rolling_annual_return_df[[j]]), linestyle="--", linewidth=2, label=j)
        plt.legend(loc='upper left', prop={'size':12})
        plt.xlabel('Year')
        plt.ylabel('Annualized Return')
        plt.title('Annualized Return')
        # manipulate to % format
        vals = ax.get_yticks()
        ax.set_yticklabels(['{:3.1f}%'.format(x*100) for x in vals])
        pdf.savefig()
        plt.close()
        
        # Cummulative return
        fig, ax = plt.subplots()
        for j in index_name:
            if j == 'TeamCo Client Composite':
                plt.plot(cum_return_df.index,(cum_return_df[[j]]), linewidth=4, label=j)
            else:
                plt.plot(cum_return_df.index,(cum_return_df[[j]]), linestyle="--", linewidth=2, label=j)
        
        plt.legend(loc='upper left', prop={'size':12})
        plt.xlabel('Year')
        plt.ylabel('Cummulative Return')
        plt.title('Cummulative Return')
        # manipulate to % format
        vals = ax.get_yticks()
        ax.set_yticklabels(['{:3.1f}%'.format(x*100) for x in vals])
        pdf.savefig()
        plt.close()
        
        #Rolling alpha
        for j in index_name:
            if j == 'TeamCo Client Composite':
                plt.plot(rolling_alpha_df.index,(rolling_alpha_df[[j]]), linewidth=4, label=j)
            else:
                plt.plot(rolling_alpha_df.index,(rolling_alpha_df[[j]]), linestyle="--", linewidth=2, label=j)
        plt.legend(prop={'size':12})
        plt.xlabel('Year')
        plt.ylabel('Annualized Alpha')
        plt.title('36 Months Rolling Alpha')
        pdf.savefig()
        plt.close()
        
        # Rolling Beta
        for j in index_name:
            if j == 'TeamCo Client Composite':
                plt.plot(rolling_beta_df.index,(rolling_beta_df[[j]]), linewidth=4, label=j)
            else:
                plt.plot(rolling_beta_df.index,(rolling_beta_df[[j]]), linestyle="--", linewidth=2, label=j)
        plt.legend(prop={'size':12})
        plt.xlabel('Year')
        plt.ylabel('Beta')
        plt.title('36 Months Rolling Beta')
        pdf.savefig()
        plt.close()
        
        # Rolling correlation
        for j in index_name:
            if j == 'TeamCo Client Composite':
                plt.plot(rolling_corr_df.index,(rolling_corr_df[[j]]), linewidth=4, label=j)
            else:
                plt.plot(rolling_corr_df.index,(rolling_corr_df[[j]]), linestyle="--", linewidth=2, label=j)
        plt.legend(prop={'size':12})
        plt.xlabel('Year')
        plt.ylabel('Correlation')
        plt.title('36 Months Rolling Correlation')
        pdf.savefig()        
        plt.close()
        
        # Rolling Sharpe Ratio
        for j in index_name:
            if j == 'TeamCo Client Composite':
                plt.plot(rolling_sharpe_ratio_df.index,(rolling_sharpe_ratio_df[[j]]), linewidth=4, label=j)
            else:
                plt.plot(rolling_sharpe_ratio_df.index,(rolling_sharpe_ratio_df[[j]]), linestyle="--", linewidth=2, label=j)
        plt.legend(loc='upper left',prop={'size':12})
        plt.xlabel('Year')
        plt.ylabel('Annualized Sharpe Ratio')
        plt.title('36 Months Rolling Sharpe Ratio')
        pdf.savefig() 
        plt.close()
        
        # Rolling Sortino Ratio
        for j in index_name:
            if j == 'TeamCo Client Composite':
                plt.plot(rolling_sharpe_ratio_df.index,(rolling_sharpe_ratio_df[[j]]), linewidth=4, label=j)
            else:
                plt.plot(rolling_sharpe_ratio_df.index,(rolling_sharpe_ratio_df[[j]]), linestyle="--", linewidth=2, label=j)
        plt.legend(loc='upper left',prop={'size':12})
        plt.xlabel('Year')
        plt.ylabel('Annualized Sortino Ratio')
        plt.title('36 Months Rolling Sortino')
        pdf.savefig()
        plt.close()
        
        # Rolling Omega Ratio
        for j in index_name:
            if j == 'TeamCo Client Composite':
                plt.plot(rolling_omega_ratio_df.index,(rolling_omega_ratio_df[[j]]), linewidth=4, label=j)
            else:
                plt.plot(rolling_omega_ratio_df.index,(rolling_omega_ratio_df[[j]]), linestyle="--", linewidth=2, label=j)
        plt.legend(loc='upper left',prop={'size':12})
        plt.xlabel('Year')
        plt.ylabel('Omega Ratio')
        plt.title('36 Months Rolling Omega Ratio')
        pdf.savefig()
        plt.close()
        
        # Drawdown
        for j in index_name:
            if j == 'TeamCo Client Composite':
                plt.plot(dd_df.index,(dd_df[[j]]), linewidth=4, label=j)
            else:
                plt.plot(dd_df.index,(dd_df[[j]]), linestyle="--", linewidth=2, label=j)
        plt.legend(loc='lower left',prop={'size':12})
        plt.xlabel('Year')
        plt.ylabel('Draw Down')
        plt.title('Draw Down - Fund vs Competitors vs Benchmark')
        pdf.savefig()
        plt.close()        
        
        # max_dd_df.plot(title='Current Drawdown Changing Graph')
        
        # Plot radar plot
        # Beta
        a = radar_plot(Beta_df.fillna(0.01), 'Beta Radar Chart', 'best')
        pdf.savefig(a) 
        plt.close()
        
        # Upside Beta
        b = radar_plot(Beta_df_p.fillna(0.01), 'Beta Radar Chart (Upside)', 'best')
        pdf.savefig(b)
        plt.close()
        
        # Downside Beta
        c = radar_plot(Beta_df_np.fillna(0.01), 'Beta Radar Chart (Downside)', 'best')
        pdf.savefig(c)
        plt.close()
        
        # Correlation
        d = radar_plot(Corr_df.fillna(0.01), 'Correlation Radar Chart', 'best')
        pdf.savefig(d)
        plt.close()
        
        # Upside Correlation
        e = radar_plot(Corr_df_p.fillna(0.01), 'Correlation Radar Chart (Upside)', 'best')
        pdf.savefig(e)
        plt.close()
        
        # Downside Correlation
        f = radar_plot(Corr_df_np.fillna(0.01), 'Correlation Radar Chart (Downside)', 'best')
        pdf.savefig(f)
        plt.close()
        

    
