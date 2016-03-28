from contextlib import contextmanager
import sys
import traceback


class TaskError(Exception):

    pass


class TaskWarning(Exception):

    pass


@contextmanager
def capture_errors(opts):
    try:
        yield
    except TaskWarning as ex:
        sys.stdout.write("WARNING!\n")
        sys.stdout.write("* {}\n".format(ex.args[0]))
    except KeyboardInterrupt:
        sys.stdout.write("ABORTED!\n")
        sys.exit(1)
    except Exception as ex:
        sys.stdout.write("ERROR!\n")
        sys.stdout.write("{}\n".format(ex.args[0] if isinstance(ex, TaskError) else "Unexpected error."))
        if opts.traceback:
            traceback.print_exc(file=sys.stdout)
        sys.exit(1)
    finally:
        sys.stdout.flush()


@contextmanager
def mark_task(opts, description):
    sys.stdout.write("{}... ".format(description))
    sys.stdout.flush()
    with capture_errors(opts):
        yield
        sys.stdout.write("done!\n")
