import FWCore.ParameterSet.Config as cms

combinedMVAComputerETH = cms.ESProducer("CombinedMVAJetTagESProducerETH",
	useCategories = cms.bool(False),
	calibrationRecord = cms.string('CombinedMVA'),
	jetTagComputers = cms.vstring(
		'jetProbabilityComputer',
		'jetBProbabilityComputer',
		'combinedSecondaryVertexComputer',
		'combinedSecondaryVertexComputer',
		'softPFMuonComputer',
		'softPFElectronComputer'
    ),
    isCandidateBased = cms.bool(False)
)

