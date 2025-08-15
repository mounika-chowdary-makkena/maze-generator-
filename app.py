from flask import Flask, render_template, jsonify, url_for
import random

app = Flask(__name__)

def generate_maze(rows=15, cols=20):
    H, W = 2 * rows + 1, 2 * cols + 1
    maze = [['#'] * W for _ in range(H)]
    for r in range(rows):
        for c in range(cols):
            maze[2 * r + 1][2 * c + 1] = ' '

    stack = [(0, 0)]
    visited = {(0, 0)}
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def carve(r1, c1, r2, c2):
        ar, ac = 2 * r1 + 1, 2 * c1 + 1
        br, bc = 2 * r2 + 1, 2 * c2 + 1
        maze[(ar + br) // 2][(ac + bc) // 2] = ' '

    while stack:
        r, c = stack[-1]
        neighbors = [(r+dr, c+dc) for dr, dc in dirs
                     if 0 <= r+dr < rows and 0 <= c+dc < cols and (r+dr, c+dc) not in visited]
        if neighbors:
            nr, nc = random.choice(neighbors)
            carve(r, c, nr, nc)
            visited.add((nr, nc))
            stack.append((nr, nc))
        else:
            stack.pop()

    maze[1][0] = 'S'
    maze[2 * rows - 1][2 * cols] = 'E'
    return maze

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/maze")
def maze():
    maze_data = generate_maze()
    return jsonify(maze_data)

if __name__ == "__main__":
    app.run(debug=True)
