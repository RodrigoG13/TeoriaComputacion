# Ejecutar el código corregido proporcionado por el usuario para la simulación de la máquina de Turing

class TuringMachine:
    def __init__(self, tape, blank_symbol="B"):
        self.tape = list(tape) + [blank_symbol] * 10  # Add some blank symbols for simulation
        self.head_position = 0
        self.current_state = 'q0'
        self.blank_symbol = blank_symbol
        self.halted = False

        # Define the transition function based on the diagram provided
        self.transition_function = {
            ('q0', '0'): ('q1', 'X', 'R'),
            ('q0', 'Y'): ('q3', 'Y', 'R'),
            ('q1', '0'): ('q1', '0', 'R'),
            ('q1', '1'): ('q2', 'Y', 'L'),
            ('q1', 'Y'): ('q1', 'Y', 'R'),
            ('q2', '0'): ('q2', '0', 'L'),
            ('q2', 'X'): ('q0', 'X', 'R'),
            ('q2', 'Y'): ('q2', 'Y', 'L'),
            ('q3', 'Y'): ('q3', 'Y', 'R'),
            ('q3', blank_symbol): ('q4', blank_symbol, 'R'),
        }

    def step(self):
        if self.halted:
            return

        # Read the symbol at the current head position
        current_symbol = self.tape[self.head_position]
        # Lookup the action to take in the transition function
        action = self.transition_function.get((self.current_state, current_symbol))

        if action is None:
            self.halted = True  # No transition means halt
        else:
            new_state, new_symbol, move_direction = action

            # Write the new symbol at the current head position
            self.tape[self.head_position] = new_symbol
            # Move the head
            self.head_position += 1 if move_direction == 'R' else -1
            # Update the machine's current state
            self.current_state = new_state

    def run(self):
        while not self.halted:
            self.step()

        # The machine halts, we consider it accepting if it's in the accepting state q4
        return self.current_state == 'q4'

# Let's test the Turing Machine with a string that should be accepted: '00011'
tm = TuringMachine('00011')
is_accepted = tm.run()
tape_output = ''.join(tm.tape).strip(tm.blank_symbol)  # Remove trailing blank symbols for display

is_accepted, tape_output
