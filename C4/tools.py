import json
import re
from jsonschema import validate, ValidationError
from model_client import ROOT
from agent import record_customer_interest, record_feedback

CATALOG = {
    'diagnostic': {'price_usd':15, 'description':'Workshop diagnostic assessment; fee credited against approved repair labour.'},
    'cleaning': {'price_usd':25, 'description':'Internal cleaning; assessment required; no guaranteed cure for overheating.'},
    'os_setup': {'price_usd':30, 'description':'Operating-system setup; customer provides a valid licence.'},
    'ssd_installation': {'price_usd':20, 'description':'SSD installation labour only; SSD and data migration excluded.'},
    'battery_replacement': {'price_usd':20, 'description':'Battery replacement labour only; replacement battery excluded.'}
}
TRIAGE = {
 'battery_swelling': {'urgency':'urgent','guidance':'Stop using and charging the device if safe. Do not open, press, puncture, or heat the battery. Seek professional assessment. If smoke or fire is present, move away and contact local emergency services.','diagnosis':'Not a remote diagnosis.'},
 'liquid_exposure': {'urgency':'urgent','guidance':'Stop using and charging the device if safe; disconnect external power only if safe. Do not power it on to test it. Seek professional assessment. No liquid-damage price is published.','diagnosis':'Damage cannot be assessed remotely.'},
 'overheating': {'urgency':'assessment','guidance':'Shut down if dangerously hot. Let the device cool on a hard, ventilated surface and seek assessment if the issue persists. Cleaning may help only after inspection.','diagnosis':'Do not assume dust is the cause.'},
 'slow_device': {'urgency':'routine','guidance':'Back up important data. Check storage space and startup apps; a workshop assessment is needed before recommending hardware.','diagnosis':'Many hardware and software causes are possible.'},
 'other': {'urgency':'assessment','guidance':'Ask for device model, symptoms, and when the issue started; recommend workshop assessment.','diagnosis':'No remote final diagnosis.'}
}

def get_service(service):
    """Look up a published service by ID. Return found, price_usd, and limitations."""
    item = CATALOG.get(service)
    return {'found':bool(item),'service':service,**(item or {}),'available_service_ids':list(CATALOG), 'limitations':'Illustrative labour prices. Parts excluded. No booking, inventory, or turnaround guarantee.'}

def triage_device(symptom):
    """Return conservative first steps for one listed symptom category, not a diagnosis."""
    return {'symptom':symptom, **TRIAGE.get(symptom, TRIAGE['other'])}

def estimate_repair(services):
    """Calculate listed labour, applying the diagnostic credit once; never quote parts."""
    if not services or any(s not in CATALOG for s in services) or len(set(services)) != len(services):
        return {'status':'error','message':'Use one or more unique published service IDs.'}
    subtotal = sum(CATALOG[s]['price_usd'] for s in services)
    credit = 15 if 'diagnostic' in services and len(services)>1 else 0
    return {'status':'ok','services':services,'subtotal_usd':subtotal,'diagnostic_credit_usd':credit,'estimated_labour_usd':subtotal-credit,'parts_included':False,'notice':'Illustrative labour estimate, subject to assessment and customer approval. Parts and licences excluded.'}

def record_interest(name,email,issue,consent,log_dir=ROOT/'runtime_logs'):
    """Add explicit consent validation, then reuse the original C3 lead-saving tool."""
    if consent is not True or not name.strip() or not issue.strip() or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email):
        return {'status':'error','message':'Explicit consent, name, valid email, and issue are required.'}
    return record_customer_interest(email=email, name=name, message=issue, log_dir=log_dir)

def log_unanswered(question,log_dir=ROOT/'runtime_logs'):
    """Reuse C3 feedback logging for a complaint, suggestion, or unpublished question."""
    if not question.strip():
        return {'status':'error','message':'Question cannot be empty.'}
    return record_feedback(question=question, log_dir=log_dir)

def schema(name, description, properties, required):
    return {'name':name,'description':description,'parameters':{'type':'object','properties':properties,'required':required,'additionalProperties':False}}

TOOL_SCHEMAS = [
 schema('get_service','Look up a published service and its price.',{'service':{'type':'string','enum':list(CATALOG)}},['service']),
 schema('triage_device','Get safe first steps; use for symptom or hazard questions.',{'symptom':{'type':'string','enum':list(TRIAGE)}},['symptom']),
 schema('estimate_repair','Compute combined labour and diagnostic credit; parts excluded.',{'services':{'type':'array','items':{'type':'string','enum':list(CATALOG)},'minItems':1,'uniqueItems':True}},['services']),
 schema('record_interest','Save follow-up only when customer gives contact details and consent.',{'name':{'type':'string'},'email':{'type':'string'},'issue':{'type':'string'},'consent':{'type':'boolean'}},['name','email','issue','consent']),
 schema('log_unanswered','Record feedback or a question whose answer is unpublished.',{'question':{'type':'string'}},['question'])
]

class ToolRegistry:
    def __init__(self, log_dir=ROOT/'runtime_logs'):
        self.log_dir=log_dir

    def execute(self,name,arguments):
        functions={'get_service':get_service,'triage_device':triage_device,'estimate_repair':estimate_repair,'record_interest':record_interest,'log_unanswered':log_unanswered}
        schemas={t['name']:t['parameters'] for t in TOOL_SCHEMAS}
        try:
            if name not in functions:
                raise ValueError('Unknown tool')
            validate(arguments,schemas[name])
            kwargs={'log_dir':self.log_dir} if name in {'record_interest','log_unanswered'} else {}
            return functions[name](**arguments,**kwargs)
        except (ValueError,TypeError,ValidationError):
            return {'status':'error','message':'Unknown tool or invalid arguments; use a listed schema.'}
