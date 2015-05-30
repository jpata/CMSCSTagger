class BHadrons:
  def __init__(self, tree, i):
    self.eta = tree.BHadron_eta[i]
    self.hasBdaughter = tree.BHadron_hasBdaughter[i]
    self.nCharged = tree.BHadron_nCharged[i]
    self.pdgID = tree.BHadron_pdgID[i]
    self.mass = tree.BHadron_mass[i]
    self.pT = tree.BHadron_pT[i]
    self.DHadron1 = tree.BHadron_DHadron1[i]
    self.DHadron2 = tree.BHadron_DHadron2[i]
    self.mother = tree.BHadron_mother[i]
    self.SVy = tree.BHadron_SVy[i]
    self.SVx = tree.BHadron_SVx[i]
    self.SVz = tree.BHadron_SVz[i]
    self.phi = tree.BHadron_phi[i]
  types = {
    'eta': 'Float_t',
    'hasBdaughter': 'Int_t',
    'nCharged': 'Int_t',
    'pdgID': 'Int_t',
    'mass': 'Float_t',
    'pT': 'Float_t',
    'DHadron1': 'Int_t',
    'DHadron2': 'Int_t',
    'mother': 'Int_t',
    'SVy': 'Float_t',
    'SVx': 'Float_t',
    'SVz': 'Float_t',
    'phi': 'Float_t',
  }

  @staticmethod
  def make_array(tree):
    return [BHadrons(tree, i) for i in range(tree.nBHadrons)]

class BitTrigger:
  def __init__(self, tree, i):
    self.BitTrigger = tree.BitTrigger[i]
  types = {
    'BitTrigger': 'Int_t',
  }

  @staticmethod
  def make_array(tree):
    return [BitTrigger(tree, i) for i in range(tree.nBitTrigger)]

class DHadrons:
  def __init__(self, tree, i):
    self.eta = tree.DHadron_eta[i]
    self.mass = tree.DHadron_mass[i]
    self.pT = tree.DHadron_pT[i]
    self.SVz = tree.DHadron_SVz[i]
    self.SVy = tree.DHadron_SVy[i]
    self.SVx = tree.DHadron_SVx[i]
    self.nDaughters = tree.DHadron_nDaughters[i]
    self.nChargedDaughters = tree.DHadron_nChargedDaughters[i]
    self.nCharged = tree.DHadron_nCharged[i]
    self.pdgID = tree.DHadron_pdgID[i]
    self.phi = tree.DHadron_phi[i]
  types = {
    'eta': 'Float_t',
    'mass': 'Float_t',
    'pT': 'Float_t',
    'SVz': 'Float_t',
    'SVy': 'Float_t',
    'SVx': 'Float_t',
    'nDaughters': 'Int_t',
    'nChargedDaughters': 'Int_t',
    'nCharged': 'Int_t',
    'pdgID': 'Int_t',
    'phi': 'Float_t',
  }

  @staticmethod
  def make_array(tree):
    return [DHadrons(tree, i) for i in range(tree.nDHadrons)]

class Daughters:
  def __init__(self, tree, i):
    self.DaughtersPdgID = tree.DHadron_DaughtersPdgID[i]
  types = {
    'DaughtersPdgID': 'Int_t',
  }

  @staticmethod
  def make_array(tree):
    return [Daughters(tree, i) for i in range(tree.nDaughters)]

class GenPruned:
  def __init__(self, tree, i):
    self.eta = tree.GenPruned_eta[i]
    self.mass = tree.GenPruned_mass[i]
    self.pdgID = tree.GenPruned_pdgID[i]
    self.mother = tree.GenPruned_mother[i]
    self.phi = tree.GenPruned_phi[i]
    self.pT = tree.GenPruned_pT[i]
    self.status = tree.GenPruned_status[i]
  types = {
    'eta': 'Float_t',
    'mass': 'Float_t',
    'pdgID': 'Int_t',
    'mother': 'Int_t',
    'phi': 'Float_t',
    'pT': 'Float_t',
    'status': 'Int_t',
  }

  @staticmethod
  def make_array(tree):
    return [GenPruned(tree, i) for i in range(tree.nGenPruned)]

