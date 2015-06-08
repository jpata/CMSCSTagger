class SKLearnClassifier:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.data_name = kwargs.get("data_name")
        self.mva_name = "bdt_" + self.name + "_" + self.data_name

        self.variables = kwargs.get("variables")
        self.spectators = kwargs.get("spectators", [])

        self.ntrees = kwargs.get("ntrees", 1200)
        self.shrinkage = kwargs.get("shrinkage", 0.1)
        self.bag_fraction = kwargs.get("bag_fraction", 0.5)
        self.ncuts = kwargs.get("ncuts", 50)
        self.max_depth = kwargs.get("max_depth", 1)
        self.data_classes = kwargs.get("data_classes", [])
        self.subsample = kwargs.get("subsample", 1.0)
        self.max_events = kwargs.get("max_events", None)
        self.min_samples_split = kwargs.get("min_samples_split", 100)
        self.min_samples_leaf = kwargs.get("min_samples_leaf", 100)
        
        self.weight = kwargs.get("weight", None)
        self.label_signal = kwargs.get("label_signal", None)
        
        self.data = OrderedDict()
        self.class_id = 0

    def prepare(self):
        self.cls = GradientBoostingClassifier(
            n_estimators=self.ntrees, learning_rate=self.shrinkage,
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            min_samples_leaf=self.min_samples_leaf,
            subsample=self.subsample,
            verbose=True
        )
    
    def add_data(self, data):
        d = pandas.DataFrame(
            data[self.variables+["w"]]
        )
        d["id"] = self.class_id
        self.class_id += 1
        self.data[class_name] = d
        
    def train(self):
        ks = self.data.keys()
        tot = pandas.concat(
            [self.data[k] for k in ks], ignore_index=True
        )
        self.cls.fit(tot[self.variables], tot["id"], tot["w"])

    def cumulative(self, classifier, cls):
        return cum(self.data[cls][classifier])
    
    def evaluate(self, data, nprob=0):
        inp = copy.deepcopy(data[self.variables])
        inp[np.isnan(inp)] = 0.0
        inp[np.isinf(inp)] = 0.0
        ret = self.cls.predict_proba(inp)[:, nprob]
        ret[np.isnan(ret)] = 0.0
        ret[np.isinf(ret)] = 0.0
        return ret
    
    def plot_roc(self, data):
        
        ch0b = cum(self.evaluate(data[data["id"] == 2]))
        ch0c = cum(self.evaluate(data[data["id"] == 1]))
        ch0l = cum(self.evaluate(data[data["id"] == 0]))

        plt.figure(figsize=(10,5))
        ax1 = plt.subplot(1,2,1)
        plt.plot(
            1.0 - ch0b, 1.0 - ch0l, lw=2, color="black", ls="-",
            label="c {0:.4f}".format(metrics.auc(1.0 - ch0b, 1.0 - ch0l))
        )
