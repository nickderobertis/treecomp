import os
import time
from pathlib import Path

import terminhtml_recorder.recorder
from terminhtml_recorder import OutputFormat, PageLocators, default_page_interactor
from terminhtml_recorder.cli import record

RecordConfig = record.model_cls

is_ci = os.getenv("CI")
delay = 2.8 if is_ci else 1.1


def page_interactor(page_locators: PageLocators) -> None:
    page_locators.speed_up.click()
    default_page_interactor(page_locators)
    time.sleep(1.5)


config = RecordConfig(
    in_path=None,
    out_path=None,
    output_format=OutputFormat.GIF,
    delay=1.1,
    interactor=page_interactor,
)
