import ROOT
import array

def array2root(arr,
    filename,
    treename,
    colnames=None,
    command="recreate"
    ):

    of = ROOT.TFile(filename, command)
    of.cd()
    tree = ROOT.TTree(treename, treename)
    if len(arr.shape)==1:
        nevs = len(arr)
        ncols = 1
        arr = arr.reshape((nevs, ncols))
    elif len(arr.shape)==2:
        nevs, ncols = arr.shape

    if not colnames:
        colnames = ["br"+str(i) for i in range(ncols)]

    branchvars = {}
    for col in range(ncols):
        brname = colnames[col]
        branchvars[col] = array.array("f", [0.0])
        tree.Branch(
            brname,
            branchvars[col],
            "{0}/F".format(brname)
        )

    nf = 0
    for i in range(nevs):
        for col in range(ncols):
            branchvars[col][0] = float(arr[i, col])
        nf += tree.Fill()

    tree.Write("", ROOT.TObject.kOverwrite)
    of.Close()
    return
    
def root2array(
    filename,
    treename,
    colnames=None,
    ):

    assert(os.path.isfile(filename))
    of = ROOT.TFile(filename)
    tree = of.Get(treename)
    assert(tree != None)

    nevs = tree.GetEntries()
    ncols = len(colnames)

    branchvars = {}
    #tree.SetBranchStatus("*", False)

    arr = np.zeros((nevs, ncols), dtype="f")

    for col in range(ncols):
        brname = colnames[col]
        cn = tree.GetBranch(brname).GetListOfLeaves().At(0).GetTypeName()
        #print cn
        if cn == "Int_t":
            t = "i"
        elif cn == "Float_t":
            t = "f"
        branchvars[col] = array.array(t, [0])
        tree.SetBranchAddress(
            brname,
            branchvars[col],
        )
        #tree.SetBranchStatus(brname, True)

    nf = 0
    for i in range(nevs):
        nf += tree.GetEntry(i)
        #if i<10:
        #    print [branchvars[col][0] for col in range(ncols)]
        for col in range(ncols):
            arr[i, col] = branchvars[col][0]

    #print nf
    return arr
