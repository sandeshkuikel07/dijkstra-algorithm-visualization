# DijkstraDash

A Python-based project for visualizing the Dijkstra Algorithm using `Pygame`. This project also includes placeholders for Floyd-Warshall and Bellman-Ford visualizations.

---

## **Features**

- **Interactive Visualization**: Place barriers, set start and target points, and watch Dijkstra's algorithm in action.
- **Customizable Node Grid**: Adjust node layout and obstacles with mouse clicks.
- **User-Friendly Interface**: Built using `Pygame` for easy navigation and visualization.
- **Algorithm Speed Control**: Adjust the speed of the algorithm to watch each step in detail.
- **Path Tracing**: Visualize the shortest path after the algorithm finishes.
- **Multiple Algorithm Support**: Toggle between Dijkstra's, Bellman-Ford, and Floyd-Warshall algorithms.

---

## **How to Run**

### **1. Prerequisites**

Ensure the following are installed:

- Python 3.8+
- Pygame library
- Tkinter (comes pre-installed with Python)

To install Pygame, run:

```bash
pip install pygame
```

---

## **How to Visualize**

1. **Set the Starting Node**:

   - Right-click on a node to set it as the starting point.

2. **Set the Target Node**:

   - Right-click on another node to set it as the target point.

3. **Place Barriers**:

   - Click and drag the left mouse button over nodes to place barriers.
   - This restricts the path, forcing the algorithm to find an alternative route.

4. **Start Visualization**:

   - Press the `SPACE` key to begin the visualization of the selected algorithm.

5. **Algorithm Execution**:

   - The algorithm will explore paths and find the shortest route from the start node to the target node.
   - Once completed, the shortest path will be highlighted.

6. **Reset the Nodes**:

   - Press the `R` key to reset the visualization and try again with new configurations.

---

This interactive tool provides a hands-on approach to understanding pathfinding algorithms and their behavior in different scenarios.

