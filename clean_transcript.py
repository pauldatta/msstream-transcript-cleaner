import logging
import re
import docx
from azure.functions import blob_event_hub, BlobEvent

def main(blob_event: BlobEvent):
    # Retrieve the blob data from the event
    blob_data = blob_event.get_blob_data()

    # Clean the transcript
    cleaned_transcript = clean_subtitle_transcript(blob_data)

    # Create a Word document
    document = docx.Document()

    # Add the cleaned transcript to the document
    paragraph = document.add_paragraph(cleaned_transcript)

    # Set the font of the text to Calibri
    paragraph.style.font.name = 'Calibri'

    # Save the Word document to the output container
    output_container = "output"
    output_blob = blob_event.blob_path.replace("input", output_container)
    blob_event.upload_blob_to_container(document.save, output_blob)

def clean_subtitle_transcript(transcript):
    # Remove time codes and other extraneous information
    cleaned_transcript = re.sub(r'\d\d:\d\d:\d\d\.\d\d\d --> \d\d:\d\d:\d\d\.\d\d\d\n', '', transcript)
    
    # Remove strings of the format "38dcf0f7-3aea-42c9-8d21-f417f9b03b52-1"
    cleaned_transcript = re.sub(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}-[0-9]+', '', cleaned_transcript)
    
    # Replace line breaks with a space
    cleaned_transcript = cleaned_transcript.replace('\n', ' ')
    
        # Add a line break after every period
    cleaned_transcript = re.sub(r'\.([^a-zA-Z])', r'.\n\1', cleaned_transcript)
    
    return cleaned_transcript