from odoo import api,fields, models
from datetime import date
from odoo.exceptions import UserError

class partner(models.Model):
    _inherit="res.partner"

    demo_ids=fields.Many2one("res.partner")
    gen = fields.Selection([("m", "Male"), ("f", "Female")], "Gender")


   

class Demo(models.Model):
    _name = "examkt"  # Table name
    _description = "Demo Description"
    _rec_name = "clname"

    clname = fields.Char("Write Name:", required=True)
    dob = fields.Date("Date of Birth:"  )
    gen = fields.Selection([("m", "Male"), ("f", "Female")], "Gender")
    # Dynamically filtered customers based on selected gender
    filtered_customers = fields.Many2many("examkt", string="Filtered Customers", compute="_compute_filtered_customers")
    age = fields.Integer("Age" ,compute="com_age" ,tracking=True)
    salary = fields.Float(string="Salary")
    is_active = fields.Boolean(string="Is Active", default=True)
    desc=fields.Text("Description")
    count_partner = fields.Integer(compute='com_sum_meeting')

    company_id = fields.Many2one("res.partner", string="Company")
    task_ids = fields.One2many("project.task", "demo_id", string="Tasks")
    #"demo_id": The field in the Child model (project.task) that refers back to the current model. This field establishes the reverse relationship
    partner_ids = fields.Many2many("res.partner", string="Partners")

    # ONE TASK WHICH ONE FIELDS IS MANY2ONE IN RES.PARTNER AND SHOW ITS ALL CHIlD CUSTOMER 
    parent_id=fields.Many2one("res.partner",string="Parent Name")
    sub_child = fields.Many2one('res.partner', domain="[('gen', '=', gen)]")
    # child_name_uni=fields.One2many("res.partner","demo_ids")    
    # @api.onchange('parent_id')
    # def _onchange_assigned_to(self):
    #     domain=[('parent_id','in',self.parent_id.ids)]
    #     partners = self.env['res.partner'].search(domain)
    #     print("domain====>",partners)
    #     self.sub_child=partner

    # Dynamically filtered customers based on selected gender
    @api.depends('gen')
    def _compute_filtered_customers(self):
        for record in self:
            if record.gen:
                record.filtered_customers = self.env['examkt'].search([('gen', '=', record.gen)])

            else:
                record.filtered_customers = self.env['examkt'].search([])

    # to create customer and show contants in add customer threw save ..
    def add_cust(self):
        print("=====herer=>",self.parent_id.name)

        # TO CREATE NEW CUSTOMER IN RES.PARTNER ......
        # field_value = self.clname  
        # new_partner_data = [{'name': field_value}]
        # self.env['res.partner'].create(new_partner_data)
        # print(f"Button is pressed. Created partner with name: {field_value}")
        # return True

    

    # to compute count partner  
    def com_sum_meeting(self):
        for record in self:
            if record.clname:
                domain = [('name', '=', record.clname)]
                partners = self.env['res.partner'].search(domain)
                re=partners.read()
                print("read op ===>",re)
                so=partners.sorted(key= lambda l :l.name)
                print('sorted=====>',so)
                print(f"Matching partners for with exists method  {record.clname}: {partners}")
                record.count_partner = len(partners)
            else:
                record.count_partner = 0


    # to show customer in tree in form view.
    def action_show_partners(self):
        """Action to show partners matching the name."""
        self.ensure_one()  # Ensure the action is performed for one record at a time
        domain = [('name', '=', self.clname)]
        return {
            'type': 'ir.actions.act_window',
            'name': 'Matching Customers',
            'view_mode': 'tree,form',
            'res_model': 'res.partner',
            'domain': domain,
        }
    
    # to compute count age thre year ..  
    def com_age(self):
        today=date.today()
        for rec in self:
            if rec.dob:
                rec.age = today.year-rec.dob.year
            else:
                rec.age=0
    
    def check_pop(self):
        print("==============check_pop======",self.ids)
        domain = [('id', '=', self.ids)]
        return {
        'type': 'ir.actions.act_window',
        'name': 'Check Pop',
        'res_model':'examkt',
        'view_mode': 'tree',
        'domain':domain,
        'target': 'new',
        }

    

# this show for task perpose ....
class ProjectTask(models.Model):
    _name = "project.task"  # Table name for Task
    _description = "Project Task"

  
    name = fields.Char("Task Name", required=True)
    description = fields.Text("Task Description")
    demo_id = fields.Many2one("examkt", string="Related Demo")  
    assigned_to = fields.One2many("examkt",'parent_id',string="child") 
    display_name = fields.Many2one("res.partner",domain="[('id', 'child_of', parent.parent_id),('id', '!=', parent.parent_id)]", 
    string="Child Partner")


 

   











































#     i am fresher and i am doing job in odoo company i am working in odoo17 you 
# how can i understand odoo17 source code and for my work i understand odoo code  you are sernior treat me what can understand frist or not make a 30 day full plan to understand odoo importment source code which is need to fresher know give youtub chanle and website for complete topices  
  # sub_child = fields.Many2one('res.partner', 
                               # domain="[('parent_id', '=', parent_id)]" if parent_id else [])