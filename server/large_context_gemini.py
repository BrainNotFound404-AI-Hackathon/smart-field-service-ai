from google import genai
from google.genai import types
import pathlib
import httpx

client = genai.Client(api_key = "AIzaSyBSFs4_X_-T3Ry49JeMMbBs6-LozKGNAIo")

# long_context_pdf_path = "https://data2.manualslib.com/pdf7/200/19926/1992541-kone/mx10.pdf"

# Retrieve the PDF
file_path = pathlib.Path('mannual.pdf')
# file_path.write_bytes(httpx.get(long_context_pdf_path).content)

# Upload the PDF using the File API
sample_file = client.files.upload(
  file=file_path,
)

prompt="Summarize this document"

response = client.models.generate_content(
  model="gemini-2.0-flash",
  contents=[sample_file, "Summarize this document, what is in the section 3?"])
print(response.text)
