#ifndef RecoBTau_JetTagComputer_CombinedMVAJetTagComputerETH_h
#define RecoBTau_JetTagComputer_CombinedMVAJetTagComputerETH_h

#include <string>
#include <memory>
#include <vector>
#include <map>

#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/BTauReco/interface/TaggingVariable.h"
#include "RecoBTau/JetTagComputer/interface/JetTagComputer.h"
#include "RecoBTau/JetTagComputer/interface/GenericMVAJetTagComputer.h"

class CombinedMVAJetTagComputerETH : public GenericMVAJetTagComputer {
    public:
    CombinedMVAJetTagComputerETH(const edm::ParameterSet &parameters);
    virtual ~CombinedMVAJetTagComputerETH();

    virtual void initialize(const JetTagComputerRecord & record);

    float discriminator(const TagInfoHelper &info) const override;

    std::vector<const JetTagComputer*> computers;

    std::vector<std::string> inputComputerNames;
    bool isCandidateBased;
};

#endif // RecoBTau_JetTagComputer_CombinedMVAJetTagComputerETH_h
