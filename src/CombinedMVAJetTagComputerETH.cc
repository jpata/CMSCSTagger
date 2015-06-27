#include <algorithm>
#include <iostream>
#include <sstream>
#include <string>
#include <memory>
#include <vector>
#include <map>

#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CondFormats/PhysicsToolsObjects/interface/MVAComputer.h"
#include "DataFormats/Common/interface/RefToBase.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/BTauReco/interface/TaggingVariable.h"
#include "RecoBTau/JetTagComputer/interface/JetTagComputer.h"
#include "RecoBTau/JetTagComputer/interface/JetTagComputerRecord.h"
#include "RecoBTau/JetTagComputer/interface/GenericMVAJetTagComputer.h"
#include "RecoBTag/SecondaryVertex/interface/CombinedSVComputer.h"
#include "RecoBTag/CombinedMVA/interface/CombinedMVAJetTagComputerETH.h"

#include "DataFormats/BTauReco/interface/CandIPTagInfo.h" 
#include "DataFormats/BTauReco/interface/CandSoftLeptonTagInfo.h" 
#include "DataFormats/BTauReco/interface/CandSecondaryVertexTagInfo.h"
#include "DataFormats/BTauReco/interface/CandIPTagInfo.h"

#include "DataFormats/BTauReco/interface/IPTagInfo.h" 
#include "DataFormats/BTauReco/interface/SoftLeptonTagInfo.h" 
#include "DataFormats/BTauReco/interface/SecondaryVertexTagInfo.h"
#include "DataFormats/BTauReco/interface/IPTagInfo.h"

using namespace reco;
using namespace PhysicsTools;

CombinedMVAJetTagComputerETH::CombinedMVAJetTagComputerETH(
					const edm::ParameterSet &params) :
	GenericMVAJetTagComputer(params)
{
	std::cout << "CombinedMVAJetTagComputerETH::constructor" << std::endl;

	inputComputerNames = params.getParameter< std::vector<std::string>>(
		"jetTagComputers"
	);
	isCandidateBased = params.getParameter<bool>(
		"isCandidateBased"
	);

	uses(0, "ipTagInfos");
  	uses(1, "svTagInfos");
  	uses(2, "svTagInfos");
  	uses(3, "smTagInfos");
  	uses(4, "seTagInfos");
}

CombinedMVAJetTagComputerETH::~CombinedMVAJetTagComputerETH()
{
}

void CombinedMVAJetTagComputerETH::initialize(const JetTagComputerRecord & record) {
	std::cout << "CombinedMVAJetTagComputerETH::initialize" << std::endl;

	for (auto & name : inputComputerNames) {
		edm::ESHandle<JetTagComputer> computerHandle;
		record.get(name, computerHandle);
		const JetTagComputer* comp = computerHandle.product();
		computers.push_back(comp);
		std::vector<std::string> inputLabels(comp->getInputLabels());
		
		for (auto lab : inputLabels) {
			std::cout << name << " " << lab << std::endl;
		}
		
	}
  GenericMVAJetTagComputer::initialize(record);
}

float CombinedMVAJetTagComputerETH::discriminator(const JetTagComputer::TagInfoHelper &info) const
{
   

    if (isCandidateBased) {
        float a1, a2, a3, a4, a5, a6;
        const JetTagComputer::TagInfoHelper tv1({(const reco::BaseTagInfo*)&info.get<const reco::CandIPTagInfo>(0)}); 
        const JetTagComputer::TagInfoHelper tv2({(const reco::BaseTagInfo*)&info.get<const reco::CandIPTagInfo>(0)}); 
        const JetTagComputer::TagInfoHelper tv_csv1({(const reco::BaseTagInfo*)&info.get<const reco::CandIPTagInfo>(0), (const reco::BaseTagInfo*)&info.get<const reco::CandSecondaryVertexTagInfo>(1)}); 
        const JetTagComputer::TagInfoHelper tv_csv2({(const reco::BaseTagInfo*)&info.get<const reco::CandIPTagInfo>(0), (const reco::BaseTagInfo*)&info.get<const reco::CandSecondaryVertexTagInfo>(2)}); 
        const JetTagComputer::TagInfoHelper tv3({(const reco::BaseTagInfo*)&info.get<const reco::CandSoftLeptonTagInfo>(3)});
        const JetTagComputer::TagInfoHelper tv4({(const reco::BaseTagInfo*)&info.get<const reco::CandSoftLeptonTagInfo>(4)});
        std::cout << "got taginfos" << std::endl;	
        //jetProbabilityComputer
        a1 = (*computers[0])(tv1);
        std::cout << "a1 " << a1 << std::endl;
        a2 = (*computers[1])(tv2);
        a3 = (*computers[2])(tv_csv1);
        a4 = (*computers[3])(tv_csv2);
        a5 = (*computers[4])(tv3);
        a6 = (*computers[5])(tv4);
        std::cout << "computer " << a1 << " " << a2 << " " << a3 << " " << a4 << " " << a5 << " " << a6 << std::endl;
    }
	return 0.0;
}
