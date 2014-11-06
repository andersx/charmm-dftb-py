from argparse import ArgumentParser
from datetime import datetime
from uuid import uuid4
from sccdftb_config import SCRATCH_DIR, CHARMM_EXE

ATOMS = ("H", "C", "N", "O", "S", "P")


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

    parser.add_argument('--d2', '-d2', action='store_const', const=2)
    parser.add_argument('--d3', '-d3', action='store_const', const=3)
    parser.add_argument('--cpe', '-cpe', action='store_const', const=3)

    parser.add_argument("--minimize", "-m", action='store_true',
        help="Perform geometry optimization.")

    parser.add_argument("--verbose", "-v", action='store_true',
        help="Verbose run of CHARMM.")

    parser.add_argument("--clean-up", action='store_true',
        help="Delete scratch files after completion.")

    parser.add_argument('--scf-tol', "-s" , action='store', const=None,
        help="SCF energy convergence criterion (default:  1e-7 Hartree).")

    parser.add_argument('--charge', "-c" , action='store', const=None,
        help="Total charge of the system (default:  0 a.u.).")


    args = parser.parse_args()

    return args



