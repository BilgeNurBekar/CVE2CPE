from pydantic import ValidationError
from cpeParser import CPEParser
# Test JSON verisi
json_data = {
    "cpe": [
        "cpe:2.3:a:grpc:grpc:1.58.3:*:*:*:*:*:*:*",
        "cpe:2.3:a:grpc:grpc:1.59.5:*:*:*:*:*:*:*",
        "cpe:2.3:a:grpc:grpc:1.60.2:*:*:*:*:*:*:*",
        "cpe:2.3:a:grpc:grpc:1.61.3:*:*:*:*:*:*:*",
        "cpe:2.3:a:grpc:grpc:1.62.3:*:*:*:*:*:*:*",
        "cpe:2.3:a:grpc:grpc:1.63.2:*:*:*:*:*:*:*",
        "cpe:2.3:a:grpc:grpc:1.64.3:*:*:*:*:*:*:*",
        "cpe:2.3:a:grpc:grpc:1.65.4:*:*:*:*:*:*:*"
    ]
}

# Model ile doğrulama
try:
    cpe_parser = CPEParser(**json_data)
    print(f"basarili:{cpe_parser}")
except ValidationError as e:
    print(e)
