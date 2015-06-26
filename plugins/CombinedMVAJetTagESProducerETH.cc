#include "FWCore/Framework/interface/ModuleFactory.h"

#include "RecoBTau/JetTagComputer/interface/JetTagComputerESProducer.h"
#include "RecoBTag/CombinedMVA/interface/CombinedMVAJetTagComputerETH.h"

typedef JetTagComputerESProducer<CombinedMVAJetTagComputerETH> CombinedMVAJetTagESProducerETH;
DEFINE_FWK_EVENTSETUP_MODULE(CombinedMVAJetTagESProducerETH);
