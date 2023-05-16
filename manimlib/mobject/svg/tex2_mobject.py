from __future__ import annotations

import os
import tempfile

from manimlib.mobject.svg.svg_mobject import SVGMobject

class TeX2(SVGMobject):
    def __init__(self, content: str, cmd: str = 'latex', out: str = 'dvi'):
        self.content = content
        self.cmd = cmd
        self.out = out
        super().__init__(file_name=TeX2.tex2svg(content, cmd, out))

    @property
    def hash_seed(self) -> tuple:
        return (
            self.__class__.__name__,
            self.content,
            self.cmd,
            self.out
        )
    
    @staticmethod
    def tex2svg(content: str, cmd: str, out: str) -> str:
        filename = str(abs(hash((content, cmd))))
        rootpath = os.path.join(tempfile.gettempdir(), 'manimgl')
        # rootpath = os.path.join('./', 'manimgl')
        os.makedirs(rootpath, exist_ok=True)
        with open(os.path.join(rootpath, f'{filename}.tex'), 'w') as fout:
            fout.write(content)
        command = f'cd {rootpath} && {cmd} -interaction=batchmode {filename}.tex > {os.devnull}'
        os.system(command)
        command = f'cd {rootpath} && dvisvgm {filename}.{out} -n -v 0 -o {filename}.svg > {os.devnull}'
        os.system(command)
        return os.path.join(rootpath, f'{filename}.svg')