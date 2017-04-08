from pixel import Pixel

class Graph:
    def argsort(seq):
        "Sort an array and return the permutation array"
       #http://stackoverflow.com/questions/3382352/equivalent-of-numpy-argsort-in-basic-python/3382369#3382369
        return sorted(range(len(seq)), key=seq.__getitem__)
    
    def __init__(this, size,type):
        "Graph(size,type) : create image graph of size [x,y] of a certain type"
        types = {'triagonal', this.genTreGraph,
                 'square', this.genSquareImage}
        return types[type](size)
    
    def __init__(this,filename):
        "Graph(filename): Read graph from file."
        this.nodes = []
        with open(filename) as f:
            for line in f:
                NIDs = []
                NDirs = []
                NDists = []
                split1 = line.rstrip('\n').split(":");
                if len(split1) != 2:
                    raise ValueError("expected an ID followed by a colon and its neighbors per line.")
                try:
                    newID = int(split1[0]);
                except ValueError:
                    raise ValueError("Not a valid ID given"+split1[0]+".")
                split1[1] = split1[1].strip().rstrip()
                for neighborblock in split1[1].split(" "):
                    values = neighborblock.strip().rstrip().split("|")
                    # [0] ID
                    try:
                        NIDs.append(int(values[0]))
                    except ValueError:
                        raise ValueError("Not a valid ID for next neighbor"+values[0]+".")
                    #[1] Winkel
                    try:
                        NDirs.append(float(values[1]))
                    except ValueError:
                        raise ValueError("No valid angle given for next neighbor #"+nextNID+".")
                    if len(values)>2:
                        try:
                            NDists.append(float(values[2]))
                        except ValueError:
                            raise ValueError("No valid distance for next neighbor #"+nextNID+".")
                    else:
                        NDists.append(1)
                this.nodes.append(Pixel(newID,NIDs,NDirs,NDists))

    def __repr__(this):
        Descr = "A Graph with nodes\n"
        for n in this.nodes:
            Descr += str(n)+"\n"
        return Descr