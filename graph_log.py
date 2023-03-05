import matplotlib.pyplot as plt

def graph (str):
    with open(str) as f:
        lines = [i.strip().split(',') for i in f.readlines() if i.strip()]
    # print(*lines, sep='\n')
    print(lines[1][0])
    input_range = range(0, len(lines))
    prog1_time = []
    for i in input_range:
        tmp = int(lines[i][0].split("with logical clock time ")[1].split(".")[0])
        prog1_time.append(tmp)

    print("prog1 is",prog1_time)
    prog2_time = []
    plt.plot(input_range, prog1_time, label="vm0_03-02_13-46-46_clock_rate_2_log.txt")
    plt.xlabel('Action')
    plt.ylabel('Logical clock value')
    plt.legend()
    plt.savefig('logical clock value jump.png', bbox_inches = "tight")
    plt.show()
graph('virtual_machine_0_logs/vm0_03-02_13-46-46_clock_rate_2_log.txt')
graph('virtual_machine_0_logs/vm0_03-02_12-58-56_clock_rate_3_log.txt')