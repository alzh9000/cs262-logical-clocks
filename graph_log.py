import matplotlib.pyplot as plt

def graph (str_list):
    result = []
    for elt in str_list:
        with open(elt) as f:
            lines = [i.strip().split(',') for i in f.readlines() if i.strip()]
        # print(*lines, sep='\n')
        print(lines[1][0])
        input_range = range(0, len(lines))
        prog1_time = []
        for i in input_range:
            tmp = int(lines[i][0].split("with logical clock time ")[1].split(".")[0])
            prog1_time.append(tmp)
        result.append(prog1_time)
    for i in range(len(result)):
        plt.plot(range(0,len(result[i])), result[i], label="machine" + str(i))
    plt.xlabel('ith line of log')
    plt.ylabel('Logical clock value')
    plt.legend()
    plt.savefig('logical_clock_value_jump.png', bbox_inches = "tight")
    plt.show()
graph(['virtual_machine_0_logs/vm0_03-04_22-55-36_clock_rate_2_log.txt','virtual_machine_1_logs/vm1_03-04_22-55-36_clock_rate_4_log.txt','virtual_machine_2_logs/vm2_03-04_22-55-36_clock_rate_3_log.txt'])