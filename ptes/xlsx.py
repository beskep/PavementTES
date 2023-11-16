from pathlib import Path
from typing import TYPE_CHECKING

from xlsxwriter import Workbook

from ptes.calculate import CapacityCases

if TYPE_CHECKING:
    from xlsxwriter.worksheet import Worksheet


def write_values(path: str | Path, cases: CapacityCases, *, table=True):
    with Workbook(path) as wb:
        percent = wb.add_format({'num_format': '0.0%'})
        scientific = wb.add_format({'num_format': '0.000E+00'})

        ws: Worksheet = wb.add_worksheet()

        # width
        ws.set_column(first_col=1, last_col=len(cases.COLUMNS), width=15)

        # header
        ws.write(0, 0, '번호')
        for col, name in enumerate(cases.COLUMNS):
            ws.write(0, col + 1, name)

        # value
        args: tuple
        for row, case in enumerate(cases.cases):
            ws.write(row + 1, 0, f'#{row+1}')  # 번호

            for col, key in enumerate(cases.KEYS):
                value = getattr(case, key)

                if key == 'efficiency':
                    args = (value, percent)
                elif 'e' in f'{value:.4g}':
                    args = (value, scientific)
                else:
                    args = (value,)

                ws.write(row + 1, col + 1, *args)

        # table
        if table:
            ws.add_table(
                first_row=0,
                first_col=0,
                last_row=len(cases.cases),
                last_col=len(cases.COLUMNS),
            )


def write_table(path: str | Path, cases: CapacityCases, *, chart=True):
    nrows = len(cases.cases)
    ncols = len(cases.COLUMNS)

    sheet = 'Sheet1'
    columns = [{'header': x} for x in ['번호', *cases.COLUMNS]]
    data = [
        [f'#{idx+1}', *(getattr(case, key) for key in cases.KEYS)]
        for idx, case in enumerate(cases.cases)
    ]

    with Workbook(path) as wb:
        percent = wb.add_format({'num_format': '0.0%'})
        columns = [
            {**d, 'format': percent} if d['header'].startswith('집열 효율') else d
            for d in columns
        ]

        ws: Worksheet = wb.add_worksheet()

        # width
        ws.set_column(first_col=1, last_col=ncols, width=18)

        # table
        ws.add_table(
            first_row=0,
            first_col=0,
            last_row=nrows,
            last_col=ncols,
            options={'data': data, 'columns': columns, 'style': 'Table Style Light 1'},
        )

        # chart
        if chart:
            _chart = wb.add_chart({'type': 'column'})
            # value 형식: [sheetname, first_row, first_col, last_row, last_col]
            _chart.add_series(
                {
                    'category': [sheet, 1, 0, nrows, 0],
                    'values': [sheet, 1, ncols, nrows, ncols],
                }
            )
            _chart.set_legend({'none': True})
            _chart.set_title(
                {
                    'name': cases.COLUMNS[-1],
                    'name_font': {'size': 16},
                }
            )
            ws.insert_chart(row=0, col=ncols + 2, chart=_chart)
