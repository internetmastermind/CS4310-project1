

class Node:

    dv_packets = []
    path_list = []

    def __init__(self, name):
        self.name = str(name)
        self.routing_table = []
        self.neighbor_table = []
        self.rt_change = False
        self.msg_count = 0

    def __str__(self):
        return "Router Object" + self.name

    def __lt__(self, other):
        return int(self.name) < int(other.name)

    def print_routing_table(self):
        print(*self.routing_table, sep="\n")

    def print_routing_table_endsim(self):
        for each in self.routing_table:
            print(list(each.values()))

    def print_neighbor_table(self):
        print(self.neighbor_table)

    def add_routing_table_entry(self, dst, cost, next_hop):
        e = {"node": int(dst), "cost": int(cost), "next_hop": int(next_hop)}
        self.routing_table.append(e)

    def add_neighbor_table_entry(self, dst):
        self.neighbor_table.append(int(dst))

    def create_dv_packets(self):
        table = self.routing_table[:]
        for neighbor in self.neighbor_table:
            packet = {"src": self.name, "dst": neighbor, "dv_packet": table}
            self.dv_packets.append(packet)

    def process_dv_packet(self):
        if self.dv_packets:
            #print(len(self.dv_packets))
            #self.print_dv_packets_table()
            for packet in self.dv_packets[:]:
                #print("self.name = {0} dst = {1}".format(self.name, packet["dst"]))
                if str(self.name) == str(packet["dst"]):
                    #print("names equal")
                    #print("consult routing table")
                    self.consult_routing_table(packet["dv_packet"], packet["src"])
                    self.dv_packets.remove(packet)
                    #print("removed packet")
                    #print(len(self.dv_packets))

    def consult_routing_table(self, routing_table, sender):
        #print("printing routing table")
        #self.print_routing_table()
        cost = 0

        for x in self.routing_table:
            #print(str(x["node"]), str(sender))
            if str(x["node"]) == str(sender):
                cost = int(x["cost"])
                break

        for entry in routing_table:
            found = False
            for line in self.routing_table:
                #print("senders node entry = {0}  self node entry = {1}".format(entry["node"], line["node"]))
                if str(entry["node"]) == str(self.name):
                    found = True
                    continue

                if str(entry["node"]) == str(line["node"]):
                    found = True
                    #print(int(entry["cost"]) + int(cost), line["cost"])
                    #print(self.name, sender)
                    #print()
                    if (int(entry["cost"]) + int(cost)) < line["cost"]:
                        self.update_routing_table(line["node"], (int(entry["cost"]) + int(cost)), sender)
                        self.rt_change = True
                        found = True
                    elif (int(entry["cost"]) + int(cost)) == line["cost"]:
                        self.update_routing_table(line["node"], (int(entry["cost"]) + int(cost)), sender)
                        found = True

            if not found:
                self.add_routing_table_entry(entry["node"], (entry["cost"] + cost), sender)
                self.rt_change = True

    def update_routing_table(self, node, cost, next_hop):
        for entry in self.routing_table:
            if str(entry["node"]) == str(node):
                entry["cost"] = cost
                entry["next_hop"] = next_hop

    def print_dv_packets_table(self):
        print(*self.dv_packets, sep="\n")

    def get_rt_change(self):
        return self.rt_change

    def receive_packet(self, src, dst, nodes):
        if str(self.name) == str(dst):
            self.path_list.append(self.name)
            return
        else:
            for entry in self.routing_table:
                if str(entry["node"]) == str(dst):
                    self.forward_packet(src, dst, int(entry["next_hop"]), nodes)
                    self.path_list.append(self.name)

    def forward_packet(self, src, dst, next_hop, nodes):
        for node in nodes:
            if str(node.name) == str(next_hop):
                node.receive_packet(src, dst, nodes)