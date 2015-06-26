import FWCore.ParameterSet.Config as cms

combinedMVAComputerETH = cms.ESProducer("CombinedMVAJetTagESProducerETH",
	useCategories = cms.bool(False),
	calibrationRecord = cms.string('CombinedMVA'),
	jetTagComputers = cms.vstring(
		'jetProbabilityComputer',
		'combinedSecondaryVertexComputer',
		'softPFMuonComputer',
		'softPFElectronComputer'
    )
)

