#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json

latest_by_txn_id = {}

with open("payments.jsonl") as f:
    for line in f:
        try:
            event = json.loads(line)
            if "txn_id" not in event:
                continue
            
            timestamp = event['ts']
            txn_id = event['txn_id']

            if txn_id not in latest_by_txn_id or timestamp > latest_by_txn_id[txn_id][0]:
                latest_by_txn_id[txn_id] = (timestamp, event)
        
        except json.JSONDecodeError:
            pass

successful = [event for _, event in latest_by_txn_id.values() if event["status"] == "success"]
count = len(successful)
total = sum(float(event["amount"].replace(",", "") if isinstance(event["amount"], str) else event["amount"]) for event in successful)

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
