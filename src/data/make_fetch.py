# -*- coding: utf-8 -*-
import requests
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('output_filepath', type=click.Path())
def main(output_filepath):
    """ Fetches data by scraping a website's content and saves raw HTML into data/raw.
    """
    logger = logging.getLogger(__name__)
    logger.info('fetch raw HTML data from website')

    r = requests.get('https://willisau.ch/wirtschaft-entwicklung/wirtschaft/firmenverzeichnis/')
    with click.open_file(output_filepath, 'w') as f:
        f.write(r.text)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

