import ROOT
from array import array
import copy
import os.path
from config import *
from samples import *

# Opzioni ROOT
ROOT.gStyle.SetOptStat(0)

class efficiency2 (object) :

# ---------------------------------------------------- __init__ -------------------------------------------------------------------------------

	# __init__(samples) --> creates a TChain that contains the RootFiles/Trees
	def __init__ (self, sample) :
		self.ch = ROOT.TChain('tree')
		self.ch.Add(sample['FilePath'])

		self.ch_data = ROOT.TChain('tree')
		self.ch_data.Add(DATA['FilePath'])

# ---------------------------------------------------- __EFF 1D__ -------------------------------------------------------------------------------
	def efficiency1D (self, sample, variable, wp):	

		if variable is 'pt' :
			h_den = ROOT.TH1F('h_den', 'h_den', num_pt_bins, array('d',pt_bins))
			h_num = ROOT.TH1F('h_num', 'h_num', num_pt_bins, array('d',pt_bins))
			for evt in self.ch :
				if evt.l2_reliso05<0.1 and evt.l2_muonid_tight and evt.mvis>60 and evt.mvis<100 :
					h_den.Fill(evt.l1_pt)
					if wp is 'loose':
						if evt.l1_byCombinedIsolationDeltaBetaCorr3Hits>0.5 :
							h_num.Fill(evt.l1_pt)
					elif wp is 'medium' :
						if evt.l1_byCombinedIsolationDeltaBetaCorr3Hits>1.5 :
							h_num.Fill(evt.l1_pt)
					elif wp is 'tight' :
						if evt.l1_byCombinedIsolationDeltaBetaCorr3Hits>2.5 :
							h_num.Fill(evt.l1_pt)

		if variable is 'eta' :
			h_den = ROOT.TH1F('h_den', 'h_den', 10, -3, 3)
			h_num = ROOT.TH1F('h_num', 'h_num', 10, -3, 3)
			for evt in self.ch :
				if evt.l2_reliso05<0.1 and evt.l2_muonid_tight and evt.mvis>60 and evt.mvis<100 :
					h_den.Fill(evt.l1_eta)
					if wp is 'loose':
						if evt.l1_byCombinedIsolationDeltaBetaCorr3Hits>0.5 :
							h_num.Fill(evt.l1_eta)
					elif wp is 'medium' :
						if evt.l1_byCombinedIsolationDeltaBetaCorr3Hits>1.5 :
							h_num.Fill(evt.l1_eta)
					elif wp is 'tight' :
						if evt.l1_byCombinedIsolationDeltaBetaCorr3Hits>2.5 :
							h_num.Fill(evt.l1_eta)

		return ROOT.TGraphAsymmErrors(h_num, h_den)

# ---------------------------------------------------- __EFF 2D__ -------------------------------------------------------------------------------
	def efficiency2D (self,sample, wp) :

		h_den = ROOT.TH2F('h_den', 'h_den', num_pt_bins, array('d',pt_bins), num_eta_bins, array('d',eta_bins))
		h_num = ROOT.TH2F('h_num', 'h_num', num_pt_bins, array('d',pt_bins), num_eta_bins, array('d',eta_bins))

		if sample['Sample'] is 'DATA' :
			for evt in self.ch_data :
				if evt.l2_reliso05<0.1 and evt.l2_muonid_tight and evt.mvis>60 and evt.mvis<100 :
					h_den.Fill(evt.l1_pt, evt.l1_eta)
					if wp is 'loose':
						if evt.l1_byCombinedIsolationDeltaBetaCorr3Hits>0.5 :
							h_num.Fill(evt.l1_pt, evt.l1_eta)
					elif wp is 'medium' :
						if evt.l1_byCombinedIsolationDeltaBetaCorr3Hits>1.5 :
							h_num.Fill(evt.l1_pt, evt.l1_eta)
					elif wp is 'tight' :
						if evt.l1_byCombinedIsolationDeltaBetaCorr3Hits>2.5 :
							h_num.Fill(evt.l1_pt, evt.l1_eta)
		else :
			for evt in self.ch :
				if evt.l2_reliso05<0.1 and evt.l2_muonid_tight and evt.mvis>60 and evt.mvis<100 :
					h_den.Fill(evt.l1_pt, evt.l1_eta)
					if wp is 'loose':
						if evt.l1_byCombinedIsolationDeltaBetaCorr3Hits>0.5 :
							h_num.Fill(evt.l1_pt, evt.l1_eta)
					elif wp is 'medium' :
						if evt.l1_byCombinedIsolationDeltaBetaCorr3Hits>1.5 :
							h_num.Fill(evt.l1_pt, evt.l1_eta)
					elif wp is 'tight' :
						if evt.l1_byCombinedIsolationDeltaBetaCorr3Hits>2.5 :
							h_num.Fill(evt.l1_pt, evt.l1_eta)

		h_num.GetXaxis().SetTitle('p_{T}(#tau) [GeV]')
		h_num.GetYaxis().SetTitle('#eta')
		h_num.Divide(h_den)
		h_num.SetName(wp+'_eff_'+sample['Sample'])
		h_num.SetTitle(wp+'_eff_'+sample['Sample'])
		return h_num

