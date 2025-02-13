# SPDX-FileCopyrightText: 2025-present kleines Filmröllchen <kleines@filmroellchen.eu>
#
# SPDX-License-Identifier: MIT

import asyncio
from pathlib import Path
import time

from watchdog.events import (
    FileSystemEventHandler,
    FileCreatedEvent,
    FileClosedEvent,
    FileMovedEvent,
    FileModifiedEvent,
)
from watchdog.observers import Observer

from .ffmpeg import FFmpegHandler

from concurrent.futures import ThreadPoolExecutor


def thread_event_loop() -> asyncio.AbstractEventLoop:
    try:
        return asyncio.get_event_loop()
    except Exception:
        return asyncio.new_event_loop()


class TranscoderHandler(FileSystemEventHandler):
    def __init__(self, ffmpeg_handler: FFmpegHandler):
        super().__init__()
        self.ffmpeg_handler = ffmpeg_handler
        self.executor = ThreadPoolExecutor(
            max_workers=2, thread_name_prefix="transcode_worker_"
        )

    def run_initial_scan(self, dir: Path):
        for file in dir.glob("**/*"):
            if file.is_file():
                output = self.ffmpeg_handler.associated_output_name(file)
                if not output.exists():
                    self.try_transcode(file)

    def on_moved(self, event):
        # move output files with their inputs
        output = self.ffmpeg_handler.associated_output_name(Path(event.src_path))
        if output.exists():
            new_output = self.ffmpeg_handler.associated_output_name(
                Path(event.dest_path)
            )
            print(f"Renaming output file {output} to {new_output}")
            output.rename(new_output)
        else:
            self.try_transcode(Path(event.dest_path))

    def on_closed(self, event):
        if isinstance(event, FileClosedEvent):
            self.try_transcode(Path(event.src_path))

    def on_created(self, event):
        if isinstance(event, FileCreatedEvent):
            self.try_transcode(Path(event.src_path))

    def try_transcode(self, input: Path):
        if self.ffmpeg_handler.is_output_file(input):
            print(f"{input} is an output file, not transcoding.")
            return
        print(f"New file {input} was created, trying to transcode...")
        try:
            self.executor.submit(
                lambda: thread_event_loop().run_until_complete(
                    self.ffmpeg_handler.transcode(input)
                )
            )
        except Exception as e:
            print(f"Error while running transcode: {e}")


def handle_transcoding(path: Path, ffmpeg_handler: FFmpegHandler):
    event_handler = TranscoderHandler(ffmpeg_handler)

    event_handler.run_initial_scan(path)

    observer = Observer()
    observer.schedule(
        event_handler,
        str(path),
        recursive=True,
        event_filter=[
            FileCreatedEvent,
            FileClosedEvent,
            FileMovedEvent,
            FileModifiedEvent,
        ],
    )
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
