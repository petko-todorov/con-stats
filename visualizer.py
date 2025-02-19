import matplotlib.pyplot as plt
import seaborn as sns


def visualizer(df_plot):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_plot, x='Day', y='VP', hue='Nation', marker='o')

    plt.xlim(left=1)
    plt.xticks(ticks=range(int(df_plot["Day"].min()), int(df_plot["Day"].max()) + 1))

    for nation in df_plot['Nation'].unique():
        nation_data = df_plot[df_plot['Nation'] == nation]

        first_row = nation_data.iloc[0]
        last_row = nation_data.iloc[-1]

        plt.text(first_row['Day'], first_row['VP'], str(first_row['VP']),
                 fontsize='x-large', ha='center', va='bottom')

        plt.text(last_row['Day'], last_row['VP'], str(last_row['VP']),
                 fontsize='x-large', ha='center', va='bottom')

    plt.title("Progression of Victory Points in Conflict of Nations")
    plt.xlabel("Day")
    plt.ylabel("Victory Points")

    plt.legend(title="Nation")
    plt.grid(True)

    plt.show()
