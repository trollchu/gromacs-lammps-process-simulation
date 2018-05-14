# _*_ coding: utf-8 _*_

'''
@author: Ruan Yang
Created on 2018.5.7
Simulation process
  EM---NVTEquilibrium---NPTEquilibrium---NVT(NPT) Production run---Standmdp
'''

import numpy as np

def Emmdp(method='steep',emtol=1000,nsteps=50000,rcoulomb=1.0,rvdw=1.0):
	'''
	method: steep or cg
	emtol: default=1000, If the system doesn't converge, increase this variabel
	nstpes: run steps, default=50000
	rcoulomb: cut-off distances of electrostatic interaction,default=1.0
	rvdw: cut-off distances of vdw interaction,default=1.0
	'''
	with open('emequilibrium.mdp','w') as f:
		f.write('; This mdp file generated by Gmxmdp.py. \n')
		f.write('; Author: Ruan Yang\n')
		f.write('; https://github.com/ruanyangry \n')
		f.write('; em.mdp - used as input into grompp to generate em.tpr\n')
		f.write(' \n')
		f.write('integrator	= %s\n'%(method))
		f.write('emtol		= %.2f\n'%(emtol))
		f.write('emstep     = 0.01\n')
		f.write('nsteps		= %d\n'%(nsteps))
		f.write(' \n')
		f.write('; Parameters describing how to find the neighbors of each \
		atom and how to calculate the interactions\n')
		f.write('nstlist		 = 1\n')
		f.write('cutoff-scheme   = Verlet\n')
		f.write('ns_type		 = grid\n')
		f.write('coulombtype	 = PME\n')
		f.write('rcoulomb	     = %.2f\n'%(rcoulomb))
		f.write('rvdw		     = %.2f\n'%(rvdw))
		f.write('pbc		     = xyz\n')
		
def Equilibrium(ensemble='nvt',integrator='md',nsteps=1000000,dt=0.002,outfrequency=500,\
constraints='all-bonds',rcoulomb=1.0,rvdw=1.0,tcoupl='V-rescale',ref_t=300.0,pcoupl='no',\
pcoupltype='isotropic',ref_p=1.0):
	'''
	ensemble : nvt or npt
	integrator : md, md-vv, md-vv-avek, default=md
	nsteps : run steps, default=1000000
	dt : timesteps, default= 0.002
	outfrequency : outfrequency*dt=1 ps, default=500
	constraints : constraints bond vibration h-bonds,all-bonds,h-angles,all-angles,none,\
	for organic default=all-bonds
	rcoulomb : cut-off distances of electrostatic interaction,default=1.0
	rvdw: cut-off distances of vdw interaction,default=1.0
	tcoupl : temperature coupling method, berendsen,nose-hoover,andersen,andersen-massive,\
	v-rescale, default=v-rescale
	ref_t : reference temperature for coupling (one for each group in tc-grps), default=300.0K
	pcoupl : if ensemble ='npt',pressure coupling on,berendsen,Parrinello-Rahman, default= Parrinello-Rahman,\
	         default=Parrinello-Rahman
	pcoupltype : isotropic,semiisotropic,anisotropic,surface-tension, default=isotropic
	ref_p : reference pressure for coupling, default= 1.0
	'''
	with open('%sequilibrium.mdp'%(ensemble),'w') as f:
		f.write('; This mdp file generated by Gmxmdp.py. \n')
		f.write('; Author: Ruan Yang\n')
		f.write('; https://github.com/ruanyangry \n')
		f.write('; NVT ensemble equilibrium\n')
		f.write(' \n')
		f.write('; Run parameters\n')
		f.write('integrator	= %s\n'%(integrator))
		f.write('nsteps		= %d\n'%(nsteps))
		f.write('dt		    = %.5f\n'%(dt))
		f.write(' \n')
		f.write('; Output control\n')
		f.write('nstxout		= %d\n'%(outfrequency))
		f.write('nstvout		= %d\n'%(outfrequency))
		f.write('nstenergy	    = %d\n'%(outfrequency))
		f.write('nstlog		    = %d\n'%(outfrequency))
		f.write('nstxout-compressed  = %d\n'%(outfrequency))
		f.write(' \n')
		f.write('; Bond parameters\n')
		f.write('continuation	        = no\n')
		f.write('constraint_algorithm   = lincs\n')
		f.write('constraints	        = %s\n'%(constraints))
		f.write('lincs_iter	            = 1\n')
		f.write('lincs_order	        = 4\n')
		f.write(' \n')
		f.write('; Neighborsearching\n')
		f.write('cutoff-scheme   = Verlet\n')
		f.write('ns_type		 = grid\n')
		f.write('nstlist		 = 10\n')
		f.write('rcoulomb	     = %.2f\n'%(rcoulomb))
		f.write('rvdw		     = %.2f\n'%(rvdw))
		f.write(' \n')
		f.write('; Electrostatics\n')
		f.write('coulombtype	    = PME\n')
		f.write('pme_order	        = 4\n')
		f.write('fourierspacing	    = 0.16\n')
		f.write(' \n')
		f.write('; Temperature coupling is on\n')
		f.write('tcoupl		= %s\n'%(tcoupl))
		f.write('tc-grps	= system\n')
		f.write('tau_t		= 0.1\n')
		f.write('ref_t		= %.2f\n'%(ref_t))
		f.write(' \n')
		if ensemble=='nvt':
			f.write('; Pressure coupling is off\n')
			f.write('pcoupl		= no\n')
		if ensemble=='npt':
			f.write('; Pressure coupling is on\n')
			f.write('pcoupl		  = %s\n'%(pcoupl))
			f.write('pcoupltype	  = %s\n'%(pcoupltype))
			f.write('tau_p		  = 2.0\n')
			f.write('ref_p		  = %.2f\n'%(ref_p))
			f.write('compressibility     = 4.5e-5\n')
		f.write(' \n')
		f.write('; Periodic boundary conditions\n')
		f.write('pbc		= xyz\n')
		f.write(' \n')
		f.write('; Dispersion correction\n')
		f.write('DispCorr	= EnerPres\n')
		f.write(' \n')
		f.write('; Velocity generation\n')
		f.write('gen_vel		= yes\n')
		f.write('gen_temp	= %.2f\n'%(ref_t))
		f.write('gen_seed	= -1\n')
		
