import streamlit as st
import base64
from PIL import Image, ImageDraw, ImageFont
import io
import random

# Set page config
st.set_page_config(
    page_title="Eid Wishes Generator",
    page_icon="🌙",
    layout="centered"
)

# App title and description
st.title("🌙 Eid Mubarak Wishes Generator")
st.markdown("Create beautiful Eid greetings to share with your loved ones!")

# Predefined Eid wishes
eid_wishes = [
    "May the magic of this Eid bring lots of happiness in your life. Eid Mubarak!",
    "May Allah flood your life with happiness, success, and prosperity. Eid Mubarak!",
    "Wishing you and your family a blessed Eid filled with joy, peace, and prosperity.",
    "May Allah's blessings be with you today and always. Eid Mubarak!",
    "On this special day, may Allah bless you with peace, happiness, and prosperity. Eid Mubarak!",
    "Sending you warm wishes on Eid. May it bring joy and prosperity to you and your family.",
    "May this Eid bring joy, health, and wealth to you and your family. Eid Mubarak!",
    "Wishing you a joyful Eid celebration with your loved ones. Eid Mubarak!"
]

# Background colors
bg_colors = {
    "Gold": (255, 223, 0),
    "Light Green": (144, 238, 144),
    "Sky Blue": (135, 206, 235),
    "Lavender": (230, 230, 250),
    "Peach": (255, 218, 185),
    "Light Cyan": (224, 255, 255),
    "Mint": (189, 252, 201),
    "Coral": (255, 127, 80)
}

# Font colors
font_colors = {
    "Black": (0, 0, 0),
    "White": (255, 255, 255),
    "Dark Green": (0, 100, 0),
    "Navy Blue": (0, 0, 128),
    "Maroon": (128, 0, 0),
    "Purple": (128, 0, 128),
    "Dark Brown": (101, 67, 33),
    "Dark Blue": (0, 0, 139)
}

# Sidebar for customization
st.sidebar.header("Customize Your Greeting")

# Name input
recipient_name = st.sidebar.text_input("Recipient's Name", "")

# Select or enter a custom wish
wish_option = st.sidebar.radio(
    "Choose a wish option",
    ["Select from predefined wishes", "Write your own wish"]
)

if wish_option == "Select from predefined wishes":
    selected_wish = st.sidebar.selectbox("Select a wish", eid_wishes)
else:
    selected_wish = st.sidebar.text_area("Write your custom wish", "")

# Sender's name
sender_name = st.sidebar.text_input("Your Name", "")

# Color customization
bg_color_name = st.sidebar.selectbox("Background Color", list(bg_colors.keys()))
font_color_name = st.sidebar.selectbox("Text Color", list(font_colors.keys()))

# Card style
card_style = st.sidebar.radio("Card Style", ["Simple", "Decorative"])

# Generate greeting card
def generate_greeting_card():
    # Create a blank image
    width, height = 800, 600
    bg_color = bg_colors[bg_color_name]
    font_color = font_colors[font_color_name]
    
    image = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)
    
    # Try to load fonts, use default if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        main_font = ImageFont.truetype("arial.ttf", 36)
        name_font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        title_font = ImageFont.load_default()
        main_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
    
    # Add decorative elements if selected
    if card_style == "Decorative":
        # Draw crescent moon
        draw.ellipse((650, 50, 750, 150), fill=(255, 255, 255))
        draw.ellipse((630, 50, 730, 150), fill=bg_color)
        
        # Draw stars
        for _ in range(20):
            x = random.randint(20, width-20)
            y = random.randint(20, height-20)
            size = random.randint(3, 8)
            draw.ellipse((x, y, x+size, y+size), fill=font_color)
    
    # Draw title
    draw.text((width//2, 100), "Eid Mubarak", font=title_font, fill=font_color, anchor="mm")
    
    # Draw recipient name if provided
    if recipient_name:
        draw.text((width//2, 180), f"Dear {recipient_name},", font=name_font, fill=font_color, anchor="mm")
    
    # Draw the wish text with word wrapping
    wish_text = selected_wish
    lines = []
    words = wish_text.split()
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        text_width = draw.textlength(test_line, font=main_font)
        
        if text_width < width - 100:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    
    if current_line:
        lines.append(current_line)
    
    y_position = 250
    for line in lines:
        draw.text((width//2, y_position), line, font=main_font, fill=font_color, anchor="mm")
        y_position += 50
    
    # Draw sender name if provided
    if sender_name:
        draw.text((width//2, height-100), f"From: {sender_name}", font=name_font, fill=font_color, anchor="mm")
    
    return image

# Generate button
if st.sidebar.button("Generate Greeting Card"):
    if not selected_wish:
        st.warning("Please select or write a wish.")
    else:
        greeting_card = generate_greeting_card()
        st.image(greeting_card, caption="Your Eid Greeting Card", use_column_width=True)
        
        # Convert to bytes for download
        buf = io.BytesIO()
        greeting_card.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        # Download button
        st.download_button(
            label="Download Greeting Card",
            data=byte_im,
            file_name="eid_greeting.png",
            mime="image/png"
        )

# Display sample card on initial load
if 'greeting_card' not in st.session_state:
    sample_card = generate_greeting_card()
    st.image(sample_card, caption="Sample Eid Greeting Card", use_column_width=True)

# Footer
st.markdown("---")
st.markdown("### How to use this app")
st.markdown("""
1. Enter the recipient's name (optional)
2. Choose a predefined wish or write your own
3. Enter your name (optional)
4. Select background and text colors
5. Choose a card style
6. Click 'Generate Greeting Card'
7. Download your greeting card to share
""")

st.markdown("---")
st.markdown("Eid Mubarak! 🌙✨")