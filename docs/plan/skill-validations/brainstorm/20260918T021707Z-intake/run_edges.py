from run_campaign import *
if __name__=='__main__':
    identifiers=json.loads((RUN/'inputs/edge-trial-list.json').read_bytes())
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures=[pool.submit(execute,ident) for ident in identifiers]
        for future in as_completed(futures):
            print(json.dumps(future.result()),flush=True)
