# User scratch directory
SCRATCH_DIR = "/home/andersx/scr"

# Executable for CHARMM
CHARMM_EXE = "/home/andersx/dev/charmm_cpe/exec/gnu/charmm"

# Executable for CHARMM
CRD2XYZ_EXE = "/home/andersx/charmm-dftb-py/crd2xyz"

# This directory
D3H4_BIN_DIR = "/home/andersx/dev/charmm-dftb-py/d3h4_bin"

# Directory for the Slater-Koster files
SLKO_DIR = "/home/andersx/dev/slko-3OB_distribute130926"

# Zeta parameter
ZETA = 4.00

# Values of the Hubbard derivatives
HUBBARD = dict()
HUBBARD["C"]  = "-0.1492"
HUBBARD["H"]  = "-0.1857"
HUBBARD["N"]  = "-0.1535"
HUBBARD["O"]  = "-0.1575"
HUBBARD["S"]  = "-0.1100"
HUBBARD["P"]  = "-0.1400"
HUBBARD["CU"] = "-0.1400"


# Values of the angular momentum-dependent Hubbard derivatives
HUBBARD_LDEP = dict()
HUBBARD_LDEP["C"]  = "-0.1492 -0.1492 -0.1492"
HUBBARD_LDEP["H"]  = "-0.1857 -0.1857 -0.1857"
HUBBARD_LDEP["N"]  = "-0.1535 -0.1535 -0.1535"
HUBBARD_LDEP["O"]  = "-0.1575 -0.1575 -0.1575"
HUBBARD_LDEP["S"]  = "-0.1100 -0.1100 -0.1100"
HUBBARD_LDEP["P"]  = "-0.1400 -0.1400 -0.1400"
HUBBARD_LDEP["CU"] = "-0.2000 -0.0575 -0.0575"

SPIN_VAL = dict()

SPIN_VAL["H"]  = "spin-h      -0.07174    0.00000    0.00000     0.00000    0.00000    0.00000     0.00000    0.00000    0.00000"
SPIN_VAL["C"]  = "spin-c      -0.03062   -0.02505   -0.02505    -0.02265    0.00000    0.00000     0.00000    0.00000    0.00000"
SPIN_VAL["N"]  = "spin-n      -0.03318   -0.02755   -0.02755    -0.02545    0.00000    0.00000     0.00000    0.00000    0.00000"
SPIN_VAL["O"]  = "spin-o      -0.03524   -0.02956   -0.02956    -0.02785    0.00000    0.00000     0.00000    0.00000    0.00000"
SPIN_VAL["P"]  = "spin-p      -0.02062   -0.01609   -0.01609    -0.01490    0.00027   -0.00018    -0.08000    0.00027   -0.00018" 
SPIN_VAL["S"]  = "spin-s      -0.02137   -0.01699   -0.01699    -0.01549    0.00015   -0.00006    -0.08000    0.00015   -0.00006" 
SPIN_VAL["CU"] = "spin-cu     -0.01703   -0.01239   -0.01239    -0.04293   -0.00281    0.00052    -0.01738   -0.00281    0.00052"
