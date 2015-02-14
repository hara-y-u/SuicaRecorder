import reader
import dummy_card_server
from functools import wraps
from cement.core import foundation, controller
from history import History


class CliBaseController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = 'SuicaRecorder utilities.'

        arguments = [
            (['--csv'], dict(action='store_true',
                             help='preffer csv format for output')),
            (['--dev'], dict(action='store_true',
                             help='toggle development mode \
                                   (emulates card touch)'))
        ]

    def prepare_dev(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            if args[0].app.pargs.dev:
                dummy_card_server.start()
            return f(*args, **kwds)
        return wrapper

    def show_histories(self, histories):
        if self.app.pargs.csv:
            print unicode(History.csv_header)
        for history in histories:
            if self.app.pargs.csv:
                print unicode(history.to_csv())
            else:
                print unicode(history) + '\n'

    def on_error(self, error):
        self.app.log.error('An error has occured on reading histories: %s' %
                           error)

    @controller.expose(hide=True, aliases=['run'])
    @prepare_dev
    def default(self):
        self.app.log.info('Inside base.default function.')
        if self.app.pargs.csv:
            self.app.log.info("Recieved option 'format' with value '%s'." %
                              self.app.pargs.csv)

    @controller.expose(help='output suica histories to STDOUT')
    @prepare_dev
    def show(self):
        reader.read_histories(
            self.show_histories,
            self.app.log,
            self.on_error,
            'udp' if self.app.pargs.dev else 'usb'
        )


class CliApp(foundation.CementApp):
    class Meta:
        label = 'suicarecorder'
        base_controller = CliBaseController


def run():
    app = CliApp()
    try:
        app.setup()
        app.run()
    finally:
        app.close()


if __name__ == '__main__':
    run()
