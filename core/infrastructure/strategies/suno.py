import requests
from django.conf import settings
from .base import SongGeneratorStrategy

class SunoSongGeneratorStrategy(SongGeneratorStrategy):
    """
    Real strategy that integrates with SunoApi.org.
    """

    def __init__(self):
        self.api_token = getattr(settings, 'SUNO_API_TOKEN', '')
        self.base_url = "https://api.sunoapi.org/api/v1"

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def generate(self, prompt, genre=None, mood=None, instrumental=False, title=None):
        """
        Calls the Suno Generate Music endpoint with the strict schema found during diagnosis.
        """
        url = f"{self.base_url}/generate"
        
        # Combining genre and mood into tags for the musical style
        style_tags = f"{genre or ''} {mood or ''}".strip()
        
        payload = {
            "prompt": prompt,              # Lyrics/Song content
            "tags": style_tags,            # Musical style
            "title": title or "New Song",
            "instrumental": instrumental,  # Field MUST be 'instrumental', not 'make_instrumental'
            "customMode": True,            # Required for separate prompt and tags
            "model": "V3_5",               # Field MUST be 'model' and valid version
            "callBackUrl": "http://example.com/callback" # Mandatory field for this API
        }
        
        try:
            response = requests.post(
                url, 
                headers=self._get_headers(), 
                json=payload, 
                timeout=20
            )
            data = response.json()
            if data.get('code') and data.get('code') != 200:
                error_msg = data.get('msg', 'Unknown API Error')
                print(f"Suno API Business Error: {error_msg}")
                raise Exception(f"Suno API Error: {error_msg}")

            response.raise_for_status()
            
            # The API returns a response containing taskId
            task_id = data.get('taskId') or data.get('id') or (data.get('data') and data.get('data').get('taskId'))
            
            if not task_id:
                print(f"DEBUG: No Task ID found in response: {data}")

            return {
                "suno_id": task_id,
                "status": "PENDING",
                "raw_response": data
            }
        except requests.exceptions.Timeout:
            print("Suno API Error: Request timed out")
            raise Exception("Suno API connection timed out")
        except requests.exceptions.RequestException as e:
            print(f"Suno API Request Error: {e}")
            raise e

    def get_status(self, task_id):
        """
        Checks generation status using the record-info endpoint.
        Handles the nested structure specific to sunoapi.org records.
        """
        url = f"{self.base_url}/generate/record-info"
        params = {"taskId": task_id}
        
        try:
            response = requests.get(url, headers=self._get_headers(), params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # Diagnostic revealed the following structure:
            # { "code": 200, "data": { "status": "...", "response": { "data": [ { "audioUrl": "..." } ] } } }
            
            api_inner_data = data.get('data', {})
            status = api_inner_data.get('status')
            
            # Find the audio URL in the nested response.sunoData list
            audio_url = None
            api_response = api_inner_data.get('response', {})
            if isinstance(api_response, dict):
                suno_data_list = api_response.get('sunoData', []) # Corrected: it's 'sunoData'
                if isinstance(suno_data_list, list) and len(suno_data_list) > 0:
                    audio_url = suno_data_list[0].get('audioUrl')
            
            # Map Suno SUCCESS to our Ready status
            mapped_status = 'Ready' if status == 'SUCCESS' else 'Generating'
            if status == 'ERROR':
                mapped_status = 'Failed'
                
            return {
                "suno_id": task_id,
                "status": mapped_status,
                "audio_url": audio_url,
                "raw_status": status
            }
        except requests.exceptions.RequestException as e:
            print(f"Suno API Status Error: {e}")
            return {"status": "Failed", "error": str(e)}
