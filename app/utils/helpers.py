import os

from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Optional, TYPE_CHECKING
from PIL import Image, ImageChops

from data.models import Group

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_TEXTURE_PATH = BASE_DIR / "photos" / "white.png"

async def flag_texture(cid: str, input_image_path: str, texture_path: Optional[str] = None) -> Optional[str]:
    """
    Applies a wavy flag texture to an image.

    Args:
        cid: Unique identifier for the output file
        input_image_path: Path to the input image
        texture_path: Path to the flag texture (defaults to white.png)

    Returns:
        str: Path to the saved file or None on error
    """

    if texture_path is None:
        texture_path_obj = DEFAULT_TEXTURE_PATH
    else:
        texture_path_obj = Path(texture_path)

    input_path = Path(input_image_path)
    output_path = BASE_DIR / "photos" / f"{cid}.png"

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if not input_path.exists():
            print(f"Error: source file {input_path} not found")
            return None

        if not texture_path_obj.exists():
            print(f"Error: texture file {texture_path_obj} not found")
            return None

        with Image.open(input_path) as original_img:
            original_image = original_img.convert("RGB")

            with Image.open(texture_path_obj) as texture_img:
                flag_texture = texture_img.convert("L")
                flag_texture = flag_texture.resize(original_image.size, Image.Resampling.LANCZOS)
                
                r, g, b = original_image.split()
                
                r = ImageChops.multiply(r, flag_texture)
                g = ImageChops.multiply(g, flag_texture)
                b = ImageChops.multiply(b, flag_texture)
                
                result = Image.merge("RGB", (r, g, b))
                result.save(output_path, "PNG", optimize=True)

        return str(output_path)

    except Exception as e:
        print(f"Error processing image: {e}")
        return None
    
    
#-----------------------------------------------------------------------------------------

class GameTimeSystem:
    
    REAL_DAY_TO_GAME_DAYS = 365
    
    def __init__(self, group: 'Group'):
        self.group = group
    
    def get_current_date(self) -> date:
        real_days_passed = (date.today() - self.group.created_at).days
        game_days_passed = real_days_passed * self.REAL_DAY_TO_GAME_DAYS
        current_date = self.group.start_date + timedelta(days=game_days_passed)
        return current_date
    
    def get_formatted_date(self) -> str:
        current_date = self.get_current_date()
        
        months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        
        day = current_date.day
        month = months[current_date.month - 1]
        year = current_date.year
        
        return f"{day} {month} {year}"
    
    def get_years_passed(self) -> int:
        current_date = self.get_current_date()
        return (current_date - self.group.start_date).days // 365
    
    def get_days_until_next_year(self) -> int:
        real_days_passed = (date.today() - self.group.created_at).days
        days_until_next_real_day = 1 - (datetime.now().hour / 24 + datetime.now().minute / 1440)
        return int(days_until_next_real_day * 100) / 100
