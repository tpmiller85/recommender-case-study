import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

plt.style.use('ggplot')
plt.rcParams.update({'font.size': 18})

if __name__ == "__main__":
    df = pd.read_csv('data/movies/ratings.csv')

    count_rating = df.groupby('rating', as_index=False).count()
    fig, ax = plt.subplots(figsize=(12,10))
    plt.xticks(np.arange(0, 5.5, 0.5))
    plt.xlabel('Ratings')
    plt.ylabel('Counts')
    plt.title('Count per Rating')
    plt.tight_layout()
    ax.bar(count_rating['rating'], count_rating['userId'], align='center', width=0.3)