from os import getcwd, chdir, mkdir, system
from shutil import rmtree
from argparse import ArgumentParser
from datetime import datetime
from uuid import uuid4
from sccdftb_config import SCRATCH_DIR, CHARMM_EXE, SLKO_DIR, ZETA, HUBBARD, HUBBARD_LDEP, CRD2XYZ_EXE


ATOMS = ("H", "C", "N", "O", "S", "P", "CU")


def generate_atom_dict():

    atom_dict = dict()

    for atom in ATOMS:
        atom_dict[atom] = 0

    return atom_dict


def get_time_string():
    d = datetime.now()
    return str(d).replace(" ","_")

def generate_scr_name():
    scr = SCRATCH_DIR + "/" + get_time_string() + "_" + str(uuid4())
    return scr


def get_args():
    parser = ArgumentParser(
        description="Run a DFTB3 calculation through CHARMM.")

    parser.add_argument("--ixyz", "-i", action='store', const=None,
        help="Input .xyz file.")

    parser.add_argument("--oxyz", "-o", action='store', const=None,
        help="Output .xyz file (for geometry optimization).")

    parser.add_argument('--d2', '-d2', action='store_true', default=False,
        help="Add Grimmes's two-body D3(BJ) dispersion correction.")

    parser.add_argument('--d3', '-d3', action='store_true', default=False,
        help="Add Grimmes's three-body D3(BJ) dispersion correction.")

    parser.add_argument('--cpe', '-cpe', action='store_true', default=False,
        help="Use Chemical Potential Equalization correction.")

    parser.add_argument("--minimize", "-m", action='store_true', default=False,
        help="Perform geometry optimization.")

    parser.add_argument("--verbose", "-v", action='store_true', default=False,
        help="Verbose run of CHARMM.")

    parser.add_argument("--clean-up", action='store_true', default=False,
        help="Delete scratch files after completion.")

    parser.add_argument('--scf-tol', "-s" , action='store', default=1e-7,
        help="SCF energy convergence criterion (default:  1e-7 Hartree).")

    parser.add_argument('--charge', "-c" , action='store', default=0.0,
        help="Total charge of the system (default:  0 a.u.).")

    parser.add_argument('--l-dependent', "-ldep" , action='store_true', default=False,
        help="Enable angular momentum-dependent Hubbard derivatives (only required for Cu)")

    args = parser.parse_args()

    return args

def run_charmm(ixyz, clean_up=False, charge=0.0, d2=False, d3=False,
        cpe=False, verbose=False, minimize=False, scf_tol=1e-7,
        oxyz=None, ldep=False):

    scr_dir = generate_scr_name()
    # scr_dir = "/home/andersx/scr/temp"
    try:
        mkdir(scr_dir)
    except:
        pass

    crd_file = scr_dir + "/molecule.crd"

    f = open(ixyz, "r")
    ixyz_lines = f.readlines()
    f.close()

    atom_count = generate_atom_dict()

    total_atoms_count = int(ixyz_lines[0])

    crd_output  = "*  Molecule input for CHARMM\n"
    crd_output += "*  Generated by sccdftb\n"
    crd_output += "*\n""" 
    crd_output += "%5i" % (total_atoms_count) 

    for i, line in enumerate(ixyz_lines[2:]):

        tokens = line.split()

        if len(tokens) < 4:
            break

        atom_type = tokens[0].upper()
        x = float(tokens[1])
        y = float(tokens[2])
        z = float(tokens[3])

        atom_count[atom_type] += 1

        atom_spec = "%s%i" % (atom_type, atom_count[atom_type])
        if len(atom_spec) < 3:
            atom_spec += " "

        crd_string = "\n %4i    1 DFTB %3s %10.5f %9.5f %9.5f DFTB 1      0.00000" % (i + 1,atom_spec, x, y, z)

        crd_output += crd_string

    f = open(crd_file, "w")
    for line in crd_output:
        f.write(line)
    f.close()


    # create molecule.rtf

    rtf_file = scr_dir + "/molecule.rtf"
    
    rtf_output = "31  1\n"
    rtf_output += "\n"
    rtf_output += "MASS     1 H      1.00800 H ! polar H\n"
    rtf_output += "MASS     2 C     12.01100 C ! carbonyl C, peptide backbone\n"
    rtf_output += "MASS     3 N     14.00700 N ! proline N\n"
    rtf_output += "MASS     4 O     15.99900 O ! carbonyl oxygen\n"
    rtf_output += "MASS    15 P     30.97379 P ! phosphorous\n"
    rtf_output += "MASS    16 S     32.06000 S ! sulphur\n"
    rtf_output += "MASS    29 CU    63.54600 CU ! copper\n"
    rtf_output += "\n"
    rtf_output += "DEFA FIRS NONE LAST NONE\n"
    rtf_output += "AUTO ANGLES DIHE\n"
    rtf_output += "\n"
    rtf_output += "RESI DFTB        0.00\n"
    rtf_output += "GROUP\n"

    for atom in ATOMS:
        n = atom_count[atom]
        if n == 0:
            continue
        for i in range(n):
            rtf_output += "ATOM %1s%-3i  %1s     0.00\n" % (atom, i+1, atom)
 
    rtf_output += "\n"
    rtf_output += "END"

    f = open(rtf_file, "w")
    for line in rtf_output:
        f.write(line)
    f.close()

    # print rtf_file

    # create geometry.inp

    inp_output  = "* DFTB input for CHARMM\n"
    inp_output += "*\n"
    inp_output += "\n"
    inp_output += "bomb -5\n"
    inp_output += "wrnlev -5\n"
    inp_output += "\n"
    inp_output += "open read card unit 10 name %s\n" %  rtf_file
    inp_output += "read rtf card unit 10\n"
    inp_output += "close unit 10\n"
    inp_output += "\n"
    inp_output += "read sequence dftb 1\n"
    inp_output += "generate dftb setup noangle nodihedral\n"
    inp_output += "\n"
    inp_output += "open read unit 10 card name %s\n" % crd_file
    inp_output += "read coor unit 10 card append\n"
    inp_output += "close unit 10\n"
    inp_output += "\n"
    if clean_up is False:
        inp_output += "open unit 3 name %s write form\n" % (scr_dir + "/molecule_charmm.psf")
        inp_output += "write psf card unit 3\n"
        inp_output += "\n"
        inp_output += "open unit 3 name %s write form\n" % (scr_dir + "/molecule_charmm.crd")
        inp_output += "write coor card unit 3\n"
        inp_output += "\n"
