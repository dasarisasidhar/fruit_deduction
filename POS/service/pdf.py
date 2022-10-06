import os
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
from datetime import datetime

# choosing English as the document language

os.environ["INVOICE_LANG"] = "en"

class pdf_generator:
    def generate_bill(storeid, userid, bill_number, billed_products):
        client = Client(userid)
        provider = Provider('Nexsmart', bank_account='xxx-xxx-xxx')
        creator = Creator(storeid)
        invoice = Invoice(client, provider, creator)
        for i in billed_products:
            #invoice.add_item(Item(units, prics, description= product_name))
            invoice.add_item(Item(i[1], i[2], description= i[0]))
        invoice.currency = "Rs."
        invoice.number = bill_number
        invoice.datetime = datetime.now()
        print("downloading invoice")
        docu = SimpleInvoice(invoice)
        docu.gen(str(bill_number)+".pdf", generate_qr_code=False)
        return True
