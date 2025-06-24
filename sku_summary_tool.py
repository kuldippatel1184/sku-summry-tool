import pandas as pd
import re
from collections import defaultdict
from PyPDF2 import PdfReader

# === CONFIGURATION ===
pdf_path = "sample.pdf"  # 🔁 Replace this with your PDF file path
output_csv_path = "SKU_Summary.csv"

# === PROCESSING ===
reader = PdfReader(pdf_path)
full_text = ""
for page in reader.pages:
    full_text += page.extract_text()

# Extract SKU and Quantity (based on "Free Size" line pattern)
sku_pattern = re.compile(r"\b([a-zA-Z0-9\-]+)\b\s+Free\s+Size\s+(\d+)", re.IGNORECASE)
sku_counts = defaultdict(lambda: {"Total Orders": 0, "Total Quantity": 0})

for match in sku_pattern.finditer(full_text):
    sku = match.group(1).strip()
    qty = int(match.group(2))
    sku_counts[sku]["Total Orders"] += 1
    sku_counts[sku]["Total Quantity"] += qty

# === OUTPUT ===
if sku_counts:
    df = pd.DataFrame([
        {"SKU": sku, "Total Orders": data["Total Orders"], "Total Quantity": data["Total Quantity"]}
        for sku, data in sku_counts.items()
    ])
    print("\n📦 SKU-wise Order Summary:\n")
    print(df.to_string(index=False))
    df.to_csv(output_csv_path, index=False)
    print(f"\n✅ Summary saved to: {output_csv_path}")
else:
    print("\n⚠️ No SKU data found in the PDF.")
