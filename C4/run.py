import getpass
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent/'.env',override=False)
provider=os.getenv('MODEL_PROVIDER','openai').lower()
variable='DEEPSEEK_API_KEY' if provider=='deepseek' else 'OPENAI_API_KEY'
if not os.getenv(variable):
    os.environ[variable]=getpass.getpass(f'{provider.title()} API key (hidden, kept only for this run): ').strip()
if not os.environ[variable]:
    raise SystemExit('No key entered.')
from app import build_app
from interface import CSS, THEME, HEAD
build_app().launch(server_name='127.0.0.1',server_port=int(os.getenv('PORT','7861')),share=False,inbrowser=True,theme=THEME,css=CSS,head=HEAD,footer_links=[])