#         plt.plot(1.0 - ch0t, 1.0 - ch1t, lw=2, color="black", ls="--",
#             label="T AUC={0:.4f}".format(metrics.auc(1.0 - ch0t, 1.0 - ch1t))
#         )
        
        c1b = cum(data[data["id"]==2]["bd_csv1"])
        c1c = cum(data[data["id"]==1]["bd_csv1"])
        c1l = cum(data[data["id"]==0]["bd_csv1"])
        
        plt.plot(1.0 - c1b,
                 1.0 - c1l, color="red",
                 label="AVR {0:.4f}".format(metrics.auc(1.0 - c1b, 1.0 - c1l))
        )
        
        c2b = cum(data[data["id"]==2]["bd_csv2"])
        c2c = cum(data[data["id"]==1]["bd_csv2"])
        c2l = cum(data[data["id"]==0]["bd_csv2"])
        
        plt.plot(1.0 - c2b,
                 1.0 - c2l, color="green",
                 label="IVF {0:.4f}".format(metrics.auc(1.0 - c2b, 1.0 - c2l))
        )
        plt.yscale("log")
        plt.grid()
        plt.xlim(0,1)
        plt.ylim(0.0001, 1.0)
        plt.xlabel("b eff", fontsize=16)
        plt.ylabel("udsg eff", fontsize=16)
        plt.legend(loc=4)
        
        plt.text(0.05,0.94,
            "at $\epsilon_b \simeq$ 0.7",
            transform=ax1.transAxes,
            fontsize=16
        )
        plt.text(0.05,0.89,
            "$\epsilon_l$={0:.4f}".format(1.0 - ch0l[ch0b.searchsorted(0.3)]),
            transform=ax1.transAxes,
            fontsize=12
        )
        plt.text(0.05,0.84,
            "$\epsilon_l$={0:.4f}".format(1.0 - c1l[c1b.searchsorted(0.3)]),
            transform=ax1.transAxes,
            fontsize=12, color="red"
        )
        plt.text(0.05,0.79,
            "$\epsilon_l$={0:.4f}".format(1.0 - c2l[c2b.searchsorted(0.3)]),
            transform=ax1.transAxes,
            fontsize=12, color="green"
        )
        
        plt.text(0.05,0.7,
            "at $\epsilon_b \simeq$ 0.5",
            transform=ax1.transAxes,
            fontsize=16
        )
        plt.text(0.05,0.65,
            "$\epsilon_l$={0:.4f}".format(1.0 - ch0l[ch0b.searchsorted(0.5)]),
            transform=ax1.transAxes,
            fontsize=12
        )
        plt.text(0.05,0.6,
            "$\epsilon_l$={0:.4f}".format(1.0 - c1l[c1b.searchsorted(0.5)]),
            transform=ax1.transAxes,
            fontsize=12, color="red"
        )
        plt.text(0.05,0.55,
            "$\epsilon_l$={0:.4f}".format(1.0 - c2l[c2b.searchsorted(0.5)]),
            transform=ax1.transAxes,
            fontsize=12, color="green"
        )
        
        ax2 = plt.subplot(1,2,2)
        plt.plot(
            1.0 - ch0b, 1.0 - ch0c, lw=2, color="black", ls="-",
            label="c {0:.4f}".format(metrics.auc(1.0 - ch0b, 1.0 - ch0c))
        )
#         plt.plot(1.0 - ch0t, 1.0 - ch1t, lw=2, color="black", ls="--",
#             label="T AUC={0:.4f}".format(metrics.auc(1.0 - ch0t, 1.0 - ch1t))
#         )

        plt.plot(1.0 - c1b,
                 1.0 - c1c, color="red",
                 label="AVR {0:.4f}".format(metrics.auc(1.0 - c1b, 1.0 - c1c))
        )

        plt.plot(1.0 - c2b,
                 1.0 - c2c, color="green",
                 label="IVF {0:.4f}".format(metrics.auc(1.0 - c2b, 1.0 - c2c))
        )

        plt.text(0.05,0.94,
            "at $\epsilon_b \simeq$ 0.7",
            transform=ax2.transAxes,
            fontsize=16
        )
        plt.text(0.05,0.89,
            "$\epsilon_c$={0:.4f}".format(1.0 - ch0c[ch0b.searchsorted(0.3)]),
            transform=ax2.transAxes,
            fontsize=12
        )
        plt.text(0.05,0.84,
            "$\epsilon_c$={0:.4f}".format(1.0 - c1c[c1b.searchsorted(0.3)]),
            transform=ax2.transAxes,
            fontsize=12, color="red"
        )
        plt.text(0.05,0.79,
            "$\epsilon_c$={0:.4f}".format(1.0 - c2c[c2b.searchsorted(0.3)]),
            transform=ax2.transAxes,
            fontsize=12, color="green"
        )
        
        plt.text(0.05,0.7,
            "at $\epsilon_b \simeq$ 0.5",
            transform=ax2.transAxes,
            fontsize=16
        )
        plt.text(0.05,0.65,
            "$\epsilon_c$={0:.4f}".format(1.0 - ch0c[ch0b.searchsorted(0.5)]),
            transform=ax2.transAxes,
            fontsize=12
        )
        plt.text(0.05,0.6,
            "$\epsilon_c$={0:.4f}".format(1.0 - c1c[c1b.searchsorted(0.5)]),
            transform=ax2.transAxes,
            fontsize=12, color="red"
        )
        plt.text(0.05,0.55,
            "$\epsilon_c$={0:.4f}".format(1.0 - c2c[c2b.searchsorted(0.5)]),
            transform=ax2.transAxes,
            fontsize=12, color="green"
        )
        
        plt.yscale("log")
        plt.grid()
        plt.xlim(0,1)
        plt.ylim(0.0001, 1.0)
        plt.xlabel("b eff", fontsize=16)
        plt.ylabel("c eff", fontsize=16)
        plt.legend(loc=4)
