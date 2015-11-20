# -*- coding: ISO-8859-1 -*-
"""Game of Life."""

# (C) Juha Kari 2015.

import copy

class InvalidCellReference(Exception):
    """Class representing an invalid cell reference exception."""
    def __init_(self, msg):
        self.msg = msg

class Grid:
    """Class representing a grid."""
    
    # Ruudukon sarakkeiden määrä.
    x_size = 0
    # Ruudukon rivien määrä.
    y_size = 0
    # Ruudukon esittämän sukupolven numero (0 = alkutilanne).
    generation = 0
    # Ruudukko alustetaan tyhjäksi.
    cells = [ ]
    # Viittaus vanhaan ruudukkoon on alussa tyhjä.
    old_grid = 0
    
    def __init__(self, x = 5, y = 5):
        """Initialize the grid."""
        self.reset(x, y)
    
    def reset(self, x = 5, y = 5):
        """Reset the grid."""
        self.x_size = x
        self.y_size = y
        self.generation = 0
        self.cells = [0 for i in range(x*y)]
        self.old_grid = copy.deepcopy(self)

    def set_cell(self, x, y):
        """Mark the given cell as alive."""
        if x >= 0 and x < self.x_size and y >= 0 and y < self.y_size:
            self.cells[y * self.x_size + x] = 1
        else:
            err = "Coordinates must be x = [%i, %i] and y = [%i, %i]"\
                % (0, self.x_size-1, 0, self.y_size-1)
            raise InvalidCellReference(err)
    
    def set_cells(self, cells):
        """Mark the list of cells as alive."""
        for c in cells:
            (x, y) = c
            self.set_cell(x, y)
    
    def reset_cell(self, x, y):
        """Mark the given cell as dead."""
        if x >= 0 and x < self.x_size and y >= 0 and y < self.y_size:
            self.cells[y * self.x_size + x] = 0
        else:
            err = "Coordinates must be x = [%i, %i] and y = [%i, %i]"\
                % (0, self.x_size-1, 0, self.y_size-1)
            raise InvalidCellReference(err)
    
    def reset_cells(self, cells):
        """Mark the list of cells as dead."""
        for c in cells:
            (x, y) = c
            self.reset_cell(x, y)
    
    def is_alive(self, x, y):
        """Check if the cell at given coordinates is alive."""
        if x >= 0 and x < self.x_size and y >= 0 and y < self.y_size:
            pass
        else:
            err = "Coordinates must be x = [%i, %i] and y = [%i, %i]"\
                % (0, self.x_size-1, 0, self.y_size-1)
            raise InvalidCellReference(err)
        
        return self.cells[y * self.x_size + x]
    
    def count_neighbors(self, x, y):
        """Return the number of living neighbor cells."""
        n = 0
        for y_delta in range(-1, 2):
            for x_delta in range(-1, 2):
                if x_delta == 0 and y_delta == 0:
                    pass
                else:
                    try:
                        if self.is_alive(x + x_delta, y + y_delta):
                            n += 1
                    except:
                        pass
        return n
    
    def evolve(self, generations = 1, show = True):
        """Evolve a given number of generations."""
        print("Evolving", generations, "generations...")
        for i in range(generations):
            self.generation += 1
            
            self.old_grid = copy.deepcopy(self)
            
            for y in range(self.y_size):
                for x in range (self.x_size):
                    neighbors = self.old_grid.count_neighbors(x, y)
                    if self.old_grid.is_alive(x, y):
                        if neighbors <= 1:
                            self.reset_cell(x, y)
                        elif neighbors > 3:
                            self.reset_cell(x, y)
                        else:
                            pass
                    else:
                        if neighbors == 3:
                            self.set_cell(x, y)
                        else:
                            pass
            
            if show:
                print(i+1, "OK. (", self.generation, ")")
                self.show()
    
    def show(self, output_format = "grid"):
        """Show the grid in given format."""
        # Jos parametrina saatu output_format ei ole kelvollinen,
        # asetetaan sen arvoksi "grid".
        if not output_format in ("grid", "list"):
            output_format = "grid"
        
        if output_format == "grid":
            for y in range(self.y_size):
                for x in range(self.x_size):
                    #print "(", x, ",", y, ")",
                    print(self.cells[y * self.x_size + x], end=' ')
                print()
        elif output_format == "list":
            for z in range(self.x_size * self.y_size):
                #print "(", x, ",", y, ")",
                print(self.cells[z], end=' ')
            print()

if __name__ == "__main__":
    """The main functionality of the Game of Life."""
    # Luodaan uusi ruudukko.
    g = Grid()
    
    # Lista elävistä soluista.
    
    # Esimerkki #1
    #living_cells = [(1,1), (3,1), (2,2)]
    
    # Still live
    #living_cells = [(1,1), (2,1), (1,2), (2, 2)]
    
    # Oscillator
    living_cells = [(1,2), (2, 2), (3, 2)]
    
    # Glider
    #living_cells = [(3,1), (1,2), (3, 2), (2, 3), (3, 3)]
    
    # Suoritettavien kehitysaskeleiden määrä.
    generations = 7
    
    # Tulostetaanko ruudukko jokaisen kehitysaskeleen jälkeen?
    show_all_generations = False
    
    # Herätetään listan mukaiset solut henkiin.
    g.set_cells(living_cells)
    
    # Tulostetaan aluksi ruudukko listamuodossa.
    print("Cells of generation %i in list format:" % (g.generation))
    g.show(output_format="list")
    
    # Tulostetaan (2,2):n naapurien määrä.
    print("Neighbors of (2,2) =", g.count_neighbors(2,2))
    
    # Tulostetaan ruudukon alkutilanne.
    g.show()
    
    # Suoritetaan annettu määrä kehitysaskeleita.
    g.evolve(generations, show_all_generations)
    
    # Tulostetaan ruudukon lopputilanne tarpeen vaatiessa.
    if not show_all_generations:
        g.show()
    
    # Tulostetaan (2,2):n naapurien määrä.
    print("Neighbors of (2,2) =", g.count_neighbors(2,2))
    
    # Tulostetaan vielä lopuksi ruudukko listamuodossa.
    print("Cells of generation %i in list format:" % (g.generation))
    g.show(output_format="list")
    
