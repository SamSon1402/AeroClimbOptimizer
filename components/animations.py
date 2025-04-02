import streamlit as st
import time

def load_lottie_url(url: str):
    """Load a Lottie animation from URL"""
    import requests
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def fade_in_text(text, element_type="p", delay=0.1):
    """Create fade-in text animation with specified HTML element type"""
    animated_element = f"""
    <div class="fade-in" style="animation-delay: {delay}s;">
        <{element_type}>{text}</{element_type}>
    </div>
    """
    return st.markdown(animated_element, unsafe_allow_html=True)

def staggered_animation(items, element_type="div", base_delay=0.1, class_name=""):
    """Create staggered animation for a list of items"""
    for i, item in enumerate(items):
        delay = base_delay * (i + 1)
        class_attr = f' class="{class_name}"' if class_name else ''
        animated_element = f"""
        <div class="fade-in" style="animation-delay: {delay}s;">
            <{element_type}{class_attr}>{item}</{element_type}>
        </div>
        """
        st.markdown(animated_element, unsafe_allow_html=True)
        
def animated_counter(start_val, end_val, prefix="", suffix="", duration=2.0):
    """Display an animated counter that counts up to a value"""
    import time
    import numpy as np
    
    # Create a placeholder
    counter_placeholder = st.empty()
    
    # Calculate step size for smooth animation
    steps = 30
    step_size = (end_val - start_val) / steps
    
    # Animate the counter
    for i in range(steps + 1):
        current_val = start_val + step_size * i
        counter_placeholder.markdown(
            f"""
            <div class="counter-value">
                {prefix}{int(current_val) if end_val == int(end_val) else round(current_val, 1)}{suffix}
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(duration / steps)