class GenV0:
  def __init__(self, tree, i):
    self.nCharged = tree.GenV0_nCharged[i]
    self.pdgID = tree.GenV0_pdgID[i]
    self.pT = tree.GenV0_pT[i]
    self.SVy = tree.GenV0_SVy[i]
    self.SVx = tree.GenV0_SVx[i]
    self.SVz = tree.GenV0_SVz[i]
    self.eta = tree.GenV0_eta[i]
    self.phi = tree.GenV0_phi[i]
  types = {
    'nCharged': 'Int_t',
    'pdgID': 'Int_t',
    'pT': 'Float_t',
    'SVy': 'Float_t',
    'SVx': 'Float_t',
    'SVz': 'Float_t',
    'eta': 'Float_t',
    'phi': 'Float_t',
  }

  @staticmethod
  def make_array(tree):
    return [GenV0(tree, i) for i in range(tree.nGenV0)]

class Genlep:
  def __init__(self, tree, i):
    self.pdgID = tree.Genlep_pdgID[i]
    self.pT = tree.Genlep_pT[i]
    self.mother = tree.Genlep_mother[i]
    self.status = tree.Genlep_status[i]
    self.phi = tree.Genlep_phi[i]
    self.eta = tree.Genlep_eta[i]
  types = {
    'pdgID': 'Int_t',
    'pT': 'Float_t',
    'mother': 'Int_t',
    'status': 'Int_t',
    'phi': 'Float_t',
    'eta': 'Float_t',
  }

  @staticmethod
  def make_array(tree):
    return [Genlep(tree, i) for i in range(tree.nGenlep)]

class Genquark:
  def __init__(self, tree, i):
    self.mother = tree.Genquark_mother[i]
    self.pT = tree.Genquark_pT[i]
    self.eta = tree.Genquark_eta[i]
    self.pdgID = tree.Genquark_pdgID[i]
    self.phi = tree.Genquark_phi[i]
  types = {
    'mother': 'Int_t',
    'pT': 'Float_t',
    'eta': 'Float_t',
    'pdgID': 'Int_t',
    'phi': 'Float_t',
  }

  @staticmethod
  def make_array(tree):
    return [Genquark(tree, i) for i in range(tree.nGenquark)]