# ---------------------------------------------------- __SCALE FACTOR__ -------------------------------------------------------------------------------
	def scale_factor (self,sample_MC, wp) :

		MC = self.efficiency2D(sample_MC, wp)
		data = self.efficiency2D(DATA, wp)

		data.SetName(wp+'_sf_'+sample_MC['Sample'])
		data.SetTitle(wp+'_sf_'+sample_MC['Sample'])
		data.Divide(MC)
		return data

# ---------------------------------------------------- __FULL MC EFFICIENCY__ -------------------------------------------------------------------------------
	def full_mc_sf (self, wp) :
		
		ch_full_mc = ROOT.TChain('tree')
		for mc_sample in mc_samples:
			ch_full_mc.Add(mc_sample['FilePath'])

		full_den = ROOT.TH2F('full_den', 'full_den', num_pt_bins, array('d',pt_bins), num_eta_bins, array('d',eta_bins))
		full_num = ROOT.TH2F('full_num', 'full_num', num_pt_bins, array('d',pt_bins), num_eta_bins, array('d',eta_bins))

		for evt in ch_full_mc :
			if evt.l2_reliso05<0.1 and evt.l2_muonid_tight and evt.mvis>60 and evt.mvis<100 :
				full_den.Fill(evt.l1_pt, evt.l1_eta)
				if wp is 'loose':
					if evt.l1_byCombinedIsolationDeltaBetaCorr3Hits>0.5 :
						full_num.Fill(evt.l1_pt, evt.l1_eta)
				elif wp is 'medium' :
					if evt.l1_byCombinedIsolationDeltaBetaCorr3Hits>1.5 :
						full_num.Fill(evt.l1_pt, evt.l1_eta)
				elif wp is 'tight' :
					if evt.l1_byCombinedIsolationDeltaBetaCorr3Hits>2.5 :
						full_num.Fill(evt.l1_pt, evt.l1_eta)
		
		full_num.GetXaxis().SetTitle('p_{T}(#tau) [GeV]')
		full_num.GetYaxis().SetTitle('#eta')
		full_num.Divide(full_den)		# Efficiency for all the mc samples together

		data = self.efficiency2D(DATA, wp)
		data.SetName(wp+'_sf_full_mc')
		data.SetTitle(wp+'_sf_full_mc')
		data.Divide(full_num)			# SF for all the mc samples together

		# Saving the full_mc_scale_factor on the Root File
		lookup_table = ROOT.TFile.Open('new_mt_lookup_table.root','update')
		lookup_table.cd()
		if wp is 'loose' :
			lookup_table.mkdir('tau_loose_iso')
			lookup_table.cd('tau_loose_iso')
			data.Write()
			print 'full_mc_sf LOOSE'
		elif wp is 'medium' :
			lookup_table.mkdir('tau_medium_iso')
			lookup_table.cd('tau_medium_iso')
			data.Write()
			print 'full_mc_sf MEDIUM'
		elif wp is 'tight' :
			lookup_table.mkdir('tau_tight_iso')
			lookup_table.cd('tau_tight_iso')
			data.Write()
			print 'full_mc_sf TIGHT'
		lookup_table.cd()
		lookup_table.Close()

