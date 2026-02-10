import tkinter as tk
import random
import time
from threading import Thread

class SortingVisualizer(tk.Frame):
    def __init__(self, master, size=50):
        super().__init__(master)
        self.master = master
        self.size = size
        self.array = [random.randint(50, 350) for _ in range(size)]
        self.highlighted1 = -1
        self.highlighted2 = -1
        self.delay = 0.3  # default delay in seconds

        # Canvas setup
        self.canvas = tk.Canvas(self, width=600, height=400, bg="white")
        self.canvas.pack()

        # Controls frame
        control_frame = tk.Frame(master)
        control_frame.pack(pady=10)

        # Buttons for sorting
        buttons = [
            ("Bubble Sort", self.start_bubble_sort),
            ("Insertion Sort", self.start_insertion_sort),
            ("Selection Sort", self.start_selection_sort),
            ("Merge Sort", self.start_merge_sort),
            ("Quick Sort", self.start_quick_sort),
            ("Shuffle Array", self.shuffle_array)
        ]
        for idx, (text, command) in enumerate(buttons):
            tk.Button(control_frame, text=text, command=command).grid(row=0, column=idx, padx=5)

        # Speed slider
        tk.Label(control_frame, text="Speed:").grid(row=1, column=0, padx=5)
        self.speed_slider = tk.Scale(control_frame, from_=1, to=1000, orient="horizontal",
                                     command=self.update_speed)
        self.speed_slider.set(300)
        self.speed_slider.grid(row=1, column=1, columnspan=5, sticky="we")

        # Initial draw
        self.pack()
        self.draw_array()

    def update_speed(self, val):
        """Update the delay from the slider (1–1000 ms)."""
        self.delay = int(val) / 1000

    def draw_array(self):
        self.canvas.delete("all")
        width = 600 / self.size
        for i, height in enumerate(self.array):
            x0 = i * width
            y0 = 400 - height
            x1 = x0 + width - 2
            y1 = 400
            color = "red" if i == self.highlighted1 or i == self.highlighted2 else "blue"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        self.master.update_idletasks()

    def shuffle_array(self):
        self.array = [random.randint(50, 350) for _ in range(self.size)]
        self.highlighted1 = self.highlighted2 = -1
        self.draw_array()

    # -------------------- Sorting Algorithms --------------------
    def bubble_sort(self):
        n = len(self.array)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                self.highlighted1, self.highlighted2 = j, j + 1
                self.draw_array()
                time.sleep(self.delay)
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    self.draw_array()
                    time.sleep(self.delay)
        self.highlighted1 = self.highlighted2 = -1
        self.draw_array()

    def insertion_sort(self):
        for i in range(1, len(self.array)):
            key = self.array[i]
            j = i - 1
            while j >= 0 and self.array[j] > key:
                self.highlighted1, self.highlighted2 = j, j + 1
                self.array[j + 1] = self.array[j]
                self.draw_array()
                time.sleep(self.delay)
                j -= 1
            self.array[j + 1] = key
            self.draw_array()
            time.sleep(self.delay)
        self.highlighted1 = self.highlighted2 = -1
        self.draw_array()

    def selection_sort(self):
        n = len(self.array)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                self.highlighted1, self.highlighted2 = min_idx, j
                self.draw_array()
                time.sleep(self.delay)
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
            self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
            self.draw_array()
            time.sleep(self.delay)
        self.highlighted1 = self.highlighted2 = -1
        self.draw_array()

    def merge_sort(self, l=0, r=None):
        if r is None:
            r = len(self.array) - 1
        if l < r:
            m = (l + r) // 2
            self.merge_sort(l, m)
            self.merge_sort(m + 1, r)
            self.merge(l, m, r)

    def merge(self, l, m, r):
        left = self.array[l:m+1]
        right = self.array[m+1:r+1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            self.highlighted1, self.highlighted2 = k, k
            if left[i] <= right[j]:
                self.array[k] = left[i]
                i += 1
            else:
                self.array[k] = right[j]
                j += 1
            self.draw_array()
            time.sleep(self.delay)
            k += 1
        while i < len(left):
            self.array[k] = left[i]
            i += 1
            k += 1
            self.draw_array()
            time.sleep(self.delay)
        while j < len(right):
            self.array[k] = right[j]
            j += 1
            k += 1
            self.draw_array()
            time.sleep(self.delay)
        self.highlighted1 = self.highlighted2 = -1
        self.draw_array()

    def quick_sort(self, low=0, high=None):
        if high is None:
            high = len(self.array) - 1
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort(low, pi - 1)
            self.quick_sort(pi + 1, high)

    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        for j in range(low, high):
            self.highlighted1, self.highlighted2 = j, high
            self.draw_array()
            time.sleep(self.delay)
            if self.array[j] < pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
                self.draw_array()
                time.sleep(self.delay)
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        self.draw_array()
        time.sleep(self.delay)
        return i + 1

    # -------------------- Threaded Start Methods --------------------
    def start_bubble_sort(self):
        Thread(target=self.bubble_sort).start()

    def start_insertion_sort(self):
        Thread(target=self.insertion_sort).start()

    def start_selection_sort(self):
        Thread(target=self.selection_sort).start()

    def start_merge_sort(self):
        Thread(target=self.merge_sort).start()

    def start_quick_sort(self):
        Thread(target=self.quick_sort).start()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sorting Visualizer: Bubble, Insertion, Selection, Merge, Quick")
    app = SortingVisualizer(root, size=50)
    root.mainloop()