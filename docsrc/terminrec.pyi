from pathlib import Path
from typing import Callable, Optional

import terminhtml_recorder.recorder
from pydantic import BaseModel
from terminhtml_recorder import OutputFormat, PageLocators, default_page_interactor
from terminhtml_recorder.cli import record

class RecordConfig(BaseModel):
    in_path: Optional[Path] = None
    out_path: Optional[Path] = None
    output_format: Optional[OutputFormat] = OutputFormat.GIF
    delay: Optional[float] = 1.1
    interactor: Optional[
        Callable[[terminhtml_recorder.recorder.PageLocators], None]
    ] = default_page_interactor

config: RecordConfig
