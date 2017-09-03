from .Pixel import Pixel

class Graph:
    def argsort(seq):
        "Sort an array and return the permutation array"
       #http://stackoverflow.com/questions/3382352/equivalent-of-numpy-argsort-in-basic-python/3382369#3382369
        return sorted(range(len(seq)), key=seq.__getitem__)

    def __init__(this, var=None):
        if isinstance(var,dict):
            this.nodes = var
        elif isinstance(var,Graph):
            this.nodes = var.nodes;
        else:
            this.nodes = {}

    @classmethod
    def load(this,fn):
        """Graph.load(fn) – load a graph from the file fn in the format
        one line per node with its neighbors (direction/distance),
        $Node: $NeighborID1|Direction|Distance $NeighborID2|Direction|Distance
        """
        nodes = dict()
        with open(fn) as f:
            for line in f:
                NDirs = {}
                NDists = {}
                split1 = line.rstrip('\n').split(":");
                if len(split1) != 2:
                    raise ValueError("expected an ID followed by a colon and its neighbors per line.")
                try:
                    newID = int(split1[0]);
                    #print()
                    #print(newID)
                    #print("---")
                except ValueError:
                    raise ValueError("Not a valid ID given"+split1[0]+".")
                split1[1] = split1[1].strip().rstrip()
                for neighborblock in split1[1].split(" "):
                    values = neighborblock.strip().rstrip().split("|")
                    # [0] ID
                    try:
                        NID = int(values[0])
                        #print(NID)
                    except ValueError:
                        raise ValueError("Not a valid ID for next neighbor"+str(values[0])+".")
                    #[1] Winkel
                    try:
                        NDirs[NID] = (float(values[1]))
                    except ValueError:
                        raise ValueError("No valid angle given for next neighbor #"+str(NID)+".")
                    if len(values)>2:
                        try:
                            NDists[NID] = (float(values[2]))
                        except ValueError:
                            raise ValueError("No valid distance for next neighbor #"+str(NID)+".")
                    else:
                        NDists[NID] = 1
                nodes[newID] = Pixel(newID,NDirs,NDists)
        g = this(nodes)
        return g

    def getPixel(this,ID):
        if ID in this.nodes:
            return this.nodes[ID]
        else:
            return None

    def permute(this,permutation):
        oldnodes = this.nodes
        this.nodes = dict()
        for k,n in oldnodes.items():
            newID = permutation[k]
            NDirs = {}
            NDists = {}
            for k2 in n.getNeighborIDs():
                NDists[permutation[k2]] = oldnodes[k].neighborDistance[k2]
                NDirs[permutation[k2]] = oldnodes[k].neighborDirection[k2]
            this.nodes[newID] = Pixel(newID,NDirs,NDists)

    def __add__(this,graph):
        """adds pixel of same node IDs
        """
        g = Graph(this)
        for k in this.nodes.keys():
            g.nodes[k] += graph.nodes[k]
        return g
    def __iadd__(this,graph):
        for k in this.nodes.keys():
            this.nodes[k] += graph.nodes[k]
    def __mul__(this,graph):
        """multiplies pixel of same node IDs
        """
        g = Graph(this)
        for k in this.nodes.keys():
            g.nodes[k] *= graph.nodes[k]
        return g
    def __imul__(this,graph):
        for k in this.nodes.keys():
            this.nodes[k] *= graph.nodes[k]

    def getNumNodes(this):
        return len(this.nodes)

    def setBlack(this):
        for k,n in this.nodes.items():
            n.setColor([0,0,0])

    def __repr__(this):
        Descr = "A Graph with nodes\n"
        for k,n in this.nodes.items():
            Descr += str(n)+"\n"
        return Descr

    def clone(this):
        g = Graph(this)
        g.nodes = dict()
        for k in this.nodes.keys():
            g.nodes[k] = this.nodes[k].clone()
        return g
