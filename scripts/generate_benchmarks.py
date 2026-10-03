"""Deterministic program generation; oracle ground truth is computed separately."""
import json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SEED=20261003
def write(group,name,variables,**kw):
 p=ROOT/'benchmarks'/group/(name+'.json');p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(dict(name=name,group=group,variables=variables,**kw),indent=2),encoding='utf-8')
def v(lo=-3,hi=6): return dict(type='Money',min=lo,max=hi,quantum='1')
def main():
 rng=random.Random(SEED)
 for i in range(8):
  r=rng.choice([2,4,5,10]);vs={'x':v(),'y':v()}
  write('synthetic',f'safe_{i:02}',vs,pattern='insensitive',batch=dict(lines=[f'{r}*x',f'{r}*y'],mode='HALF_EVEN'))
 for i in range(10):
  r=rng.choice([2,4,5,10]); mode=rng.choice(['HALF_EVEN','FLOOR','CEILING'])
  write('synthetic',f'stage_{i:02}',{'x':v(),'y':v()},pattern='stage',batch=dict(lines=[f'x/{r}',f'y/{r}'],mode=mode))
 for i in range(10):
  r=rng.choice([2,4,5,10]);m1,m2=rng.sample(['HALF_UP','HALF_EVEN','FLOOR','CEILING','DOWN','UP'],2)
  write('synthetic',f'mode_{i:02}',{'x':v(-12,12)},pattern='mode',variants={'a':f'Q(x/{r},1,"{m1}")','b':f'Q(x/{r},1,"{m2}")'})
 for i in range(10):
  r=rng.choice([2,4,5]);c=rng.choice([-1,0,1]);
  write('synthetic',f'threshold_{i:02}',{'x':v(-10,10)},pattern='threshold',variants={'a':f'100 if Q(x/{r},1,"HALF_EVEN") >= {c} else 0','b':f'100 if x/{r} >= {c} else 0'})
 for i in range(10):
  vs={'x':v(),'y':v(),'z':v()}; q=rng.choice([2,5])
  write('synthetic',f'tree_{i:02}',vs,pattern='aggregation',variants={'left':f'Q(Q(x+y,{q},"HALF_EVEN")+z,{q},"HALF_EVEN")','right':f'Q(x+Q(y+z,{q},"HALF_EVEN"),{q},"HALF_EVEN")'})
 cases=[
 ('tax_per_line',{'x':v(0,19),'y':v(0,19)},dict(batch=dict(lines=['x/5','y/5'],mode='HALF_EVEN'))),
 ('allocation',{'x':v(0,60)},dict(variants={'parts':'Q(x*rate("0.4"),1,"HALF_EVEN")+Q(x*rate("0.6"),1,"HALF_EVEN")','whole':'x'})),
 ('payroll_deduction',{'x':v(0,99)},dict(variants={'twice':'Q(Q(x*rate("0.062"),1,"HALF_UP")+Q(x*rate("0.0145"),1,"HALF_UP"),1,"HALF_UP")','combined':'Q(x*rate("0.0765"),1,"HALF_UP")'})),
 ('percentage_discount',{'x':v(0,39)},dict(variants={'stage':'Q(Q(x*rate("0.9"),1,"HALF_EVEN")*rate("0.8"),1,"HALF_EVEN")','end':'Q(x*rate("0.72"),1,"HALF_EVEN")'})),
 ('vat',{'x':v(0,29),'y':v(0,29)},dict(batch=dict(lines=['x/5','y/20'],mode='FLOOR'))),
 ('currency_conversion',{'x':v(0,99)},dict(variants={'stage':'Q(Q(x*rate("1.2345"),"0.1","HALF_UP"),1,"HALF_UP")','end':'Q(x*rate("1.2345"),1,"HALF_UP")'})),
 ('threshold_rule',{'x':v(490,510)},dict(variants={'before':'100 if Q(x/10,1,"HALF_EVEN") >= 50 else 0','after':'100 if x/10 >= 50 else 0'})),
 ('capped_contribution',{'x':v(180,220)},dict(variants={'stage':'min(Q(x*rate("0.125"),1,"HALF_EVEN"),25)','end':'Q(min(x*rate("0.125"),25),1,"HALF_EVEN")'})),
 ('benefit_calculation',{'x':v(100,139)},dict(variants={'before':'Q(Q(x*rate("0.73"),10,"FLOOR")-3,100,"FLOOR")','after':'Q(x*rate("0.73")-3,100,"FLOOR")'})),
 ('settlement',{'x':v(0,29),'y':v(0,29)},dict(batch=dict(lines=['x','y'],mode='HALF_EVEN',quantum='5'))),
 ('homogeneous_tree',{'x':v(),'y':v(),'z':v()},dict(variants={'a':'Q(Q(x+y,1,"HALF_EVEN")+z,1,"HALF_EVEN")','b':'Q(x+Q(y+z,1,"HALF_EVEN"),1,"HALF_EVEN")'})),
 ('placements',{'x':v(0,15),'y':v(0,15)},dict(template='Q(maybe(x/5,1,"HALF_EVEN","a")+maybe(y/5,1,"HALF_EVEN","b"),1,"HALF_EVEN")')),
 ]
 for name,vs,kw in cases: write('canonical',name,vs,pattern=name,**kw)
 # These are small independently reimplemented rule fragments, not full legal
 # calculators or confirmed defects in any deployed application.
 real=[
 ('hmrc_invoice',{'x':v(10000,10039),'y':v(5000,5039)},'https://www.gov.uk/guidance/vat-guide-notice-700','17.5 / 17.5.1',dict(variants={'line_tenth_then_penny':'Q(Q(x/5,"0.1","FLOOR")+Q(y/5,"0.1","FLOOR"),1,"FLOOR")','total_penny':'Q((x+y)/5,1,"FLOOR")'})),
 ('irs_payroll',{'x':v(100000,100199)},'https://www.irs.gov/publications/p15','Fractions-of-cents adjustment',dict(variants={'separate_taxes':'Q(x*rate("0.062"),1,"HALF_UP")+Q(x*rate("0.0145"),1,"HALF_UP")','counterfactual_combined':'Q(x*rate("0.0765"),1,"HALF_UP")'})),
 ('ssa_benefit',{'x':v(100000,100199)},'https://secure.ssa.gov/POMS.NSF/LNX/0300601020','A.2, D.2',dict(variants={'dime_then_offset_then_dollar':'Q(Q(x*rate("1.025"),10,"FLOOR")-1234,100,"FLOOR")','counterfactual_dollar_early':'Q(x*rate("1.025"),100,"FLOOR")-1234'})),
 ('cash_settlement',{'x':v(2000,2039),'y':v(1000,1039)},'https://www.canada.ca/en/revenue-agency/programs/about-canada-revenue-agency-cra/federal-government-budgets/archived-budget-2012/archived-eliminating-penny-canada-s-coinage-system.html','Final bill after taxes',dict(batch=dict(lines=['x','y'],mode='HALF_EVEN',quantum='5'))),
 ('rational_money',{'x':v(1000,1199)},'https://github.com/brick/money','RationalMoney intermediate rounding example; independent parametrization',dict(variants={'intermediate':'Q(Q(x*rate("1.21"),1,"HALF_UP")*rate("0.9"),1,"HALF_UP")','deferred':'Q(x*rate("1.089"),1,"HALF_UP")'})),
 ('ssa_entitlement',{'x':v(990,1010)},'https://secure.ssa.gov/POMS.NSF/LNX/0300601020','D: compare before lower-dollar provision',dict(variants={'compare_before':'50 if x >= 999 else 0','counterfactual_compare_after':'50 if Q(x,100,"FLOOR") >= 999 else 0'})),
 ]
 for name,vs,url,section,kw in real: write('realistic',name,vs,source=url,source_section=section,scope='Illustrative rounding fragment; comparison policy may be deliberately counterfactual; no production defect claim.',**kw)
 for n in [2,4,8,16,32,64]:
  for magnitude in [3,20,10000,1000000000]:
   vs={f'x{i}':v(0,magnitude) for i in range(n)}
   write('scaling',f'batch_n{n}_u{magnitude}',vs,pattern='heterogeneous independent invoice',batch=dict(lines=[f'x{i}/{[2,4,5,10][i%4]}' for i in range(n)],mode='HALF_EVEN'))
 (ROOT/'benchmarks'/'MANIFEST.md').write_text('# Benchmark provenance\n\nSeed: 20261003. 48 synthetic, 12 canonical, 6 rule-derived fragments, 24 scaling cases. Synthetic labels are computed by the independent exhaustive Decimal oracle, not inferred from generator names. Cases include negative inputs, half ties, homogeneous exact aggregation, threshold and cap behavior. Realistic fragments are authored from public rule descriptions and compare explicit alternatives; no copied external code or production-bug claim. Monetary output units are cents unless case quantum states otherwise. All scaling ground truths use independent local Decimal error envelopes, integrality of the final discrepancy, explicit in-box witness checks, and independent Decimal replay of an attaining assignment. The universal nearest-even aggregation bound is reported separately and is not necessarily attainable. The Decimal oracle shares the parsed AST but not the concrete Fraction or symbolic operator implementation.\n',encoding='utf-8')
if __name__=='__main__': main()

