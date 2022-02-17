import click
from datetime import datetime
import kind._kind as kind
import sys

class Date(click.ParamType):
    name = "date"

    def convert(self, value, param, ctx):
        try:
            value = datetime.strptime(value, "%Y-%m-%d")
        except:
            self.fail(
                f"invalid date format, ensure the date format is YYYY-MM-DD eg. 2022-01-01",
                param,
                ctx,
            )
    
        return value

@click.command()
@click.option('--company', required=True, help='Company symbol')
@click.option('--start', type=Date(), help='Start date')
@click.option('--end', type=Date(), help='End date')
def search(company, start, end):
    if start == None:
        start = datetime(datetime.now().year, 1, 1)
        
    if end == None:
        end = datetime(datetime.now().year, 3, 31)
        
    print(f"Searching KIND for disclosure of company symbol {company} for periods between {datetime.strftime(start, '%Y-%m-%d')} to {datetime.strftime(end, '%Y-%m-%d')}")
    
    try:
        search_results = kind.search(company, start, end)
        for search_result in search_results:
            if search_result["title"] == "주주총회소집결의":
                search_result["title"] = "Agenda"
            elif search_result["title"] == "주주총회소집공고":
                search_result["title"] = "Notice of Meeting"
            elif search_result["title"] == "참고서류":
                search_result["title"] = "Reference Document"
            elif search_result["title"] == "감사보고서":
                search_result["title"] = "Auditor's Report"
            elif search_result["title"] == "사업보고서(일반법인)":
                search_result["title"] = "Business Report"
        #    else:
        #        break
        
            print(search_result)
    except:
        print("Error occurred while getting search result")

@click.group()
def cli():
    pass

cli.add_command(search)

if __name__ == '__main__':
    cli()
