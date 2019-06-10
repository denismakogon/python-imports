import random
import pandas as pd

from plotly import graph_objs
from plotly import offline


random.seed()


def create_graphic_objects(pairs_of_x_y: list):

    brs = []
    for title, x, y in pairs_of_x_y:
        brs.append(graph_objs.Bar(
            x=x, y=y,
            marker=dict(color='rgb({0},{1},{2})'.format(
                    random.randint(30, 255),
                    random.randint(30, 255),
                    random.randint(30, 255),
                )
            ),
            name=title
        ))

    return brs


def df_from_file(fname):
    df = pd.read_csv(fname, sep="\n")
    df.columns = ["time"]
    df['index'] = range(0, len(df))

    return df


def get_percentage_from_range(df_raw, df_lru, lim1, lim2):
    print(f"Range: [{lim1}:{lim2}]")

    df1_filtered = df_raw.loc[df_raw["time"].between(lim1, lim2)]
    df2_filtered = df_lru.loc[df_lru["time"].between(lim1, lim2)]

    df1_filtered_mean = df1_filtered['time'].mean()
    df1_filtered_len = len(df1_filtered)
    print(f"Number of raw imports in range: {df1_filtered_len}")

    df2_filtered_mean = df2_filtered['time'].mean()
    df2_filtered_len = len(df2_filtered)
    print(f"Number of LRU imports in range: {df2_filtered_len}")

    print(f"Raw imports mean: {df1_filtered_mean}")
    print(f"LRU imports mean: {df2_filtered_mean}")

    return (float(df1_filtered_mean/df2_filtered_mean) - 1) * 100


if __name__ == "__main__":

    raw_results_file = "raw_results.txt"
    lru_results_file = "lru_results.txt"

    df_raw = df_from_file(raw_results_file)
    df_lru = df_from_file(lru_results_file)

    max_lru = df_lru['time'].max()
    max_raw = df_raw['time'].max()
    max_of_maxes = max((max_lru, max_raw))

    for lim1, lim2 in [(0, 20000),
                       (20000, 40000),
                       (40000, 60000),
                       (60000, 80000),
                       (80000, max_of_maxes)]:
        prctg = get_percentage_from_range(df_raw, df_lru, lim1, lim2)
        print(f"Practical percentage of slow imports in range [{lim1}: {lim2}]: {prctg}\n\n")

    objs = create_graphic_objects(
        [
            ("raw imports", df_raw['index'], df_raw['time']),
            ("LRU imports", df_lru['index'], df_lru['time']),
        ],
    )

    offline.plot(
        objs,
        filename='{0}-peaks.html'.format("final_results"),
        auto_open=False,
    )
