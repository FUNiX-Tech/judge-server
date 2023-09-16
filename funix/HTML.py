from dmoj.executors.python_executor import PythonExecutor


class Executor(PythonExecutor):
    name = 'html5'
    command = 'python3'
    command_paths = ['python%s' % i for i in ['3.6', '3.5', '3.4', '3.3', '3.2', '3.1', '3']]
    test_program = """
import sys
if sys.version_info.major == 3:
    print(sys.stdin.read(), end='')
"""
    def create_files(self, problem_id: str, source_code: bytes, *args, **kwargs) -> None:
        if source_code.decode() == self.test_program:
            super().create_files(problem_id, source_code,  **kwargs)
        else:
            super().create_files(problem_id, "print('')".encode("utf-8"),  **kwargs)


    @classmethod
    def get_runtime_versions(cls):
        return [('html', (5,0,0)),]