class Jet:
  def __init__(self, tree, i):
    self.trackSip2dValAboveCharm = tree.TagVarCSV_trackSip2dValAboveCharm[i]
    self.CombMVANEW = tree.Jet_CombMVANEW[i]
    self.ProbaN = tree.Jet_ProbaN[i]
    self.DoubleSV = tree.Jet_DoubleSV[i]
    self.ProbaP = tree.Jet_ProbaP[i]
    self.CombSvx = tree.Jet_CombSvx[i]
    self.tightID = tree.Jet_tightID[i]
    self.CombIVF_P = tree.Jet_CombIVF_P[i]
    self.vertexCategory = tree.TagVarCSV_vertexCategory[i]
    self.flightDistance3dVal = tree.TagVarCSV_flightDistance3dVal[i]
    self.ntracks = tree.Jet_ntracks[i]
    self.CombIVF_N = tree.Jet_CombIVF_N[i]
    self.ncHadrons = tree.Jet_ncHadrons[i]
    self.BprobN = tree.Jet_BprobN[i]
    self.flightDistance2dSig = tree.TagVarCSV_flightDistance2dSig[i]
    self.flightDistance2dVal = tree.TagVarCSV_flightDistance2dVal[i]
    self.BprobP = tree.Jet_BprobP[i]
    self.trackSumJetDeltaR = tree.TagVarCSV_trackSumJetDeltaR[i]
    self.Proba = tree.Jet_Proba[i]
    self.nFirstTrack = tree.Jet_nFirstTrack[i]
    self.pt = tree.Jet_pt[i]
    self.trackSip2dSigAboveCharm = tree.TagVarCSV_trackSip2dSigAboveCharm[i]
    self.nLastTrkInc = tree.Jet_nLastTrkInc[i]
    self.SoftElP = tree.Jet_SoftElP[i]
    self.vertexNTracks = tree.TagVarCSV_vertexNTracks[i]
    self.nseltracks = tree.Jet_nseltracks[i]
    self.nLastTrkTagVarCSV = tree.Jet_nLastTrkTagVarCSV[i]
    self.nSM = tree.Jet_nSM[i]
    self.nSE = tree.Jet_nSE[i]
    self.vertexJetDeltaR = tree.TagVarCSV_vertexJetDeltaR[i]
    self.SoftMuP = tree.Jet_SoftMuP[i]
    self.Svx = tree.Jet_Svx[i]
    self.CombIVF = tree.Jet_CombIVF[i]
    self.nLastTrack = tree.Jet_nLastTrack[i]
    self.CombMVA = tree.Jet_CombMVA[i]
    self.nLastTrkEtaRelTagVarCSV = tree.Jet_nLastTrkEtaRelTagVarCSV[i]
    self.nLastSV = tree.Jet_nLastSV[i]
    self.SvxHP = tree.Jet_SvxHP[i]
    self.nFirstSE = tree.Jet_nFirstSE[i]
    self.nLastSM = tree.Jet_nLastSM[i]
    self.flavour = tree.Jet_flavour[i]
    self.nLastSE = tree.Jet_nLastSE[i]
    self.CombSvxP = tree.Jet_CombSvxP[i]
    self.jetNTracksEtaRel = tree.TagVarCSV_jetNTracksEtaRel[i]
    self.CombSvxN = tree.Jet_CombSvxN[i]
    self.jetNTracks = tree.TagVarCSV_jetNTracks[i]
    self.jetNSecondaryVertices = tree.TagVarCSV_jetNSecondaryVertices[i]
    self.trackSumJetEtRatio = tree.TagVarCSV_trackSumJetEtRatio[i]
    self.trackSip3dValAboveCharm = tree.TagVarCSV_trackSip3dValAboveCharm[i]
    self.mass = tree.Jet_mass[i]
    self.nFirstSV = tree.Jet_nFirstSV[i]
    self.histJet = tree.Jet_histJet[i]
    self.SvxNHP = tree.Jet_SvxNHP[i]
    self.flightDistance3dSig = tree.TagVarCSV_flightDistance3dSig[i]
    self.SoftMuN = tree.Jet_SoftMuN[i]
    self.Bprob = tree.Jet_Bprob[i]
    self.SV_multi = tree.Jet_SV_multi[i]
    self.SoftEl = tree.Jet_SoftEl[i]
    self.phi = tree.Jet_phi[i]
    self.SoftMu = tree.Jet_SoftMu[i]
    self.Ip2N = tree.Jet_Ip2N[i]
    self.Ip2P = tree.Jet_Ip2P[i]
    self.nFirstTrkEtaRelTagVarCSV = tree.Jet_nFirstTrkEtaRelTagVarCSV[i]
    self.looseID = tree.Jet_looseID[i]
    self.trackSip3dSigAboveCharm = tree.TagVarCSV_trackSip3dSigAboveCharm[i]
    self.jes = tree.Jet_jes[i]
    self.eta = tree.Jet_eta[i]
    self.hist2 = tree.Jet_hist2[i]
    self.nFirstSM = tree.Jet_nFirstSM[i]
    self.SoftElN = tree.Jet_SoftElN[i]
    self.vertexMass = tree.TagVarCSV_vertexMass[i]
    self.Ip3N = tree.Jet_Ip3N[i]
    self.vertexEnergyRatio = tree.TagVarCSV_vertexEnergyRatio[i]
    self.nFirstTrkInc = tree.Jet_nFirstTrkInc[i]
    self.nFirstTrkTagVarCSV = tree.Jet_nFirstTrkTagVarCSV[i]
    self.histSvx = tree.Jet_histSvx[i]
    self.genpt = tree.Jet_genpt[i]
    self.hist1 = tree.Jet_hist1[i]
    self.nbHadrons = tree.Jet_nbHadrons[i]
    self.hist3 = tree.Jet_hist3[i]
    self.SvxN = tree.Jet_SvxN[i]
    self.residual = tree.Jet_residual[i]
    self.trackJetPt = tree.TagVarCSV_trackJetPt[i]
    self.Ip3P = tree.Jet_Ip3P[i]
  types = {
    'trackSip2dValAboveCharm': 'Float_t',
    'CombMVANEW': 'Float_t',
    'ProbaN': 'Float_t',
    'DoubleSV': 'Float_t',
    'ProbaP': 'Float_t',
    'CombSvx': 'Float_t',
    'tightID': 'Int_t',
    'CombIVF_P': 'Float_t',
    'vertexCategory': 'Float_t',
    'flightDistance3dVal': 'Float_t',
    'ntracks': 'Int_t',
    'CombIVF_N': 'Float_t',
    'ncHadrons': 'Int_t',
    'BprobN': 'Float_t',
    'flightDistance2dSig': 'Float_t',
    'flightDistance2dVal': 'Float_t',
    'BprobP': 'Float_t',
    'trackSumJetDeltaR': 'Float_t',
    'Proba': 'Float_t',
    'nFirstTrack': 'Int_t',
    'pt': 'Float_t',
    'trackSip2dSigAboveCharm': 'Float_t',
    'nLastTrkInc': 'Int_t',
    'SoftElP': 'Float_t',
    'vertexNTracks': 'Float_t',
    'nseltracks': 'Int_t',
    'nLastTrkTagVarCSV': 'Int_t',
    'nSM': 'Int_t',
    'nSE': 'Int_t',
    'vertexJetDeltaR': 'Float_t',
    'SoftMuP': 'Float_t',
    'Svx': 'Float_t',
    'CombIVF': 'Float_t',
    'nLastTrack': 'Int_t',
    'CombMVA': 'Float_t',
    'nLastTrkEtaRelTagVarCSV': 'Int_t',
    'nLastSV': 'Int_t',
    'SvxHP': 'Float_t',
    'nFirstSE': 'Int_t',
    'nLastSM': 'Int_t',
    'flavour': 'Int_t',
    'nLastSE': 'Int_t',
    'CombSvxP': 'Float_t',
    'jetNTracksEtaRel': 'Float_t',
    'CombSvxN': 'Float_t',
    'jetNTracks': 'Float_t',
    'jetNSecondaryVertices': 'Float_t',
    'trackSumJetEtRatio': 'Float_t',
    'trackSip3dValAboveCharm': 'Float_t',
    'mass': 'Float_t',
    'nFirstSV': 'Int_t',
    'histJet': 'Int_t',
    'SvxNHP': 'Float_t',
    'flightDistance3dSig': 'Float_t',
    'SoftMuN': 'Float_t',
    'Bprob': 'Float_t',
    'SV_multi': 'Int_t',
    'SoftEl': 'Float_t',
    'phi': 'Float_t',
    'SoftMu': 'Float_t',
    'Ip2N': 'Float_t',
    'Ip2P': 'Float_t',
    'nFirstTrkEtaRelTagVarCSV': 'Int_t',
    'looseID': 'Int_t',
    'trackSip3dSigAboveCharm': 'Float_t',
    'jes': 'Float_t',
    'eta': 'Float_t',
    'hist2': 'Int_t',
    'nFirstSM': 'Int_t',
    'SoftElN': 'Float_t',
    'vertexMass': 'Float_t',
    'Ip3N': 'Float_t',
    'vertexEnergyRatio': 'Float_t',
    'nFirstTrkInc': 'Int_t',
    'nFirstTrkTagVarCSV': 'Int_t',
    'histSvx': 'Int_t',
    'genpt': 'Float_t',
    'hist1': 'Int_t',
    'nbHadrons': 'Int_t',
    'hist3': 'Int_t',
    'SvxN': 'Float_t',
    'residual': 'Float_t',
    'trackJetPt': 'Float_t',
    'Ip3P': 'Float_t',
  }

  @staticmethod
  def make_array(tree):
    return [Jet(tree, i) for i in range(tree.nJet)]

