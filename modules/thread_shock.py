import time
import threading
from concurrent.futures import ThreadPoolExecutor


class ThreadShock:
    def __init__(self):
        self.max_conection = 20
        self.__time_sleep = 1

    def exec_thread(self, _function_name, _command_str, _target_list, _mix):
        if _function_name and _command_str and _target_list:
            try:
                list_threads = []
                for tgt_str in _target_list:
                    if tgt_str:
                        while threading.active_count() > self.max_conection:
                            time.sleep(self.__time_sleep)
                        thread = threading.Thread(
                            target=_function_name, args=(
                                tgt_str, _command_str, _mix,)
                        )
                        list_threads.append(thread)
                        thread.start()
                for thread in list_threads:
                    thread.join()
            except:
                pass


    def main_pool_thread(self, _function_name, _target, _command, _exploit: list):
        return self.setting_main_pool_thread(_function_name, [_target], [_command], [_exploit])


    def setting_main_pool_thread(self, _function_name, _target, _command, _exploit: list):
        try:
            executor = ThreadPoolExecutor(max_workers=self.max_conection)
            executor.map(_function_name, _target, _command, _exploit)
            executor.shutdown(wait=True)
            executor.shutdown()
        except Exception as err:
            print(err)
            pass
