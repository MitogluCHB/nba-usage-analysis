import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


usage_df = pd.read_csv('denver_usage.csv')

mean_usage = usage_df.groupby('name')['usage %'].mean()

with_jokic = usage_df[usage_df['jokic_playing'] == True]
without_jokic = usage_df[usage_df['jokic_playing'] == False]

mean_usage_without_jokic = without_jokic.groupby('name')['usage %'].mean().rename('without_jokic')
mean_usage_with_jokic = with_jokic.groupby('name')['usage %'].mean().rename('with_jokic')

merged = pd.merge(mean_usage_with_jokic, mean_usage_without_jokic, on='name')

merged['usage_difference'] = round(merged['without_jokic'] - merged['with_jokic'], 2)
print(merged.sort_values(by='usage_difference', ascending=False))


x = np.arange(len(merged))   # numeričke pozicije
width = 0.4                  # širina jednog bara
plt.bar(x - width/2, merged['with_jokic'], width, label='With Jokic')
plt.bar(x + width/2, merged['without_jokic'], width, label='Without Jokic')

plt.xticks(x, merged.index, rotation=45, ha='right')
plt.legend()
plt.title('Player Usage With/Without Jokic', )
plt.tight_layout()
plt.savefig('denver_usage.png')
plt.show()

