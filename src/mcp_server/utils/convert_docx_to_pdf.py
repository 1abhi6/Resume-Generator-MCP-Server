import os
import time
import logging
import requests
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def docx_to_pdf(docx_bytes: bytes, input_format: str = "docx") -> BytesIO:
    """
    Convert Word document to PDF using CloudConvert API.

    Args:
        docx_bytes: File content as bytes
        input_format: 'doc' or 'docx' (default: 'docx')

    Free tier: 25 conversions/day
    Sign up at: https://cloudconvert.com/register
    """
    api_key = os.getenv("CLOUDCONVERT_API_KEY")

    if not api_key:
        raise ValueError(
            "CLOUDCONVERT_API_KEY not found in environment variables. "
            "Get your key at: https://cloudconvert.com/register"
        )

    base_url = "https://api.cloudconvert.com/v2"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        # Step 1: Create job
        logger.info("Creating conversion job...")
        job_response = requests.post(
            f"{base_url}/jobs",
            headers=headers,
            json={
                "tasks": {
                    "upload-task": {"operation": "import/upload"},
                    "convert-task": {
                        "operation": "convert",
                        "input": "upload-task",
                        "input_format": input_format,
                        "output_format": "pdf",
                    },
                    "export-task": {"operation": "export/url", "input": "convert-task"},
                }
            },
            timeout=30,
        )
        job_response.raise_for_status()
        job_data = job_response.json()

        logger.info(f"Job created: {job_data['data']['id']}")

        # Step 2: Upload file
        logger.info("Uploading file...")
        upload_task = next(
            t for t in job_data["data"]["tasks"] if t["operation"] == "import/upload"
        )

        upload_url = upload_task["result"]["form"]["url"]
        upload_params = upload_task["result"]["form"]["parameters"]

        # Upload with proper filename including extension
        filename = f"document.{input_format}"
        upload_response = requests.post(
            upload_url,
            data=upload_params,
            files={"file": (filename, docx_bytes)},
            timeout=60,
        )
        upload_response.raise_for_status()
        logger.info("File uploaded successfully")

        # Step 3: Poll for completion
        logger.info("Converting to PDF...")
        job_id = job_data["data"]["id"]
        max_attempts = 60

        for attempt in range(max_attempts):
            time.sleep(2)

            status_response = requests.get(
                f"{base_url}/jobs/{job_id}", headers=headers, timeout=30
            )
            status_response.raise_for_status()
            status_data = status_response.json()

            job_status = status_data["data"]["status"]
            logger.info(f"Status: {job_status}")

            if job_status == "finished":
                # Step 4: Download PDF
                export_task = next(
                    t
                    for t in status_data["data"]["tasks"]
                    if t["operation"] == "export/url"
                )

                pdf_url = export_task["result"]["files"][0]["url"]
                logger.info("Downloading PDF...")

                pdf_response = requests.get(pdf_url, timeout=60)
                pdf_response.raise_for_status()

                logger.info("✓ Conversion successful!")
                return BytesIO(pdf_response.content)

            elif job_status == "error":
                # Log full response for debugging
                logger.error(f"Full error response: {status_data}")

                # Get detailed error information from all tasks
                for task in status_data["data"]["tasks"]:
                    logger.error(
                        f"Task {task['name']}: {task.get('status')} - {task.get('message', 'No message')}"
                    )

                error_tasks = [
                    t
                    for t in status_data["data"]["tasks"]
                    if t.get("status") == "error"
                ]

                if error_tasks:
                    error_details = error_tasks[0].get("message", "Unknown error")
                    error_code = error_tasks[0].get("code", "")
                    raise Exception(
                        f"Conversion failed: {error_details} (Code: {error_code})"
                    )
                else:
                    raise Exception("Conversion failed with unknown error")

        raise TimeoutError("Conversion timed out after 2 minutes")

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise Exception(f"CloudConvert API error: {str(e)}")

