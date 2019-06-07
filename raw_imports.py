def do_import():
    import collections
    return collections


def call_times(times=100):
    for i in range(times):
        do_import()


if __name__ == "__main__":
    call_times(times=100)
