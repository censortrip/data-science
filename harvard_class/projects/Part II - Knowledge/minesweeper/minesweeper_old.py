import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines

# Just supposed to track surrounding vlues of a selected cell 
# for future guesses
class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        self.safe_cells = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return(self.safe_cells)

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        self.safe_cells.add(cell)
        self.cells.remove(cell)

# this keeps track of same mines, safe cells, and knowelde base
# note that, safe mines and 
class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width
        
        # All available moves at start of game
        self.available_moves = set()
          
        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []


    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        if len(self.knowledge) != 0:
            for sentence in self.knowledge:
                sentence.mark_safe(cell)
    
    # STARTING POINT FROM runner.py, if move made is valid
    # and not game over, it gets passed into here. 
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            fin 
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # 0. Get surrounding cells for cell
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself and any erroneous cells
                # that don't fall in the range (like (-1, -1) )

                # MORE LOGIC HAS TO BE ADDED IN ORDER TO AVOID ADDING
                # NEGIHBORS THAT HAVE ALREADY BEEN TRAVERSED, CHECK
                # self.mines and self.safes FOR THIS
                if (i, j) == cell or i < 0 or j < 0 or i >= 8 or j >= 8:
                    continue
                else:
                    neighbors.add((i,j))

     
        # 1. Add and remove cell as necessary from moves_made, available_moves,
        self.moves_made.add(cell)
        
        if len(self.available_moves) > 0:
            self.available_moves.remove(cell)
        if cell in self.safes: 
            self.safes.remove(cell)

        print(f'Available Moves: {self.available_moves}')       
        print(f'Moves Made: {self.moves_made}')

        # 2. Mark the cell as safe
        if count == 0:
            for neighbor in neighbors:
                if neighbor not in self.moves_made:
                    self.mark_safe(neighbor)
        print(f'Safe Cells: {self.safes}')

        # 3. Add a new sentence to the AI's knowledge base based on the 
        #    value of `cell` and `count`.

        # 3b. Update KB with new sentence if necessary
        #     Note: sentences are only created if cell value > 0 and 
        #           as long as count != number of neighbors (means all mines)
        if count == 0 or len(neighbors) == count:
            print('DONT NEED TO CREATE A SENTENCE')             
        else: 
            print('NEED TO CREATE A SENTENCE')
            print(f'COUNT AROUND CELL: {count}') 

        

        if len(self.knowledge) > 0:

            # If there are sentences in KB, check each one for current cell,
            # if cell is found, remove it as it is no longer a possible threat
            for sentence in self.knowledge:
                 print(f'SENTENCE KNOWN SAFE CELLS: {sentence.safe_cells}')
#                if cell in sentence:
#                    sentence.remove(cell)
#                                        
#
#            # 2. NEXT, LOOP THROUGH NEIGHBORS AND ONLY ADD THE ONES NOT IN moves_made TO THE SENTENCE
#            for neighbor in neighbors:
#                if neighbor not in self.moves_made:
                
              
            
#            for sentence in self.knowledge:         
#                print(f'Sentence: {sentence}')
#                print(f'Current Cell Value: {sentence.count}')
                  
        else:
            self.knowledge.append(Sentence(neighbors,count))
 

        # 3c. Update self.safes as necessary
#        if count == 0:
#            # add all cell neighbors to self.safes
#            
#            for cel in neighbors:
#                self.safes.add(cel)

        print(f'Safe Cells Updated: {self.safes}')
  

        # 3d. Update self.mines as necessary
        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) == 0:
            return None
        else:
            for c in self.safes:
                if c not in self.moves_made:
                    return(c)
                    break
        

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        # If KB is empty, make random move
        if len(self.available_moves) == 0:
            for i in range(0, self.height):
                for j in range(0, self.height):
                    self.available_moves.add((i,j))

        return(random.choice(list(self.available_moves)))
        