class PFElectron:
  def __init__(self, tree, i):
    self.pt = tree.PFElectron_pt[i]
    self.ratio = tree.PFElectron_ratio[i]
    self.ptrel = tree.PFElectron_ptrel[i]
    self.eta = tree.PFElectron_eta[i]
    self.IdxJet = tree.PFElectron_IdxJet[i]
    self.IP = tree.PFElectron_IP[i]
    self.IP2D = tree.PFElectron_IP2D[i]
    self.ratioRel = tree.PFElectron_ratioRel[i]
    self.deltaR = tree.PFElectron_deltaR[i]
    self.phi = tree.PFElectron_phi[i]
  types = {
    'pt': 'Float_t',
    'ratio': 'Float_t',
    'ptrel': 'Float_t',
    'eta': 'Float_t',
    'IdxJet': 'Int_t',
    'IP': 'Float_t',
    'IP2D': 'Float_t',
    'ratioRel': 'Float_t',
    'deltaR': 'Float_t',
    'phi': 'Float_t',
  }

  @staticmethod
  def make_array(tree):
    return [PFElectron(tree, i) for i in range(tree.nPFElectron)]

class PFMuon:
  def __init__(self, tree, i):
    self.GoodQuality = tree.PFMuon_GoodQuality[i]
    self.nTkHit = tree.PFMuon_nTkHit[i]
    self.deltaR = tree.PFMuon_deltaR[i]
    self.nMuHit = tree.PFMuon_nMuHit[i]
    self.chi2Tk = tree.PFMuon_chi2Tk[i]
    self.nTkLwM = tree.PFMuon_nTkLwM[i]
    self.IdxJet = tree.PFMuon_IdxJet[i]
    self.ratioRel = tree.PFMuon_ratioRel[i]
    self.IP = tree.PFMuon_IP[i]
    self.nMatched = tree.PFMuon_nMatched[i]
    self.ratio = tree.PFMuon_ratio[i]
    self.IP2D = tree.PFMuon_IP2D[i]
    self.phi = tree.PFMuon_phi[i]
    self.pt = tree.PFMuon_pt[i]
    self.nOutHit = tree.PFMuon_nOutHit[i]
    self.isGlobal = tree.PFMuon_isGlobal[i]
    self.nPixLwM = tree.PFMuon_nPixLwM[i]
    self.hist = tree.PFMuon_hist[i]
    self.dz = tree.PFMuon_dz[i]
    self.eta = tree.PFMuon_eta[i]
    self.nPixHit = tree.PFMuon_nPixHit[i]
    self.ptrel = tree.PFMuon_ptrel[i]
    self.chi2 = tree.PFMuon_chi2[i]
  types = {
    'GoodQuality': 'Int_t',
    'nTkHit': 'Int_t',
    'deltaR': 'Float_t',
    'nMuHit': 'Int_t',
    'chi2Tk': 'Float_t',
    'nTkLwM': 'Int_t',
    'IdxJet': 'Int_t',
    'ratioRel': 'Float_t',
    'IP': 'Float_t',
    'nMatched': 'Int_t',
    'ratio': 'Float_t',
    'IP2D': 'Float_t',
    'phi': 'Float_t',
    'pt': 'Float_t',
    'nOutHit': 'Int_t',
    'isGlobal': 'Int_t',
    'nPixLwM': 'Int_t',
    'hist': 'Int_t',
    'dz': 'Float_t',
    'eta': 'Float_t',
    'nPixHit': 'Int_t',
    'ptrel': 'Float_t',
    'chi2': 'Float_t',
  }

  @staticmethod
  def make_array(tree):
    return [PFMuon(tree, i) for i in range(tree.nPFMuon)]

