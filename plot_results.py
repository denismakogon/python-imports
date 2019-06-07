import random
import pandas as pd

from plotly import graph_objs
from plotly import offline

random.seed()


def save_plot(pairs_of_x_y: list, where_to_save: str):
    html_file = '{0}-peaks.html'.format(where_to_save)

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

    offline.plot(
        brs,
        filename=html_file,
        auto_open=False,
    )
    return html_file


def df_from_file(fname):
    df = pd.read_csv(fname, sep="\n")
    df.columns = ["time"]
    df['index'] = range(0, len(df))

    return df


if __name__ == "__main__":
    raw_results_file = "raw_results.txt"
    lru_results_file = "lru_results.txt"

    df_raw = df_from_file(raw_results_file)
    df_lru = df_from_file(lru_results_file)

    raw_mean = df_raw["time"].mean()
    print("Raw imports mean: ", raw_mean)
    lru_mean = df_lru["time"].mean()
    print("LRU imports mean: ", lru_mean)

    raw_filtered = df_raw.loc[df_raw["time"] >= raw_mean]
    print("Number of peaks during raw imports: ", len(raw_filtered))
    lru_filtered = df_lru.loc[df_lru["time"] >= lru_mean]
    print("Number of peaks during LRU imports: ", len(lru_filtered))

    lowest_mean = lru_mean if raw_mean > lru_mean else raw_mean
    print("Lower mean: ", lowest_mean)
    raw_filtered_v2 = df_raw.loc[df_raw["time"] >= lowest_mean]
    print("Number of peaks during raw imports (higher than a lower mean): ", len(raw_filtered_v2))
    lru_filtered_v2 = df_lru.loc[df_lru["time"] >= lowest_mean]
    print("Number of peaks during LRU imports (higher than a lower mean): ", len(lru_filtered_v2))

    save_plot(
        [
            ("raw imports", df_raw['index'], df_raw['time']),
            ("LRU imports", df_lru['index'], df_lru['time']),
        ],
        "final_results",
    )
