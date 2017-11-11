from Simulation import Simulation
import sys

file_data = []
file_name = str(sys.argv[1])
num_of_rounds = int(sys.argv[2])


def read_file():
    try:
        f = open(file_name, "r")

        for line in f.readlines():
            data = line.rstrip("\n").split("\t")
            n = {"node1": data[0], "node2": data[1], "cost": data[2]}
            file_data.append(n)

        f.close()
    except Exception as error:
        print("Error reading file.")
        print(error)


# print(*file_data,sep="\n")
print("Starting....")

read_file()
sim = Simulation(file_data, sys.argv[1])
sim.create_routers()
sim.start_simulation(num_of_rounds)

for node in sim.node_list:
    print("\nNode " + str(node.name) + "'s routing table")
    print("-------------------------")
    node.print_routing_table_endsim()

print(sim.msg)
print("This is the route:")
print(sim.return_path_list())