class PU:
  def __init__(self, tree, i):
    self.z = tree.PU_z[i]
    self.sumpT_low = tree.PU_sumpT_low[i]
    self.sumpT_high = tree.PU_sumpT_high[i]
    self.bunch = tree.PU_bunch[i]
    self.ntrks_low = tree.PU_ntrks_low[i]
    self.ntrks_high = tree.PU_ntrks_high[i]
  types = {
    'z': 'Float_t',
    'sumpT_low': 'Float_t',
    'sumpT_high': 'Float_t',
    'bunch': 'Int_t',
    'ntrks_low': 'Int_t',
    'ntrks_high': 'Int_t',
  }

  @staticmethod
  def make_array(tree):
    return [PU(tree, i) for i in range(tree.nPU)]

class SV:
  def __init__(self, tree, i):
    self.z = tree.SV_z[i]
    self.flightErr = tree.SV_flightErr[i]
    self.EnergyRatio = tree.SV_EnergyRatio[i]
    self.totCharge = tree.SV_totCharge[i]
    self.x = tree.SV_x[i]
    self.y = tree.SV_y[i]
    self.vtx_phi = tree.SV_vtx_phi[i]
    self.vtxDistJetAxis = tree.SV_vtxDistJetAxis[i]
    self.mass = tree.SV_mass[i]
    self.flight2DErr = tree.SV_flight2DErr[i]
    self.chi2 = tree.SV_chi2[i]
    self.vtx_pt = tree.SV_vtx_pt[i]
    self.dir_y = tree.SV_dir_y[i]
    self.ndf = tree.SV_ndf[i]
    self.vtx_eta = tree.SV_vtx_eta[i]
    self.flight = tree.SV_flight[i]
    self.flight2D = tree.SV_flight2D[i]
    self.ex = tree.SV_ex[i]
    self.ey = tree.SV_ey[i]
    self.ez = tree.SV_ez[i]
    self.nTrk = tree.SV_nTrk[i]
    self.deltaR_jet = tree.SV_deltaR_jet[i]
    self.dir_z = tree.SV_dir_z[i]
    self.dir_x = tree.SV_dir_x[i]
    self.deltaR_sum_dir = tree.SV_deltaR_sum_dir[i]
    self.deltaR_sum_jet = tree.SV_deltaR_sum_jet[i]
  types = {
    'z': 'Float_t',
    'flightErr': 'Float_t',
    'EnergyRatio': 'Float_t',
    'totCharge': 'Float_t',
    'x': 'Float_t',
    'y': 'Float_t',
    'vtx_phi': 'Float_t',
    'vtxDistJetAxis': 'Float_t',
    'mass': 'Float_t',
    'flight2DErr': 'Float_t',
    'chi2': 'Float_t',
    'vtx_pt': 'Float_t',
    'dir_y': 'Float_t',
    'ndf': 'Float_t',
    'vtx_eta': 'Float_t',
    'flight': 'Float_t',
    'flight2D': 'Float_t',
    'ex': 'Float_t',
    'ey': 'Float_t',
    'ez': 'Float_t',
    'nTrk': 'Int_t',
    'deltaR_jet': 'Float_t',
    'dir_z': 'Float_t',
    'dir_x': 'Float_t',
    'deltaR_sum_dir': 'Float_t',
    'deltaR_sum_jet': 'Float_t',
  }

  @staticmethod
  def make_array(tree):
    return [SV(tree, i) for i in range(tree.nSV)]

