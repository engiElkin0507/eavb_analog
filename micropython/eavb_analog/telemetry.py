def pack_telemetry(**kwargs) -> str:
    """Packs analog data into a fast CSV string like >V1:4.2,V2:1.1"""
    payload = ",".join([f"{k}:{v}" for k, v in kwargs.items()])
    return f">{payload}\n"
