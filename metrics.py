# Get all txt files in the current directory
# Get Frame Time and Points Drawn eg.: Frame Time: 2.20 ms, Points Drawn: 9591
# For each programming language , calculate the average Frame Time and Points Drawn
# Create a bar chart for each programming language
import glob
import re
import numpy as np
import matplotlib.pyplot as plt

txt_files = glob.glob('**/*.txt')

metrics = {}


# Extract the metrics from each file
for file in txt_files:
    print(file)
    language = file.replace('metrics_', '').replace('.txt', '')
    frame_times = []
    points_drawn = []
    print(language)

    with open(file, 'r') as f:
        for line in f:

            match = re.search(
                r'Frame\s*Time:\s*([\d.]+)\s*ms,\s*Points\s*Drawn:\s*(\d+)', line)
            if match:
                frame_times.append(float(match.group(1)))
                points_drawn.append(int(match.group(2)))

    if frame_times and points_drawn:
        avg_frame_time = sum(frame_times) / len(frame_times)
        avg_points_drawn = sum(points_drawn) / len(points_drawn)
        metrics[language] = {
            'avg_frame_time': avg_frame_time,
            'avg_points_drawn': avg_points_drawn
        }

languages = list(metrics.keys())
avg_frame_times = [metrics[lang]['avg_frame_time'] for lang in languages]
avg_points_drawn = [metrics[lang]['avg_points_drawn'] for lang in languages]

x = np.arange(len(languages))
width = 0.35

fig, ax = plt.subplots(2, 1, figsize=(10, 10))

ax[0].bar(x, avg_frame_times, width, label='Frame Time')
ax[0].set_xticks(x, languages)
ax[0].set_xlabel('Language')
ax[0].set_ylabel('Average Frame Time (ms)')
ax[0].legend()


ax[1].bar(x, avg_points_drawn, width, label='Points Drawn')
ax[1].set_xticks(x, languages)
ax[1].set_xlabel('Language')
ax[1].set_ylabel('Average Points Drawn')
ax[1].legend()

plt.tight_layout()
plt.show()
