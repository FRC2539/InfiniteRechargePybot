import constants

def init():
    
    try:    # Try to import the graphing library.
        import matplotlib.pyplot as plt
    except ImportError:
        print('Matplotlib is not installed. Cougar Courses graphs are therefore unavailable.')
        return 
    
    data = constants.drivetrain.coursesToGraph  # The courses to graph.
    
    t = [i * 0.01 for i in range(0, 100)]       # The 'x' of a standard, non-parametric equation.
    Xs, Ys = [], []
    
    for k, v in data.items():                   # Calculate the Xs and Ys for each course.
        resX, resY = [], []
        for i in t:
            result = v[0](i)
            resX.append(result[0])
            resY.append(result[1])
        Xs.append(resX)
        Ys.append(resY)
                
    for x, y, name in zip(Xs, Ys, list(data.values())):
        plt.plot(x, y, label=name)              # Plot all the courses.
            
    plt.title('Cougar Course Graphs')           # Set the graph setting.
    plt.xlabel('X-Axis')
    plt.ylabel('Y-Axis')
    plt.grid(alpha=0.1, linestyle='--')
    plt.legend()
    plt.xlim([-100, 100])
    plt.ylim([-100, 100])
    
    plt.show()                                  # Show the graph.