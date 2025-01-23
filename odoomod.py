from odoo import api,models, fields

class SaleOrderCustom(models.Model):
    _inherit = 'sale.order'

           

class AccountMoveCustom(models.Model):
    _inherit = 'account.move'

class StockPickingCustom(models.Model):
    _inherit = 'stock.picking'
  
    
class SaleOrderLineCustom(models.Model):
    _inherit = 'sale.order.line'

    new_brands = fields.Char(string="Brand Name")

    def _prepare_invoice_line(self, **optional_values):
        val=super(SaleOrderLineCustom,self)._prepare_invoice_line()
        print("val=====_prepare_invoice_line========",val)
        val['new_brand']=self.new_brands
        return val
    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLineCustom, self)._prepare_procurement_values(group_id)
        sale_line = values.get('sale_line_id')
        print(self,"=============self",sale_line)
        # values['new_brand']=self.new_brands
        values.update({
            'new_brand': self.new_brands,  
        })
        # import pdb;pdb.set_trace()

        print("val=====_prepare_procurement_values=====333===",values)
        return values
  
class AccountMoveLineCustom(models.Model):
    _inherit = 'account.move.line'

    new_brand = fields.Char(string="Brand Name")
    
class StockMoveCustom(models.Model):
    _inherit='stock.move'

    new_brand = fields.Char(string="Brand Name")

    @api.model
    def create(self,val):
        da=super(StockMoveCustom,self).create(val)
        brand_name = self.env['sale.order.line'].browse(val.get('sale_line_id')).new_brands
        da.new_brand = brand_name
        print(self,"=====StockMoveCustom========self",da.new_brand)
        return da

class crmleadcustom(models.Model):
    _inherit='crm.lead'

    new_brand = fields.Char(string="Brand Name")
