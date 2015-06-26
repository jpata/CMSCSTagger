#include "FWCore/Framework/interface/ModuleFactory.h"

#include "RecoBTau/JetTagComputer/interface/JetTagComputerESProducer.h"
#include "RecoBTag/CombinedMVA/interface/CombinedMVAJetTagComputerETH.h"

typedef JetTagComputerESProducer<CombinedMVAJetTagComputerETH> CombinedMVAETHJetTagESProducer;
DEFINE_FWK_EVENTSETUP_MODULE(CombinedMVAETHJetTagESProducer);
