# User scratch directory
SCRATCH_DIR = "/home/andersx/scr"

# Executable for CHARMM
CHARMM_EXE = "/home/andersx/dev/charmm_d3/exec/gnu/charmm"

# Executable for CHARMM
CRD2XYZ_EXE = "/home/andersx/charmm-dftb-py/crd2xyz"

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
