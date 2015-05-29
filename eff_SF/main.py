from efficiency2 import efficiency2
from samples import *
from config import *

#	---- MAIN ----

process_GGH = efficiency2(GGH)
#process_GGH.plotting (GGH, 'pt')
#process_GGH.plotting (GGH, 'eta')
process_GGH.lookup_table(GGH)
process_GGH.full_mc_sf('loose')		# <--- full_mc_sf only called once (for GGH), as it uses all the mc samples available,
process_GGH.full_mc_sf('medium')	# so there is no reason to call it for the other processes (VBF, TTH) as well
process_GGH.full_mc_sf('tight')

process_VBF = efficiency2(VBF)
#process_VBF.plotting (VBF, 'pt')
#process_VBF.plotting (VBF, 'eta')
process_VBF.lookup_table(VBF)

process_TTH = efficiency2(TTH)
#process_TTH.plotting (TTH, 'pt')
#process_TTH.plotting (TTH, 'eta')
process_TTH.lookup_table(TTH)

#process_DATA = efficiency2(DATA)
#process_DATA.plotting (DATA, 'pt')
#process_DATA.plotting (DATA, 'eta')