def Standmdp(mdpname,ensemble='nvt',dt=0.002,nsteps = 10000,outfrequency=500,rcoulomb=1.00,rvdw=1.00,tcoupl='V-rescale',\
ref_t=300.0,pcoupl='=Parrinello-Rahman',pcoupltype='isotropic',ref_p=1.0,GB='off',QMMM='off',Anneal='on',annealmethod='single',\
npoints=30,deltT=10.0,timepoint=500,temperatureStart=100,simulationState='new',constraints='all-bonds',walls='off',\
pull='off',rotation='off',NMR='off',freeenergy='off',nemd='off',tempering='off',electric='off',electrophysiology='off'):
	'''
	mdpname : the name of the mdp file
	ensemble : nvt or npt
	dt : timesteps, default= 0.002
	nsteps : run steps, default=1000000
	outfrequency : outfrequency*dt=1 ps, default=500
	rcoulomb : cut-off distances of electrostatic interaction,default=1.0
	rvdw: cut-off distances of vdw interaction,default=1.0
	tcoupl : temperature coupling method, berendsen,nose-hoover,andersen,andersen-massive,\
	v-rescale, default=v-rescale
	ref_t : reference temperature for coupling (one for each group in tc-grps), default=300.0K
	pcoupl : if ensemble ='npt',pressure coupling on,berendsen,Parrinello-Rahman, default= Parrinello-Rahman,\
	         default=Parrinello-Rahman
	pcoupltype : isotropic,semiisotropic,anisotropic,surface-tension, default=isotropic
	ref_p : reference pressure for coupling, default= 1.0
	GB : implicit solvent algorithm, default = off
	QMMM : quantum mechanics and molecular mechanics,default = off
	anneal : simulated annealing,default = on
	annealmethod : Type of annealing for each temperature group, no/single/periodic, default=single
	npoints : Number of time points to use for specifying annealing in each group, default=30
	deltT : The rate of temperature rise at each step.
	timepoint : List of times at the annealing points for each group, default=1000ps
	temperatureStart : define the annealing start temperature, default = 100K
	simulationState : define is a new simulation or continue, defaule='new'
	constraints : define the constraint method, default='all-bonds' 
	walls : define the wall in topology, default='off'
	pull : define the potential of mean force calculated method,default='off', if on ,the method=Umbrella
	rotation : define the enforced rotation method,default='off'
	NMR : NMR refinement stuff,default='off'
	freeenergy : start free energy calculation,default='off'
	nemd : Non-equilibrium MD stuff, default='off'
	tempering : simulated tempering variables, default='off'
	electric : Electric fields,default='off'
	electrophysiology : Ion/water position swapping for computational electrophysiology setups, default='off'
	reference: https://www.mpibpc.mpg.de/grubmueller/compel
	'''
	with open('%s.mdp'%(mdpname),'w') as f:
		f.write('; This mdp file generated by Gmxmdp.py. \n')
		f.write('; Author: Ruan Yang\n')
		f.write('; https://github.com/ruanyangry \n')
		f.write('; mdout.mdp template\n')
		f.write(' \n')
		f.write(';RUN CONTROL PARAMETERS\n')
		f.write('integrator               = md\n')
		f.write('tinit                    = 0\n')
		f.write('dt                       = %.5f\n'%(dt))
		f.write('nsteps                   = %d\n'%(nsteps))
		f.write('init-step                = 0\n')
		f.write('simulation-part          = 1\n')
		f.write('comm-mode                = Linear\n')
		f.write('nstcomm                  = 100\n')
		f.write('comm-grps                =\n')
		f.write(' \n')
		f.write('; LANGEVIN DYNAMICS OPTIONS\n')
		f.write('bd-fric                  = 0\n')
		f.write('ld-seed                  = -1\n')
		f.write(' \n')
		f.write('; ENERGY MINIMIZATION OPTIONS\n')
		f.write('emtol                    = 1000.00\n')
		f.write('emstep                   = 0.01\n')
		f.write('niter                    = 20\n')
		f.write('fcstep                   = 0\n')
		f.write('nstcgsteep               = 1000\n')
		f.write('nbfgscorr                = 10\n')
		f.write(' \n')
		f.write('; TEST PARTICLE INSERTION OPTIONS\n')
		f.write('rtpi                     = 0.05\n')
		f.write(' \n')
		f.write('; OUTPUT CONTROL OPTIONS\n')
		f.write('nstxout                  =%d\n'%(outfrequency))
		f.write('nstvout                  =%d\n'%(outfrequency))
		f.write('nstfout                  =%d\n'%(outfrequency))
		f.write('nstlog                   =%d\n'%(outfrequency))
		f.write('nstcalcenergy            =%d\n'%(outfrequency))
		f.write('nstenergy                =%d\n'%(outfrequency))
		f.write('nstxout-compressed       =0\n')
		f.write('compressed-x-precision   =%d\n'%(outfrequency))
		f.write('compressed-x-grps        = \n')
		f.write('energygrps               = \n')
		f.write(' \n')
		f.write('; NEIGHBORSEARCHING PARAMETERS\n')
		f.write('cutoff-scheme            = Verlet\n')
		f.write('nstlist                  = 1\n')
		f.write('pbc                      = xyz\n')
		f.write('periodic-molecules       = no\n')
		f.write('verlet-buffer-tolerance  = 0.005\n')
		f.write('rlist                    = 1\n')
		f.write('rlistlong                = -1\n')
		f.write('nstcalclr                = -1\n')
		f.write(' \n')
		f.write('; OPTIONS FOR ELECTROSTATICS AND VDW\n')
		f.write('coulombtype              = PME\n')
		f.write('coulomb-modifier         = Potential-shift-Verlet\n')
		f.write('rcoulomb-switch          = 0.8\n')
		f.write('rcoulomb                 = %.2f\n'%(rcoulomb))
		f.write('epsilon-r                = 1\n')
		f.write('epsilon-rf               = 0\n')
		f.write('vdw-type                 = Cut-off\n')
		f.write('vdw-modifier             = Potential-shift-Verlet\n')
		f.write('rvdw-switch              = 0.8\n')
		f.write('rvdw                     = %.2f\n'%(rvdw))
		f.write('DispCorr                 = EnerPres\n')
		f.write('table-extension          = 1\n')
		f.write('energygrp-table          = \n')
		f.write('fourierspacing           = 0.12\n')
		f.write('fourier-nx               = 0\n')
		f.write('fourier-ny               = 0\n')
		f.write('fourier-nz               = 0\n')
		f.write('pme-order                = 4\n')
		f.write('ewald-rtol               = 1e-05\n')
		f.write('ewald-rtol-lj            = 0.001\n')
		f.write('lj-pme-comb-rule         = Geometric\n')
		f.write('ewald-geometry           = 3d\n')
		f.write('epsilon-surface          = 0\n')
		f.write(' \n')
		if GB=='on':
			f.write('; IMPLICIT SOLVENT ALGORITHM\n')
			f.write('implicit-solvent         = No\n')
			f.write('gb-algorithm             = Still\n')
			f.write('nstgbradii               = 1\n')
			f.write('rgbradii                 = 1\n')
			f.write('gb-epsilon-solvent       = 80\n')
			f.write('gb-saltconc              = 0\n')
			f.write('gb-obc-alpha             = 1\n')
			f.write('gb-obc-beta              = 0.8\n')
			f.write('gb-obc-gamma             = 4.85\n')
			f.write('gb-dielectric-offset     = 0.009\n')
			f.write('sa-algorithm             = Ace-approximation\n')
			f.write('sa-surface-tension       = -1\n')
			f.write(' \n')
		f.write('; OPTIONS FOR WEAK COUPLING ALGORITHMS\n')
		f.write('tcoupl                   = %s\n'%(tcoupl))
		f.write('nsttcouple               = -1\n')
		f.write('nh-chain-length          = 10\n')
		f.write('print-nose-hoover-chain-variables = no\n')
		f.write('tc-grps                  = system\n')
		f.write('tau-t                    = 0.1\n')
		f.write('ref-t                    =%.2f\n'%(ref_t))
		if ensemble=='nvt':
			f.write('; Pressure coupling is off\n')
			f.write('pcoupl		          = no\n')
		if ensemble=='npt':
			f.write('; Pressure coupling is on\n')
			f.write('pcoupl		          = %s\n'%(pcoupl))
			f.write('pcoupltype	          = %s\n'%(pcoupltype))
			f.write('tau_p		          = 2.0\n')
			f.write('ref_p		          = %.2f\n'%(ref_p))
			f.write('nstpcouple           = -1\n')
			f.write('compressibility      = 4.5e-5\n')
		f.write(' \n')
		f.write('; Scaling of reference coordinates, No, All or COM\n')
		f.write('refcoord-scaling         = No\n')
		f.write('\n')
		if QMMM=='on':
			f.write('; OPTIONS FOR QMMM calculations\n')
			f.write('QMMM                     = no\n')
			f.write('QMMM-grps                =\n')
			f.write('QMmethod                 =\n')
			f.write('QMMMscheme               = normal\n')
			f.write('QMbasis                  = \n')
			f.write('QMcharge                 =\n')
			f.write('QMmult                   = \n')
			f.write('SH                       =\n')
			f.write('CASorbitals              =\n')
			f.write('CASelectrons             =\n')
			f.write('SAon                     =\n')
			f.write('SAoff                    =\n')
			f.write('SAsteps                  =\n')
			f.write('MMChargeScaleFactor      = 1\n')
			f.write('bOPT                     =\n')
			f.write('bTS                      =\n')
		if Anneal=='on':
			f.write('; SIMULATED ANNEALING \n')
			f.write('annealing                = %s\n'%(annealmethod))
			f.write('annealing-npoints        = %d\n'%(npoints))
			simulttime=[str(i*timepoint) for i in range(npoints)]
			simulttime=' '.join(simulttime)
			f.write('annealing-time           = %s\n'%(simulttime))
			temperaure=[str(temperatureStart+i*deltT) for i in range(npoints)]
			temperaure=' '.join(temperaure)
			f.write('annealing-temp           = %s\n'%(temperaure))
			f.write(' \n')
		if simulationState=='new':
			f.write('; GENERATE VELOCITIES FOR STARTUP RUN\n')
			f.write('gen-vel                  = yes\n')
			f.write('gen-temp                 = %.2f\n'%(ref_t))
			f.write('gen-seed                 = -1\n')
			f.write('\n')
		else:
			f.write('; GENERATE VELOCITIES FOR STARTUP RUN\n')
			f.write('gen-vel                  = no\n')
			f.write('gen-temp                 = %.2f\n'%(ref_t))
			f.write('gen-seed                 = -1\n')
			f.write('\n')
		f.write('; OPTIONS FOR BONDS\n')
		f.write('constraints              = %s\n'%(constraints))
		f.write('constraint-algorithm     = Lincs\n')
		f.write('continuation             = no\n')
		f.write('Shake-SOR                = no\n')
		f.write('shake-tol                = 0.0001\n')
		f.write('lincs-order              = 4\n')
		f.write('lincs-iter               = 1\n')
		f.write('lincs-warnangle          = 30\n')
		f.write('morse                    = no\n')
		f.write('\n')
		f.write('; ENERGY GROUP EXCLUSIONS\n')
		f.write('energygrp-excl           =\n')
		f.write('\n')
		if walls=='on':
			f.write('nwall                    = 0\n')
			f.write('wall-type                = 9-3\n')
			f.write('wall-r-linpot            = -1\n')
			f.write('wall-atomtype            =\n')
			f.write('wall-density             =\n')
			f.write('wall-ewald-zfac          = 3\n')
			f.write('\n')
		if pull=='on':
			f.write('pull                     = yes\n')
			f.write('pull_ngroups             = 2\n')
			f.write('pull_ncoords             = 1\n')
			f.write('pull_group1_name         = Chain_B\n')
			f.write('pull_group2_name         = Chain_A \n')
			f.write('pull_coord1_type         = umbrella\n')
			f.write('pull_coord1_geometry     = distance \n')
			f.write('pull_coord1_groups	      = 1 2\n')
			f.write('pull_coord1_dim          = N N Y\n')
			f.write('pull_coord1_rate         = 0.01\n')
			f.write('pull_coord1_k            = 1000\n')
			f.write('pull_coord1_start        = yes\n')	
			f.write('\n')
		if rotation=='on':
			f.write(';Exemplary GROMACS .mdp file entries for enforced rotation\n')
			f.write('; Reference :http://www.mpibpc.mpg.de/grubmueller/rotation\n')
			f.write('; ENFORCED ROTATION\n')
			f.write('rotation                 = Yes\n')
			f.write('; Output frequency for angle, torque and rotation potential energy for the whole group\n')
			f.write('rot-nstrout              = 1\n')
			f.write('; Output frequency for per-slab data (angles, torques and slab centers)\n')
			f.write('rot-nstsout              = 10\n')
			f.write('; Number of rotation groups\n')
			f.write('rot-ngroups              = 1\n')
			f.write('; Rotation group name \n')
			f.write('rot-group0               = System\n')
			f.write('; Rotation potential. Can be iso, iso-pf, pm, pm-pf, rm, rm-pf, rm2, rm2-pf, flex, flex-t, flex2, flex2-t\n')
			f.write('rot-type0                = flex2-t\n')
			f.write('; Use mass-weighting of the rotation group positions\n')
			f.write('rot-massw0               = yes\n')
			f.write('; Rotation vector, will get normalized\n')
			f.write('rot-vec0                 = 1 0 0\n')
			f.write('; Pivot point for the potentials iso, pm, rm, and rm2 [nm]\n')
			f.write('rot-pivot0               = 4.31852e+00  1.73201e+00  1.89800e+00\n')
			f.write('; Rotation rate [degree/ps] and force constant [kJ/(mol*nm^2)]\n')
			f.write('rot-rate0                = 10.0\n')
			f.write('rot-k0                   = 500.0\n')
			f.write('; Slab distance for flexible axis rotation [nm]\n')
			f.write('rot-slab-dist0           = 1.5\n')
			f.write('; Minimum value of Gaussian function for the force to be evaluated (for flex* potentials)\n')
			f.write('rot-min-gauss0           = 0.001\n')
			f.write('; Value of additive constant epsilon [nm^2] for rm2* and flex2* potentials\n')
			f.write('rot-eps0                 = 0.0001\n')
			f.write('; Fitting method to determine angle of rotation group (rmsd, norm, or potential)\n')
			f.write('rot-fit-method0          = norm\n')
			f.write('; For fit type ''potential'', nr. of angles around the reference for which the pot. is evaluated\n')
			f.write('rot-potfit-nsteps0       = 21\n')
			f.write('; For fit type ''potential'', distance in degrees between two consecutive angles\n')
			f.write('rot-potfit-step0         = 0.25\n')
			f.write('\n')
		f.write('; Group to display and/or manipulate in interactive MD session\n')
		f.write('IMD-group                =\n')
		f.write('\n')
		if NMR=='on':
			f.write('; NMR refinement stuff\n')
			f.write('disre                    = yes\n')
			f.write('disre-weighting          = Conservative\n')
			f.write('disre-mixed              = no\n')
			f.write('disre-fc                 = 1000\n')
			f.write('disre-tau                = 0\n')
			f.write('nstdisreout              = 100\n')
			f.write('orire                    = no\n')
			f.write('orire-fc                 = 0\n')
			f.write('orire-tau                = 0\n')
			f.write('orire-fitgrp             = \n')
			f.write('nstorireout              = 100\n')
			f.write('\n')
		if freeenergy=='on':
			f.write('; Free energy variables\n')
			f.write('free-energy              = yes\n')
			f.write('couple-moltype           =\n')
			f.write('couple-lambda0           = vdw-q\n')
			f.write('couple-lambda1           = vdw-q\n')
			f.write('couple-intramol          = no\n')
			f.write('init-lambda              = -1\n')
			f.write('init-lambda-state        = -1\n')
			f.write('delta-lambda             = 0\n')
			f.write('nstdhdl                  = 50\n')
			f.write('fep-lambdas              =\n')
			f.write('mass-lambdas             =\n')
			f.write('coul-lambdas             =\n')
			f.write('vdw-lambdas              =\n')
			f.write('bonded-lambdas           =\n')
			f.write('restraint-lambdas        =\n')
			f.write('temperature-lambdas      =\n')
			f.write('calc-lambda-neighbors    = 1\n')
			f.write('init-lambda-weights      =\n')
			f.write('dhdl-print-energy        = no\n')
			f.write('sc-alpha                 = 0\n')
			f.write('sc-power                 = 1\n')
			f.write('sc-r-power               = 6\n')
			f.write('sc-sigma                 = 0.3\n')
			f.write('sc-coul                  = no\n')
			f.write('separate-dhdl-file       = yes\n')
			f.write('dhdl-derivatives         = yes\n')
			f.write('dh_hist_size             = 0\n')
			f.write('dh_hist_spacing          = 0.1\n')
			f.write(' \n')
		if nemd=='on':
			f.write('; Non-equilibrium MD stuff\n')
			f.write('acc-grps                 = \n')
			f.write('accelerate               = \n')
			f.write('freezegrps               = \n')
			f.write('freezedim                = \n')
			f.write('cos-acceleration         = 0\n')
			f.write('deform                   = \n')
			f.write('\n')
		if tempering =='on':
			f.write('simulated-tempering      = no\n')
			f.write('simulated-tempering-scaling = geometric\n')
			f.write('sim-temp-low             = 300\n')
			f.write('sim-temp-high            = 300\n')
			f.write('\n')
		if electric =='on':
			f.write('; Electric fields\n')
			f.write('E-x                      =\n')
			f.write('E-xt                     =\n')
			f.write('E-y                      =\n')
			f.write('E-yt                     =\n')
			f.write('E-z                      =\n')
			f.write('E-zt                     =\n')
			f.write('\n')
		if electrophysiology=='on':
			f.write('; Swap coordinates: no, X, Y, Z. Choose Z if your \
			membrane is in the X-Y-plane. Ions will be swapped depending \
			on their Z-positions alone.\n')
			f.write(';https://www.mpibpc.mpg.de/grubmueller/compel\n')
			f.write('swapcoords = Z\n')
			f.write('swap-frequency = 100\n')
			f.write('split-group0 = channel0\n')
			f.write('split-group1 = channel1\n')
			f.write('massw-split0 = no\n')
			f.write('massw-split1 = no\n')
			f.write('solvent-group = SOL\n')
			f.write('coupl-steps = 10\n')
			f.write('iontypes = 3\n')
			f.write('iontype0-name = NA\n')
			f.write('iontype0-in-A = 51\n')
			f.write('iontype0-in-B = 35\n')
			f.write('iontype1-name = K\n')
			f.write('iontype1-in-A = 10\n')
			f.write('iontype1-in-B = 38\n')
			f.write('iontype2-name = CL\n')
			f.write('iontype2-in-A = -1\n')
			f.write('iontype2-in-B = -1\n')
			f.write('bulk-offsetA = 0.0\n')
			f.write('bulk-offsetB = 0.0\n')
			f.write('cyl0-r    = 5.0\n')
			f.write('cyl0-up   = 0.75\n')
			f.write('cyl0-down = 0.75\n')
			f.write('cyl1-r    = 5.0\n')
			f.write('cyl1-up   = 0.75\n')
			f.write('cyl1-down = 0.75\n')
			f.write('threshold = 1\n')
			f.write(' \n')
		f.write('; AdResS parameters\n')
		f.write('adress                   = no\n')
		f.write('\n')