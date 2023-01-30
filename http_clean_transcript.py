import re
import docx
from azure.functions import HttpResponse

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

def main(request):
    request_body = request.get_json()
    transcript = request_body['transcript']

    # Clean the transcript
    cleaned_transcript = clean_subtitle_transcript(transcript)
    
    # Create a Word document
    document = docx.Document()
    
    # Add the cleaned transcript to the document
    document.add_paragraph(cleaned_transcript)
    
    # Save the Word document
    output_file = io.BytesIO()
    document.save(output_file)
    output_file.seek(0)
    
    return HttpResponse(output_file, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
