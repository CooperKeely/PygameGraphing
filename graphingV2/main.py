from function import function
from graph import graph
import numpy as np

def main():
    grid = graph(1000, 1000, 100)

    func2 = function(np.sin)
    func3 = function(np.log)

    grid.add_function(func2)
    grid.add_function(func3)

    grid.loop()

if __name__ == "__main__":
    main()