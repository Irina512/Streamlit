import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create data
x = [1, 2, 3, 4]
y = [1, 4, 9, 16]

# Create the figure and axis
fig, ax = plt.subplots()

# Initialize the line plot
line, = ax.plot([], [], 'o-')
ax.set_xlim(0, 5)
ax.set_ylim(0, 20)
ax.set_title('Line Chart Animation')

# Update function for animation
def update(frame):
    line.set_data(x[:frame+1], y[:frame+1])
    return line,

# Create the animation
animation = FuncAnimation(fig, update, frames=len(x), interval=1000, blit=True)

# Display the animation
plt.show()
