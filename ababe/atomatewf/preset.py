from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import datetime
from pymatgen.io.vasp.sets import MPRelaxSet, MPStaticSet
from fireworks import Firework, Workflow
from atomate.vasp.fireworks.core import OptimizeFW, StaticFW


def wf_optimize_static_energy(structure, c=None):
    """
    Returns optimized structure static energy workflow.
    Args:
        structure (Structure): input structure.
        vasp_input_set_relax (VaspInputSet)
        vasp_input_set_static (VaspInputSet)
        vasp_cmd (str): vasp command to run.
        db_file (str): path to the db file.
        user_kpoints_settings (dict): example: {"grid_density": 7000}
    Returns:
        Workflow
    """
    c = c or {}
    vasp_cmd = c.get("VASP_CMD", VASP_CMD)
    db_file = c.get("DB_FILE", DB_FILE)

    tag = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S-%f')
    vis_relax = MPRelaxSet(structure, force_gamma=True)
    # Structure optimization firework
    fws = [OptimizeFW(structure=structure, vasp_input_set=vis_relax,
                      vasp_cmd=vasp_cmd, db_file=db_file,
                      name="{} structure optimization".format(tag))]

    parents = fws[0]
    fw_static = StaticFW(structure=structure, parents=parents,
                         name="{} structure scf".format(tag))
    fws.append(fw_static)
    wf_static_energy = Workflow(fws)
    wf_static_energy.name = "{}:{}".format(structure.composition.reduced_formula,
                                           "optimize static energy")

    return wf_static_energy
