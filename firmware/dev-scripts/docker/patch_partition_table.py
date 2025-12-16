import re, sys
from pathlib import Path

sdk_path = Path(sys.argv[1])
csv_name = "custom_partition_table.csv"

s = sdk_path.read_text()

def set_kv(text, key, value):
    # Replace KEY=... if present, else append
    if re.search(rf"^{re.escape(key)}=", text, flags=re.M):
        return re.sub(rf"^{re.escape(key)}=.*$", f"{key}={value}", text, flags=re.M)
    return text.rstrip() + f"\n{key}={value}\n"

s = set_kv(s, "CONFIG_PARTITION_TABLE_CUSTOM", "y")
s = set_kv(s, "CONFIG_PARTITION_TABLE_CUSTOM_FILENAME", f"\"{csv_name}\"")

if not s.endswith("\n"):
    s += "\n"

sdk_path.write_text(s)
print(f"Patched {sdk_path} -> CONFIG_PARTITION_TABLE_CUSTOM=y, CONFIG_PARTITION_TABLE_CUSTOM_FILENAME=\"{csv_name}\"")