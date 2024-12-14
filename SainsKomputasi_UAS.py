import numpy as np
from scipy.linalg import lu, solve
import random
import tkinter as tk
from tkinter import messagebox, simpledialog

class NumericalCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Numerical Calculator")

        
        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack()

        
        tk.Label(self.menu_frame, text="=== Numerical Calculator ===", font=("Arial", 16)).pack(pady=10)

        
        buttons = [
            ("Matrix Operations", self.matrix_operations),
            ("Inversion and LU Decomposition", self.inversion_lu),
            ("Gaussian Elimination", self.gaussian_elimination),
            ("Iterative Methods", self.iterative_methods),
            ("Open Methods", self.open_methods),
            ("Closed Methods", self.closed_methods),
            ("Interpolation", self.interpolation),
            ("Simulation Models", self.simulation_models),
            ("Exit", root.quit),
        ]
        
        for text, command in buttons:
            tk.Button(self.menu_frame, text=text, command=command, width=30, font=("Arial", 12)).pack(pady=5)

    
    def matrix_operations(self):
        matrix_A = self.ask_matrix("Masukkan elemen matriks A (contoh: 1,2;3,4 untuk matriks 2x2):")
        matrix_B = self.ask_matrix("Masukkan elemen matriks B (ukuran yang sama dengan A, contoh: 1,2;3,4 untuk matriks 2x2):")
        
        if matrix_A is not None and matrix_B is not None:
            try:
                result = (
                    f"Matrix A:\n{matrix_A}\n"
                    f"Matrix B:\n{matrix_B}\n"
                    f"A + B:\n{matrix_A + matrix_B}\n"
                    f"A - B:\n{matrix_A - matrix_B}\n"
                    f"A @ B (perkalian matriks):\n{matrix_A @ matrix_B}\n"
                    f"Transpose dari A:\n{matrix_A.T}"
                )
                messagebox.showinfo("Matrix Operations", result)
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    
    def inversion_lu(self):
        matrix_A = self.ask_matrix("Masukkan elemen matriks persegi A (contoh: 1,2;3,4 untuk matriks 2x2):")
        
        if matrix_A is not None:
            try:
                invers_matrix = np.linalg.inv(matrix_A)
                P, L, U = lu(matrix_A)
                result = (
                    f"Matrix A:\n{matrix_A}\n"
                    f"Inverse dari Matrix A:\n{invers_matrix}\n"
                    f"Decomposisi LU:\nP:\n{P}\nL:\n{L}\nU:\n{U}"
                )
                messagebox.showinfo("Inversion and LU Decomposition", result)
            except np.linalg.LinAlgError:
                messagebox.showerror("Error", "Matriks tidak dapat dibalik (singular).")

    
    def gaussian_elimination(self):
        augmented_matrix = self.ask_matrix("Masukkan matriks augmented (contoh: 1,2,3;4,5,6 untuk matriks Ax = b):")
        if augmented_matrix is not None:
            try:
                A = augmented_matrix[:, :-1]
                b = augmented_matrix[:, -1]
                x = solve(A, b)
                result = f"Solusi menggunakan Eliminasi Gauss:\n{x}"
                messagebox.showinfo("Gaussian Elimination", result)
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    
    def iterative_methods(self):
        matrix_A = self.ask_matrix("Masukkan elemen matriks A (contoh: 1,2;3,4 untuk matriks 2x2):")
        vector_b = self.ask_vector("Masukkan vektor b (pisahkan nilai dengan koma, contoh: 1,2,3):")
        
        if matrix_A is not None and vector_b is not None:
            
            x0 = np.zeros_like(vector_b)
            for _ in range(10):
                x0 = (vector_b - np.dot(matrix_A, x0) + np.diag(matrix_A) * x0) / np.diag(matrix_A)
            result = f"Solusi menggunakan Metode Jacobi:\n{x0}"
            messagebox.showinfo("Iterative Methods", result)

    
    def open_methods(self):
        f = simpledialog.askstring("Input", "Masukkan fungsi (contoh: lambda x: x**2 - 4):")
        df = simpledialog.askstring("Input", "Masukkan turunan dari fungsi (contoh: lambda x: 2*x):")
        f = eval(f)
        df = eval(df)
        x = float(simpledialog.askstring("Input", "Masukkan tebakan awal untuk x (contoh: 2.0):"))
        
        for _ in range(5):
            x = x - f(x) / df(x)
        messagebox.showinfo("Open Methods", f"Root menggunakan Metode Newton-Raphson: {x}")

    
    def closed_methods(self):
        f = simpledialog.askstring("Input", "Masukkan fungsi (contoh: lambda x: x**3 - x - 2):")
        a, b = map(float, simpledialog.askstring("Input", "Masukkan interval [a, b] (pisahkan dengan spasi, contoh: 1 2):").split())
        
        f = eval(f)
        for _ in range(10):
            c = (a + b) / 2
            if f(c) == 0:
                break
            elif f(a) * f(c) < 0:
                b = c
            else:
                a = c
        messagebox.showinfo("Closed Methods", f"Root menggunakan Metode Bisection: {c}")

   
    def interpolation(self):
        x = simpledialog.askstring("Input", "Masukkan nilai x (pisahkan dengan koma, contoh: 1,2,3):")
        y = simpledialog.askstring("Input", "Masukkan nilai y yang sesuai (pisahkan dengan koma, contoh: 2,3,5):")
        degree = int(simpledialog.askstring("Input", "Masukkan derajat polinom (contoh: 2):"))
        
        x = np.array(list(map(float, x.split(','))))
        y = np.array(list(map(float, y.split(','))))
        coeffs = np.polyfit(x, y, degree)
        
        result = f"Koefisien Polinom (derajat {degree}):\n{coeffs}"
        messagebox.showinfo("Interpolation", result)

    
    def simulation_models(self):
        trials = int(simpledialog.askstring("Input", "Masukkan jumlah percobaan untuk Monte Carlo (contoh: 10000):"))
        estimate = sum(random.random() ** 2 + random.random() ** 2 <= 1 for _ in range(trials)) / trials * 4
        
        messagebox.showinfo("Monte Carlo Simulation", f"Perkiraan Pi menggunakan Monte Carlo: {estimate}")

   
    def ask_matrix(self, prompt):
        input_string = simpledialog.askstring("Input", prompt)
        if input_string:
            try:
                return np.array([list(map(float, row.split(","))) for row in input_string.split(";")])
            except ValueError:
                messagebox.showerror("Error", "Format matriks tidak valid.")
        return None

    
    def ask_vector(self, prompt):
        input_string = simpledialog.askstring("Input", prompt)
        if input_string:
            try:
                return np.array(list(map(float, input_string.split(","))))
            except ValueError:
                messagebox.showerror("Error", "Format vektor tidak valid.")
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = NumericalCalculatorApp(root)
    root.mainloop()
