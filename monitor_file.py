import threading
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def monitor_path(msg_q):
    # def needed vars \ patterns -
    patterns = ["*"]        #
    ignore_patterns = None  #
    ignore_directories = False  #
    case_sensitive = True       #
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted

    path = "songPath_Listen_Together"
    go_recursively = True       #
    my_observer = Observer()    #
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)  #

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()


def on_created(event):
    # return creation status, file_name.
    song_file_name = event.src_path.split("\\")[-1]
    print("00", song_file_name)
    # send to server!


def on_deleted(event):
    # return deletion status, file_name.
    song_file_name = event.src_path.split("\\")[-1]
    print("01", song_file_name)
    # send to server!


if __name__ == "__main__":
    thread_recv_msg = threading.Thread(target=monitor_path).start()
