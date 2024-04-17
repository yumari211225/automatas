import tkinter as tk

class AFD:
    def __init__(self):
        self.states = {'q0', 'q1', 'q2', 'q3', 'q4'} 
        self.alphabet = {'a', 'b', 'c'}  
        self.transitions = {
            'q0': {'a': 'q1', 'b': 'q0', 'c': 'q4'},
            'q1': {'a': 'q1', 'b': 'q2', 'c': 'q4'},
            'q2': {'a': 'q1', 'b': 'q3', 'c': 'q4'},
            'q3': {'a': 'q3', 'b': 'q3', 'c': 'q4'},
            'q4': {'a': 'q1', 'b': 'q0', 'c': 'q4'}
        }  
        self.start_state = 'q0' 
        self.accept_states = {'q1', 'q2', 'q3'}
        self.path = []  # Lista para almacenar el camino seguido

    def run(self, input_string):
        current_state = self.start_state
        self.path = [current_state]  # Inicializa la lista de camino
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False, self.path  # Retorna el camino seguido hasta ahora
            if current_state not in self.transitions or symbol not in self.transitions[current_state]:
                return False, self.path  # Retorna el camino seguido hasta ahora
            current_state = self.transitions[current_state][symbol]
            self.path.append(current_state)  # Agrega el estado al camino
        return current_state in self.accept_states, self.path  # Retorna el resultado y el camino seguido

class AFDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AFD para Lenguaje Específico")
        
        self.label = tk.Label(root, text="Ingrese una cadena:")
        self.label.pack()

        self.input_entry = tk.Entry(root)
        self.input_entry.pack()

        self.check_button = tk.Button(root, text="Verificar", command=self.check_input)
        self.check_button.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

        self.path_label = tk.Label(root, text="")
        self.path_label.pack()

        self.canvas = tk.Canvas(root, width=500, height=300)
        self.canvas.pack()

        self.automaton = AFD()

    def draw_states(self, path):
        self.states_positions = {
            'q0': (50, 150),
            'q1': (150, 50),
            'q2': (250, 50),
            'q3': (350, 50),
            'q4': (450, 150)
        }
        for state, (x, y) in self.states_positions.items():
            if state in self.automaton.states and state in path:
                fill_color = "white"
                if state in self.automaton.accept_states:
                    fill_color = "#9ACD32"
                self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=fill_color, outline="black")
                self.canvas.create_text(x, y, text=state)

    def draw_path(self, path, input_string):
        prev_state = None
        for i, state in enumerate(path):
            if state in self.states_positions:
                x, y = self.states_positions[state]
                fill_color = "white"
                if i == len(path) - 1 and state in self.automaton.accept_states:
                    fill_color = "#9ACD32"
                self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=fill_color, outline="black")
                self.canvas.create_text(x, y, text=state)
                
                if prev_state is not None and prev_state in path:
                    self.canvas.create_line(*self.states_positions[prev_state], x, y, arrow=tk.LAST)
                prev_state = state
                
                if i < len(input_string):
                    self.canvas.create_text(x, y+30, text=input_string[i], fill="blue")

    def check_input(self):
        self.canvas.delete("all")  # Elimina todo el contenido del lienzo
        input_string = self.input_entry.get()
        result, path = self.automaton.run(input_string)
        if result:
            self.result_label.config(text=f'La cadena "{input_string}" es aceptada por el AFD.')
        else:
            self.result_label.config(text=f'La cadena "{input_string}" no es aceptada por el AFD.')
        self.path_label.config(text=f'Camino seguido: {" -> ".join(path)}')
        self.draw_states(path)
        self.draw_path(path, input_string)

# Crear la ventana principal
root = tk.Tk()
app = AFDApp(root)
root.mainloop()
