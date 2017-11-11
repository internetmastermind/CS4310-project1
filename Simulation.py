from Node import Node


class Simulation:
    node_list = []
    message_count = 0
    last = []

    def __init__(self, file_data, file_name):
        self.file_data = file_data
        self.file_name = file_name
        self.convergence = False
        self.round_number = 0
        self.msg = ""

    def send_packet(self, src, dst):
        nodes = self.node_list[:]
        self.node_list[src].receive_packet(src, dst, nodes)

    def find_last_converged_node(self):
        name = ""
        x = self.node_list[0]
        for node in self.node_list:
            if node.rt_change:
                x = node
        name = x.name

        return name

    def return_path_list(self):
        length = len(self.node_list[0].path_list)
        msg = ""
        for index in range(0, length):
            if index != length-1:
                msg += "{0} ---->".format(self.node_list[0].path_list[(length - 1) - index])
            else:
                msg += "{0}".format(self.node_list[0].path_list[(length - 1) - index])

        return msg

    def create_routers(self):
        routers = []

        for line in self.file_data:
            src = int(line["node1"])
            dst = int(line["node2"])
            cost = int(line["cost"])

            if src not in routers:
                router = Node(src)
                router.add_routing_table_entry(dst, cost, dst)
                router.add_neighbor_table_entry(dst)

                self.node_list.append(router)
                routers.append(src)
            elif src in routers:
                for index, r in enumerate(self.node_list):
                    if int(r.name) == src:
                        self.node_list[index].add_routing_table_entry(dst, cost, dst)
                        self.node_list[index].add_neighbor_table_entry(dst)

            if dst not in routers:
                router = Node(dst)
                router.add_routing_table_entry(src, cost, src)
                router.add_neighbor_table_entry(src)

                self.node_list.append(router)
                routers.append(dst)
            elif dst in routers:
                for index, r in enumerate(self.node_list):
                    if int(r.name) == dst:
                        self.node_list[index].add_routing_table_entry(src, cost, src)
                        self.node_list[index].add_neighbor_table_entry(src)

        # Sort for later
        self.node_list.sort()

    def start_simulation(self, rounds=100):
        x = 0
        while x < rounds:
            if not self.convergence:
                for node in self.node_list:
                    node.create_dv_packets()
                self.message_count += len(self.node_list[0].dv_packets)

                #print("round " + str(rounds))
                #print("dv_packets table")
                #self.node_list[1].print_dv_packets_table()

                for node in self.node_list:
                    node.process_dv_packet()

                #print("\n")
                #print("Routing Tables")
                #for node in self.node_list:
                    #node.print_routing_table()
                #print("\n")

                change_made = False
                for node in self.node_list:
                    if node.get_rt_change():
                        change_made = True

                if change_made:
                    self.convergence = False
                else:
                    self.convergence = True

                last_node = self.find_last_converged_node()
                self.last.append(last_node)

                for node in self.node_list:
                    node.rt_change = False

                x += 1
            else:
                print("Converged after " + str(x) + " rounds.... THANK GOD")
                break

        if not self.convergence:
            print("Not enough rounds to converge")
        else:
            if self.file_name.lower() == "topology1.txt":
                # node 0 receives packet destined to node 3
                self.msg = "\nNode 0 receives packet destined to node 3"
                src = 0
                dst = 3
                self.send_packet(src, dst)
            elif self.file_name.lower() == "topology2.txt":
                # node 0 receives packet destined to node 7
                self.msg = "\nNode 0 receives packet destined to node 7"
                src = 0
                dst = 7
                self.send_packet(src, dst)
            elif self.file_name.lower() == "topology3.txt":
                # node 0 receives packet destined to node 23
                self.msg = "\nNode 0 receives packet destined to node 23"
                src = 0
                dst = 23
                self.send_packet(src,dst)

        print("Total Messages Sent: " + str(self.message_count))
        print("Last Node to Converge: " + str(self.last[len(self.last) - 2]))
