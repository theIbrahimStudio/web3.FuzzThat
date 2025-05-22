def get_state(contract):
    """Returns a dict of public variable names → values"""
    state = {}
    for item in contract.abi:
        if (
            item.get("type") == "function"
            and item.get("inputs") == []
            and item.get("stateMutability") == "view"
        ):
            try:
                val = getattr(contract.functions, item["name"])().call()
                state[item["name"]] = val
            except Exception:
                continue
    return state


def compare_state(pre, post):
    """Returns dict of changed fields and their deltas or new values"""
    changes = {}
    for k in post:
        if k not in pre:
            changes[k] = {"new": post[k]}
        elif pre[k] != post[k]:
            try:
                delta = post[k] - pre[k]
                changes[k] = {"from": pre[k], "to": post[k], "delta": delta}
            except Exception:
                changes[k] = {"from": pre[k], "to": post[k]}
    return changes
