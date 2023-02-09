import threading
from runner.base_runner import BaseRunner


class ThreadRunner(threading.Thread):

    def __init__(self, runner: BaseRunner):
        threading.Thread.__init__(self)

        self.runner: BaseRunner = runner
        self.running: bool = True
        self.allow = False

    def run(self) -> None:
        
        while self.running:

            if self.allow:
                pass

    def get_runner(self) -> BaseRunner:
        return self.runner

    
    def toggle_running(self, run: bool) -> None:
        self.allow = run

    def exit(self) -> None:
        self.running = False