class TrkEtaRelTagVarCSV:
  def __init__(self, tree, i):
    self.trackEtaRel = tree.TagVarCSV_trackEtaRel[i]
  types = {
    'trackEtaRel': 'Float_t',
  }

  @staticmethod
  def make_array(tree):
    return [TrkEtaRelTagVarCSV(tree, i) for i in range(tree.nTrkEtaRelTagVarCSV)]

class TrkInc:
  def __init__(self, tree, i):
    self.IPsig = tree.TrkInc_IPsig[i]
    self.eta = tree.TrkInc_eta[i]
    self.IP = tree.TrkInc_IP[i]
    self.pt = tree.TrkInc_pt[i]
    self.phi = tree.TrkInc_phi[i]
    self.ptrel = tree.TrkInc_ptrel[i]
  types = {
    'IPsig': 'Float_t',
    'eta': 'Float_t',
    'IP': 'Float_t',
    'pt': 'Float_t',
    'phi': 'Float_t',
    'ptrel': 'Float_t',
  }

  @staticmethod
  def make_array(tree):
    return [TrkInc(tree, i) for i in range(tree.nTrkInc)]

class TrkTagVarCSV:
  def __init__(self, tree, i):
    self.trackEta = tree.TagVarCSV_trackEta[i]
    self.trackDeltaR = tree.TagVarCSV_trackDeltaR[i]
    self.trackPParRatio = tree.TagVarCSV_trackPParRatio[i]
    self.trackMomentum = tree.TagVarCSV_trackMomentum[i]
    self.trackJetDistSig = tree.TagVarCSV_trackJetDistSig[i]
    self.trackPhi = tree.TagVarCSV_trackPhi[i]
    self.trackDecayLenVal = tree.TagVarCSV_trackDecayLenVal[i]
    self.trackDecayLenSig = tree.TagVarCSV_trackDecayLenSig[i]
    self.trackPtRel = tree.TagVarCSV_trackPtRel[i]
    self.trackSip3dSig = tree.TagVarCSV_trackSip3dSig[i]
    self.trackPtRatio = tree.TagVarCSV_trackPtRatio[i]
    self.trackSip2dVal = tree.TagVarCSV_trackSip2dVal[i]
    self.trackPPar = tree.TagVarCSV_trackPPar[i]
    self.trackJetDistVal = tree.TagVarCSV_trackJetDistVal[i]
    self.trackSip3dVal = tree.TagVarCSV_trackSip3dVal[i]
    self.trackSip2dSig = tree.TagVarCSV_trackSip2dSig[i]
  types = {
    'trackEta': 'Float_t',
    'trackDeltaR': 'Float_t',
    'trackPParRatio': 'Float_t',
    'trackMomentum': 'Float_t',
    'trackJetDistSig': 'Float_t',
    'trackPhi': 'Float_t',
    'trackDecayLenVal': 'Float_t',
    'trackDecayLenSig': 'Float_t',
    'trackPtRel': 'Float_t',
    'trackSip3dSig': 'Float_t',
    'trackPtRatio': 'Float_t',
    'trackSip2dVal': 'Float_t',
    'trackPPar': 'Float_t',
    'trackJetDistVal': 'Float_t',
    'trackSip3dVal': 'Float_t',
    'trackSip2dSig': 'Float_t',
  }

  @staticmethod
  def make_array(tree):
    return [TrkTagVarCSV(tree, i) for i in range(tree.nTrkTagVarCSV)]

