import numpy as np
import sys

# Get path to mcdc (not necessary if mcdc is installed)
sys.path.append('../../../')

import mcdc

# =============================================================================
# Set materials
# =============================================================================

SigmaC = np.array([0.0])
SigmaS = np.array([[0.9]])
SigmaF = np.array([[0.1]])
nu     = np.array([6.0])
M1 = mcdc.Material(SigmaC, SigmaS, SigmaF, nu)

SigmaC = np.array([0.68])
SigmaS = np.array([[0.2]])
SigmaF = np.array([[0.12]])
nu     = np.array([2.5])
M2 = mcdc.Material(SigmaC, SigmaS, SigmaF, nu)

# =============================================================================
# Set cells
# =============================================================================

# Set surfaces
S0 = mcdc.SurfacePlaneX(0.0, "vacuum")
S1 = mcdc.SurfacePlaneX(1.5)
S2 = mcdc.SurfacePlaneX(2.5, "vacuum")

# Set cells
C1 = mcdc.Cell([+S0, -S1], M1)
C2 = mcdc.Cell([+S1, -S2], M2)
cells = [C1, C2]

# =============================================================================
# Set source
# =============================================================================

# Position distribution
pos = mcdc.DistPoint(mcdc.DistUniform(0.0, 2.5), mcdc.DistDelta(0.0), 
                             mcdc.DistDelta(0.0))
# Direction distribution
dir = mcdc.DistPointIsotropic()

# Energy group distribution
g = mcdc.DistDelta(0)

# Time distribution
time = mcdc.DistDelta(0.0)

# Create the source
Src = mcdc.SourceSimple(pos,dir,g,time)
sources = [Src]

# =============================================================================
# Set filters and tallies
# =============================================================================

spatial_filter = mcdc.FilterPlaneX(np.array([0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05, 1.2, 1.35, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5]))

T = mcdc.Tally('tally', scores=['flux-face'], spatial_filter=spatial_filter)

tallies = [T]

# =============================================================================
# Set and run simulator
# =============================================================================

# Set speed
speeds = np.array([1.0])

# Set simulator
simulator = mcdc.Simulator(speeds, cells, sources, tallies=tallies, 
                           N_hist=1000)

# Set k-eigenvalue mode parameters
simulator.set_kmode(N_iter=110)
simulator.set_pct("DD")

# Run
simulator.run()
