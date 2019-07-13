import click

from requests import get


@click.command()
@click.argument('method', type=click.Choice(['ping', 'status', 'add', 'substract']))
@click.option('--dst', default='127.0.0.1:5000')
@click.option('--uuid', default='')
@click.option('--value', default=0)
def main(method, dst, uuid, value):
    json = {'addition': {}}
    if uuid:
        json['addition'].update({'uuid': uuid})
    if value:
        json['addition'].update({'value': value})
    res = get('http://%s/api/%s' % (dst, method), json=json)
    print(res.content)


if __name__ == "__main__":
    main()
