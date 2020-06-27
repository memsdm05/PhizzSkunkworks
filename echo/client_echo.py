import websockets
import argparse
import asyncio
import sys
import logging

logging.basicConfig(format='[%(asctime)-15s][CLIENT] %(message)s', level=logging.INFO, stream=sys.stdout)

async def handler(uri, id):

    try:
        async with websockets.connect(uri) as conn:
            canID = args.conns > 1

            if canID:
                logging.info(f'[{id}] Connected to {uri}')
            else:
                logging.info(f'Connected to {uri}')

            if args.inital != '':
                if canID:
                    logging.info(f'[{id}] Initally sent "{args.inital}{id}"')
                    await conn.send(args.inital + str(id))
                else:
                    logging.info(f'Initally sent "{args.inital}"')
                    await conn.send(args.inital)


            async for message in conn:
                if args.echo == '':
                    if canID:
                        logging.info(f'[{id}] Echoed: "{message}"')
                    else:
                        logging.info(f'Echoed: "{message}"')
                    await conn.send(message)
                else:
                    if canID:
                        logging.info(f'[{id}] Recieved message and sent: "{message}"')
                    else:
                        logging.info(f'Recieved message and sent: "{message}"')
                    await conn.send(args.echo)

                if args.once:
                    if canID:
                        logging.info(f'[{id}] Ran once, closing')
                    else:
                        logging.info('Ran once, closing')
                    break

                # speed up time if no delay
                if args.delay > 0:
                    await asyncio.sleep(args.delay)
    except Exception as e:
        sys.stderr.write(f'Could not open connection to {uri}\n')
        print(e)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Websocket echo client meant to stimulate a bot",
                                     epilog="Custom made for Phizz development, so not that fast")
    parser.add_argument('--port', '-p', dest='port', type=int, default=4000,
                        help='The port to connect to (default: 4000)')
    parser.add_argument('--ip', '-I', dest='ip', type=str, default='localhost',
                        help='The uri to connect to (default: localhost)')
    parser.add_argument('--connections', '-c', dest='conns', type=int, default=1,
                        help='How many connections to the ws server (default: 1)')
    parser.add_argument('--wsuri', '-w', dest='uri', type=str, default='',
                        help='The uri of the ws connection. Overwrites PORT and IP')
    parser.add_argument('--delay', '-d', dest='delay', type=float, default=0,
                        help='Artificial delay')
    parser.add_argument('--echo_back', '-e', dest='echo', type=str, default='',
                        help='The message to send back instead of an echo')
    parser.add_argument('--run_once', '-o', dest='once', action='store_true', default=False,
                        help='Echo once then close')

    args = parser.parse_args()

    if args.uri == '':
        u = f'ws://{args.ip}:{args.port}'
    else:
        u = args.uri
    loop = asyncio.get_event_loop()


    for id in range(args.conns):
         loop.create_task(handler(u, id))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Keyboard Interupt, exiting...')
