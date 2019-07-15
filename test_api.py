import click

from requests import get


@click.command()
@click.argument('method', type=click.Choice(['ping', 'status', 'add', 'substract']))
@click.option('--dst', default='127.0.0.1:8080', help='Set API address.')
@click.option('--uuid', default='', help='Set UUID.')
@click.option('--value', default=None, help='Set value.')
def main(method, dst, uuid, value):
    json = {'addition': {}}
    if uuid:
        json['addition'].update({'uuid': uuid})
    if value:
        json['addition'].update({'value': value})
    res = get('http://%s/api/%s' % (dst, method), json=json, headers={'Host': 'service_api'})
    print(res.content)


if __name__ == "__main__":
    main()
