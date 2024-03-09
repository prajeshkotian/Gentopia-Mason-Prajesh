from typing import AnyStr
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import PyPDF2
from gentopia.tools.basetool import *

class ReadPdfArgs(BaseModel):
    url: str = Field(..., description="a web URL to visit. You must make sure that the URL is real and correct.")

class ReadPDF(BaseTool):
    """Tool that adds the capability to read PDFs from a web URL."""

    name = "read_pdf_from_url"
    description = "A tool to retrieve PDF content from a web URL."

    args_schema: Optional[Type[BaseModel]] = ReadPdfArgs

    def _run(self, url: AnyStr) -> str:
        try:
            response = requests.get(url)
            print(response)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Create a file-like object from the content of the response
                pdf_content = BytesIO(response.content)

                # Use PyPDF2 to read the PDF
                pdf_reader = PyPDF2.PdfReader(pdf_content)

                # Extract text from each page
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()

                return text
            else:
                return f"Failed to retrieve PDF from URL. Status code: {response.status_code}"
        except Exception as e:
            return f"Error: {e}\nProbably, it is an invalid URL."

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    ans = ReadPDF()._run("https://example.com/example.pdf")
    print(ans)
