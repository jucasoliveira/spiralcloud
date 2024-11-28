import glob
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Extract metrics from files
txt_files = glob.glob('**/*.txt')
metrics = {}

for file in txt_files:
    language = file.split('/')[-1]  # Get just the filename
    language = language.replace('metrics_', '').replace('.txt', '')
    frame_times = []
    points_drawn = []

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

# Setup for the animation
languages = sorted(
    metrics.keys(), key=lambda lang: metrics[lang]['avg_frame_time'])
avg_frame_times = [metrics[lang]['avg_frame_time'] for lang in languages]

# Configuration for animation
x_max = 10000  # Maximum horizontal width for the balls
fig, ax = plt.subplots(figsize=(10, 5))

# Initialize positions and velocities for each language
positions = np.zeros(len(languages))
# Further slower speed by increasing divisor  # Slower speed by increasing divisor  # Slower speed by increasing divisor
velocities = [x_max / (avg_frame_time * 20)
              for avg_frame_time in avg_frame_times]

# Set up the plot
ax.set_xlim(0, x_max)
ax.set_ylim(-1, len(languages))
ax.set_yticks(range(len(languages)))
ax.set_yticklabels(languages, rotation=45)
ax.set_xlabel('Position')
ax.set_title('Languages Animation: Ball Speed Based on Average Frame Time')

# Set different colors for each language
colors = plt.cm.get_cmap('tab10', len(languages))

# Initialize scatter plot for the balls
# Doubled size of the balls again  # Doubled size of the balls  # Increased size of the balls
scat = ax.scatter(positions, range(len(languages)), s=1200, color=[
                  colors(i) for i in range(len(languages))])


def update(frame):
    global positions

    # Update positions based on velocities
    for i in range(len(positions)):
        positions[i] += velocities[i]
        # Reverse direction if the ball reaches the boundaries
        if positions[i] >= x_max or positions[i] <= 0:
            velocities[i] *= -1

    # Update scatter plot with new positions
    scat.set_offsets(np.c_[positions, range(len(languages))])
    return scat,


# Create the animation
ani = animation.FuncAnimation(
    fig, update, frames=np.arange(0, 1000), interval=20, blit=True)

# Save animation as MP4
writer = animation.FFMpegWriter(fps=50, bitrate=1800)
ani.save('language_animation.mp4', writer=writer)

# Comment out or remove plt.show() if you don't want to display the animation while saving
# plt.show()

plt.tight_layout()
plt.show()
