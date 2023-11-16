import pandas as pd
from rich import print

from edgar import Filing
from edgar import find
from edgar.company_reports import TenK, TenQ, TwentyF, EightK, is_valid_item_for_filing
from edgar.htmltools import ChunkedDocument

pd.options.display.max_colwidth = 40


def test_tenk_filing_with_no_gaap():
    # This filing has no GAAP data
    filing = Filing(form='10-K', filing_date='2023-04-06', company='Frontier Masters Fund', cik=1450722,
                    accession_no='0001213900-23-028058')
    tenk: TenK = filing.obj()
    assert tenk
    assert tenk.financials is not None

def test_tenk_item_and_parts():
    filing = Filing(form='10-K', filing_date='2023-04-06', company='Frontier Masters Fund', cik=1450722,
                    accession_no='0001213900-23-028058')
    tenk: TenK = filing.obj()
    # Get item 1
    item1 = tenk['Item 1']
    assert 'Item 1.' in item1

    # Case in
    item3 = tenk['Item 3']
    assert 'There are no material legal' in item3
    print(item3)
    # Show Item 1
    #tenk.view('Item 1')


def test_tenq_filing():
    filing = Filing(form='10-Q', filing_date='2023-04-06', company='NIKE, Inc.', cik=320187,
                    accession_no='0000320187-23-000013')
    tenq: TenQ = filing.obj()
    assert tenq
    assert tenq.financials is not None
    assert tenq.financials.balance_sheet.asset_dataframe is not None
    print()
    print(tenq)


def test_is_valid_item_for_filing():
    assert is_valid_item_for_filing(TenK.structure, 'Item 1')
    assert is_valid_item_for_filing(TenK.structure, 'Item 9A')
    assert is_valid_item_for_filing(TenK.structure, 'Item 9A', part='Part II')
    assert is_valid_item_for_filing(TenK.structure, 'ITEM 9A', part='Part II')
    assert is_valid_item_for_filing(TenK.structure, 'ITEM 9A', part='PART II')
    assert not is_valid_item_for_filing(TenK.structure, 'Item 9A', part='Part III')

    assert is_valid_item_for_filing(TenQ.structure, 'Item 4')
    assert not is_valid_item_for_filing(TenQ.structure, 'Item 40')
    assert is_valid_item_for_filing(TenQ.structure, 'Item 4', "PART I")
    assert is_valid_item_for_filing(TenQ.structure, 'Item 4', "PART II")

    assert is_valid_item_for_filing(TwentyF.structure, 'ITEM 10')
    assert not is_valid_item_for_filing(TwentyF.structure, 'ITEM 10', "PART IV")


def test_chunk_items_for_company_reports():
    filing = find("0001193125-23-086073")
    html = filing.html()
    chunked_document = ChunkedDocument(html)
    print()
    items = chunked_document.show_items("Item.str.contains('ITEM', case=False)",  "Item")
    assert not items.empty
    print(items)

def test_item_for_10K_filing():
    filing = Filing(form='10-K', filing_date='2023-11-08', company='CHS INC', cik=823277,
                    accession_no='0000823277-23-000053')
    tenk = filing.obj()
    item_2 = tenk['Item 2']
    assert "We own or lease energy" in item_2
    assert "Kaw Pipe Line Company" in item_2
    print(item_2)

    item_7A = tenk['Item 7A']
    print(item_7A)
    assert "Commodity Price Risk" in item_7A

    item_15 = tenk['Item 15']
    assert item_15
    assert 'FINANCIAL STATEMENTS' in item_15
    assert tenk['ITEM 15'] == item_15
    print(item_15)

def test_items__for_8K_filing():
    filing = Filing(form='8-K', filing_date='2023-11-14',
                    company='ALPINE 4 HOLDINGS, INC.',
                    cik=1606698,
                    accession_no='0001628280-23-039016')
    eightk = EightK(filing)
    doc = eightk.doc
    items = doc.list_items()
    assert items == ['Item 2.03', 'Item 9.01']
    print()
    print(doc)
    print(doc.show_items("Text.notnull()", "Item"))

    item_101 = doc['Item 9.01']
    print(item_101)
