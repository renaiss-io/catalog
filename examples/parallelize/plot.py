import matplotlib.pyplot as plt
import re
import pdb

def read_data():
    # Open the file in read mode (default mode)
    with open('results.txt', 'r') as file:
        # Read the entire file content into a variable
        file_content = file.read()

    lines = file_content.strip().split("\n")

    # Initialize variables to calculate the average
    total_time = []
    total_workers = []
    total_time_mean = []
    total_workers_mean = []
    
    pattern_mean = r"Average time per execution of (\d+)  workers is : ([\d.]+) seconds"
    pattern = r"Number of workers: (\d+) Execution time: ([\d.]+) seconds" 

    for line in lines:
        match = re.search(pattern, line)
        match_mean = re.search(pattern_mean, line)

        if match:
            num_workers = int(match.group(1))
            execution_time = float(match.group(2))
            total_time.append(execution_time)
            total_workers.append(num_workers)

        if match_mean:
            num_workers = int(match_mean.group(1))
            execution_time = float(match_mean.group(2))
            total_time_mean.append(execution_time)
            total_workers_mean.append(num_workers)

    plt.scatter(total_workers,total_time,s=10)
    plt.plot(total_workers_mean,total_time_mean,label="Mean",color="red",lw=3)
    plt.axvline(x=8, color='red', linestyle='--', label='Maximun amount of cores at x=8')

    # Add labels and a title
    plt.xlabel('Number of threads', fontsize=15)
    plt.ylabel('Execution time [s]', fontsize=15)
    plt.title('Benchmarking parrallel queries using python', fontsize=15)
    plt.legend()
    plt.grid(True)
    plt.savefig("filepath.svg", format = 'svg', dpi=300)
    plt.show()  # Display the plot

# Call the read_data function to read and plot the data
read_data()