class bQuarks:
  def __init__(self, tree, i):
    self.pT = tree.bQuark_pT[i]
    self.fromGSP = tree.bQuark_fromGSP[i]
    self.phi = tree.bQuark_phi[i]
    self.status = tree.bQuark_status[i]
    self.pdgID = tree.bQuark_pdgID[i]
    self.eta = tree.bQuark_eta[i]
  types = {
    'pT': 'Float_t',
    'fromGSP': 'Int_t',
    'phi': 'Float_t',
    'status': 'Int_t',
    'pdgID': 'Int_t',
    'eta': 'Float_t',
  }

  @staticmethod
  def make_array(tree):
    return [bQuarks(tree, i) for i in range(tree.nbQuarks)]

class cQuarks:
  def __init__(self, tree, i):
    self.eta = tree.cQuark_eta[i]
    self.phi = tree.cQuark_phi[i]
    self.pdgID = tree.cQuark_pdgID[i]
    self.status = tree.cQuark_status[i]
    self.fromGSP = tree.cQuark_fromGSP[i]
    self.pT = tree.cQuark_pT[i]
  types = {
    'eta': 'Float_t',
    'phi': 'Float_t',
    'pdgID': 'Int_t',
    'status': 'Int_t',
    'fromGSP': 'Int_t',
    'pT': 'Float_t',
  }

  @staticmethod
  def make_array(tree):
    return [cQuarks(tree, i) for i in range(tree.ncQuarks)]


class Event:
  def __init__(self, tree):
    #self.BHadrons = BHadrons.make_array(tree)
    #self.BitTrigger = BitTrigger.make_array(tree)
    #self.DHadrons = DHadrons.make_array(tree)
    #self.Daughters = Daughters.make_array(tree)
    #self.GenPruned = GenPruned.make_array(tree)
    #self.GenV0 = GenV0.make_array(tree)
    #self.Genlep = Genlep.make_array(tree)
    #self.Genquark = Genquark.make_array(tree)
    self.Jet = Jet.make_array(tree)
    #self.PFElectron = PFElectron.make_array(tree)
    #self.PFMuon = PFMuon.make_array(tree)
    #self.PU = PU.make_array(tree)
    self.SV = SV.make_array(tree)
    #self.TrkEtaRelTagVarCSV = TrkEtaRelTagVarCSV.make_array(tree)
    #self.TrkInc = TrkInc.make_array(tree)
    #self.TrkTagVarCSV = TrkTagVarCSV.make_array(tree)
    #self.bQuarks = bQuarks.make_array(tree)
    #self.cQuarks = cQuarks.make_array(tree)
    #self.nGenPruned = tree.nGenPruned
    #self.nPFElectron = tree.nPFElectron
    #self.ncQuarks = tree.ncQuarks
    #self.nPUtrue = tree.nPUtrue
    #self.nGenlep = tree.nGenlep
    #self.nTrkTagVarCSV = tree.nTrkTagVarCSV
    #self.nBHadrons = tree.nBHadrons
    #self.nTrkInc = tree.nTrkInc
    #self.Run = tree.Run
    #self.nPFMuon = tree.nPFMuon
    #self.GenPVz = tree.GenPVz
    #self.nbQuarks = tree.nbQuarks
    #self.mcweight = tree.mcweight
    #self.PVz = tree.PVz
    self.nJet = tree.nJet
    #self.nPU = tree.nPU
    #self.PVez = tree.PVez
    #self.nTrkEtaRelTagVarCSV = tree.nTrkEtaRelTagVarCSV
    #self.nBitTrigger = tree.nBitTrigger
    #self.Evt = tree.Evt
    self.nSV = tree.nSV
    #self.pthat = tree.pthat
    #self.nDaughters = tree.nDaughters
    #self.LumiBlock = tree.LumiBlock
    self.nPV = tree.nPV
    #self.nGenquark = tree.nGenquark
    #self.nDHadrons = tree.nDHadrons
    #self.nGenV0 = tree.nGenV0

