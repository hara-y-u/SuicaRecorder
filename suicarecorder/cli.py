# -*- coding: utf-8 -*-

import reader
from cement.core import foundation, controller


class CliBaseController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = 'SuicaRecorder utilities.'

        arguments = [
            (['--csv'], dict(action='store_true',
                             help='preffer csv format for output')),
            (['--dev'], dict(action='store_true',
                             help='toggle development mode'))
        ]

    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        self.app.log.info('Inside base.default function.')
        if self.app.pargs.format:
            self.app.log.info("Recieved option 'format' with value '%s'." %
                              self.app.pargs.format)

    def show_histories(self, histories):
        histories.reverse()
        for history in histories:
            self.app.log.info(unicode('%s' % history))

    def on_error(self, error):
        self.app.log.error('An error has occured on reading histories: %s' %
                           error)

    @controller.expose(help='output suica histories to STDOUT.')
    def show(self):
        reader.read_histories(
            self.show_histories,
            self.app.log,
            self.on_error
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