# ---------------------------------------------------- __PLOTTING__ -------------------------------------------------------------------------------
	def plotting (self,sample,variable) :

		# Calculation of the efficiencies
		eff_loose = self.efficiency1D(sample, variable, 'loose')
		eff_medium = self.efficiency1D(sample, variable, 'medium')
		eff_tight = self.efficiency1D(sample, variable, 'tight')

		# Definition of the TLegend
		legend = ROOT.TLegend(0.1,0.75,0.35,0.9)
		legend.AddEntry(eff_loose ,'#tau_loose_iso' ,'LPFE')
		legend.AddEntry(eff_medium,'#tau_medium_iso','LPFE')
		legend.AddEntry(eff_tight ,'#tau_tight_iso' ,'LPFE')
		legend.SetFillColor(0)

		# Creation of TCanvas and plotting the results
		c1 = ROOT.TCanvas('c1','c1',700,700)
		ROOT.gPad.SetFrameLineWidth(2)
		eff_loose.Draw('AP')
		eff_loose.GetYaxis().SetRangeUser(0.4,1)
		eff_medium.Draw('sameP')
		eff_tight.Draw('sameP')
		eff_loose.SetTitle('Efficiency vs '+variable+' ('+sample['Sample']+') ')
		if variable is 'pt' : 
			eff_loose.GetXaxis().SetTitle('p_{T}(#tau) [GeV]')
		elif variable is 'eta' :
			eff_loose.GetXaxis().SetTitle('#eta')
		eff_loose.GetYaxis().SetTitle('#epsilon')
		eff_loose.GetYaxis().SetTitleOffset(1.3)
		eff_loose.SetLineColor(1)
		eff_loose.SetMarkerColor(1)
		eff_loose.SetMarkerStyle(21)
		eff_medium.SetLineColor(2)
		eff_medium.SetMarkerColor(2)
		eff_medium.SetMarkerStyle(21)
		eff_tight.SetLineColor(4)
		eff_tight.SetMarkerColor(4)
		eff_tight.SetMarkerStyle(21)
		legend.Draw('sameAPEZ')
		c1.SaveAs('eff_'+sample['Sample']+'_'+variable+'_1D.png')
		

# ---------------------------------------------------- __LOOKUP TABLE__ -------------------------------------------------------------------------------
			# !!!!!!!!!!!!!!!!! metti a posto che stampa il sf_full_mc tre volte per ogni wp!
	def lookup_table (self,sample) :
		
		print 'Processing sample '+sample['Sample']
		# Creation of Root File
		lookup_table = ROOT.TFile.Open('mt_lookup_table.root','update')
		
		# Creation of LOOSE directory
		lookup_table.cd()
		lookup_table.mkdir('tau_loose_iso')
		lookup_table.cd('tau_loose_iso')
		self.efficiency2D(sample, 'loose').Write()
		self.scale_factor(sample, 'loose').Write()
		
		# Creation of MEDIUM directory
		lookup_table.cd()
		lookup_table.mkdir('tau_medium_iso')
		lookup_table.cd('tau_medium_iso')
		self.efficiency2D(sample, 'medium').Write()
		self.scale_factor(sample, 'medium').Write()

		# Creation of TIGHT directory
		lookup_table.cd()
		lookup_table.mkdir('tau_tight_iso')
		lookup_table.cd('tau_tight_iso')
		self.efficiency2D(sample, 'tight').Write()
		self.scale_factor(sample, 'tight').Write()

		# Closing .root file
		lookup_table.cd()
		lookup_table.Close()
