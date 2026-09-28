import json,sys,glob
for d in sys.argv[1:]:
    rows=[]
    for f in glob.glob(d+"/telemetry-*.jsonl"):
        for l in open(f):
            r=json.loads(l)
            if not r["incoming_path"].endswith("chat/completions"): continue
            rows.append(r)
    if not rows: print(d,"no calls yet"); continue
    r0=rows[-1]["request"]
    print(d, "calls",len(rows), "status",sorted({r["status_code"] for r in rows}),
          "| eff",r0.get("reasoning_effort"),r0.get("chat_template_kwargs"),"T",r0.get("temperature"),"topk",r0.get("top_k"),"minp",r0.get("min_p"),"max",r0.get("max_tokens"),"stream",r0.get("stream"),"prov",r0.get("provider",{}).get("order"))
    ct=[];pt=[];dur=[];cost=0
    for r in rows:
        s=r.get("response_summary") or {}; u=s.get("usage") or (r.get("response") or {}).get("usage") if isinstance(r.get("response"),dict) else s.get("usage")
        if u: ct.append(u.get("completion_tokens",0)); pt.append(u.get("prompt_tokens",0)); cost+=u.get("cost",0) or 0
        dur.append(r.get("duration_seconds") or 0)
    if ct: print("   completion/call %.0f  prompt/call %.0f  max prompt %d  sec/call %.0f  cost $%.3f"%(sum(ct)/len(ct),sum(pt)/len(pt),max(pt),sum(dur)/len(dur),cost))
    else: print("   no usage parsed; keys:", list((rows[-1].get("response_summary") or {}).keys()))
