from typing import List
import tempfile
import os
import subprocess
import numpy as np
from CSXCAD.CSXCAD import ContinuousStructure


class FieldDump:
    """
    """

    def __init__(
        self, csx: ContinuousStructure, box: List[List[float]], field_type=0
    ):
        """
        """
        self.csx = csx
        self.unit = 1e-3
        self.box = np.multiply(self.unit, box)
        self.field_type = field_type
        self.dir_path = tempfile.mkdtemp()

        self.field_dump = self.csx.AddDump(
            os.path.join(self.dir_path, "Et_"), file_type=self.field_type
        )
        self.field_dump.AddBox(self.box[0], self.box[1])

    def save(self, dir_path: str):
        """
        """

    def view(self):
        """
        """
        subprocess.run(
            [
                "paraview",
                "--data={}".format(os.path.join(self.dir_path, "Et__..vtr")),
            ]
        )