import FWCore.ParameterSet.Config as cms

pfCombinedMVABJetTagsETH = cms.EDProducer("JetTagProducer",
	jetTagComputer = cms.string('candidateCombinedMVAComputerETH'),
	tagInfos = cms.VInputTag(
		cms.InputTag("pfImpactParameterTagInfos"),
		cms.InputTag("pfInclusiveSecondaryVertexFinderTagInfos"),
		cms.InputTag("softPFMuonsTagInfos"),
		cms.InputTag("softPFElectronsTagInfos")
	)
)