#    inp_output += "nbonds  atom fshift cdie vdw vshift  -\n"
#    inp_output += "       cutnb 14.0 ctofnb 12.0 ctonnb 10.0 wmin 1.5 eps 1.0 -\n"
#    inp_output += "       inbfrq -1\n"
#    inp_output += "\n"
    inp_output += "define qm sele all end\n"
    inp_output += "\n"

    i = 0
    for atom in ATOMS:
        n = atom_count[atom]
        if n == 0:
            continue
        i += 1

        inp_output += "scalar wmain set %i.0 sele (qm) .and. type %s*  end\n" % (i, atom)

    inp_output += "\n"

    dispersion_correction = ""

    if d2:
        dispersion_correction = "twobod"
    if d3:
        dispersion_correction = "threebod"


    ldep_output = ""
    if ldep:
        ldep_output = "ldep"

    cpe_correction = ""

    if cpe:
        cpe_correction = "cpe"

    inp_output += "sccdftb remove sele qm end temp 0.0 scftol " +  str(scf_tol) + " -\n"
    inp_output += "        chrg %2.1f d3rd hbon mixe 1 %s %s %s\n" % (charge, cpe_correction, dispersion_correction, ldep_output)


    if minimize:

        inp_output += "\n"
        inp_output += "mini abnr nstep 1000\n"
        inp_output += "\n"

    crd_opt = scr_dir + "/molecule_optimized.crd"

    if oxyz is not None:
        
        inp_output += "\n"
        inp_output += "open unit 3 name %s write form\n" % crd_opt
        inp_output += "write coor card unit 3\n"
        inp_output += "\n"

    inp_output += "energy\n"
    inp_output += "\n"
    inp_output += "stop\n"
    inp_output += "\n"
    # print inp_output

    inp_file = scr_dir + "/calculation.inp"

    
    f = open(inp_file, "w")
    for line in inp_output:
        f.write(line)
    f.close()


    # write sccdftb.dat file

    dat_file = scr_dir + "/sccdftb.dat"

    dat_output = ""
    for atom1 in ATOMS:
        for atom2 in ATOMS:
            if atom_count[atom1] > 0 and atom_count[atom2] > 0:

                dat_output += "'%s/%s%s.spl'\n" % (SLKO_DIR, atom1.lower(), atom2.lower())

    HUBBARD_OUTPUT = dict()
    if ldep:
        HUBBARD_OUTPUT = HUBBARD_LDEP
    else:
        HUBBARD_OUTPUT = HUBBARD

    for atom in ATOMS:
        if atom_count[atom] > 0:
            dat_output += "'%s' %s\n" % (atom.lower(), HUBBARD_OUTPUT[atom])

    dat_output += str(ZETA)

    f = open(dat_file, "w")
    for line in dat_output:
        f.write(line)
    f.close()

    # print dat_output

    # run charmm

    work_dir = getcwd()

    chdir(scr_dir)

    if verbose:
        system(CHARMM_EXE + " < " + inp_file + " 2>&1 | tee output.log")
    else:
        system(CHARMM_EXE + " < " + inp_file + " > output.log")

    chdir(work_dir)
    
    f = open(scr_dir + "/output.log")
    output_lines = f.readlines()
    f.close()

    energy = 0.0
    dipole = 0.0

    for line in output_lines:
        if "ENER QUANTM>" in line:
            energy = float(line.split()[2])

        if "Dipol: |mu| =" in line:
            dipole = float(line.split()[3])

    # generate+copy output xyz
    if oxyz is not None:
        system("%s %s > %s " % (CRD2XYZ_EXE, crd_opt, oxyz))

    if clean_up:
        rmtree(scr_dir)

    return energy, dipole
