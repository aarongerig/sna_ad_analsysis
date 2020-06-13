# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from scrapy.selector import Selector


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Parses HTML data into usable company data.
    """
    logger = logging.getLogger(__name__)
    logger.info('parse raw HTML data into usable company data')

    with click.open_file(input_filepath, 'r') as f:
        body = f.read()
        document = Selector(text=body)
        companies = []

        for company in document.css('.tx-institution-management .accordeon'):
            name = company.xpath('.//span[contains(@class, "institution-accordeon-header-title")]/text()')\
                .get(default='')
            address = company.xpath('.//span[contains(@class, "address")]/text()').get(default='')
            city = company.xpath('.//span[contains(@class, "institution-accordeon-header-left")]/text()').getall()
            phone = company.xpath('.//span[contains(@class, "phone")]/text()').getall()
            email = company.xpath('.//span[contains(@class, "email")]/a/text()').getall()
            website = company.xpath('.//span[contains(@class, "www")]/a/text()').getall()

            city = [item for item in city if item.strip()]
            phone = [item for item in phone if item.strip()]
            email = [item for item in email if item.strip()]
            website = [item for item in website if item.strip()]

            companies.append({
                'name': name.strip(),
                'address': address.strip(),
                'city': '' if not city else city[0].strip(),
                'phone': '' if not phone else phone[0].strip(),
                'email': '' if not email else email[0].strip(),
                'website': '' if not website else website[0].strip(),
            })

        df = pd.DataFrame(companies)
        df.to_csv(output_filepath)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

