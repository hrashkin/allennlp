#!/usr/bin/env python3
from IPython import embed
import sys, os
import json
import argparse
p = argparse.ArgumentParser()
p.add_argument("-i","--input_file",help="File used as input for `allennlp predict`")
p.add_argument("-p","--pred_file",help="File generated by `allennlp predict`")
p.add_argument("-o","--output_file",help="File you want your output to")
args = p.parse_args()

dims = ["oEffect", "oReact", "oWant", "xAttr", "xEffect", "xIntent", "xNeed", "xReact", "xWant"]

if not args.input_file or not args.pred_file or not args.output_file:
  print("Missing some arguments",file=sys.stderr)
  p.print_help()
  sys.exit(1)

# print(args)
events = [json.loads(l)["source"] for l in open(args.input_file)]
pred_dict = {}

with open(args.pred_file) as inf:
  for e,l in zip(events,inf):
    l = json.loads(l)
    out = {}
    for d in dims:
      if d+"_top_k_predicted_tokens" in l:
        out[d] = [(" ".join(ts),p) for ts, p in zip(l[d+"_top_k_predicted_tokens"],l[d+"_top_k_log_probabilities"])]
      elif d.lower()+"_top_k_predicted_tokens" in l:
        d = d.lower()
        out[d] = [(" ".join(ts),p) for ts, p in zip(l[d+"_top_k_predicted_tokens"],l[d+"_top_k_log_probabilities"])]
      # embed();exit()
    pred_dict[e] = out

with open(args.output_file,"w+") as outf:
  json.dump(pred_dict,outf,indent=2)


for e, d in pred_dict.items():
  print("#"*40)
  print("Event:",e)
  for dim, gens in d.items():
    print("===  "+dim)
    for g, p in gens:
      print('"{}" (log p = {:.4f})'.format(g,p))