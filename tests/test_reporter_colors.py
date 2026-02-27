import pytest
from reporter import Reporter

def test_smart_score_colors():
    reporter = Reporter()
    
    # Test cases based on Spec: Green > 80, Amber 50-79, Red < 50
    # Updated: Now returns HSL string
    
    # 80-100: Green (120)
    assert "hsl(120, 100%, 40%)" in reporter._get_smart_score_bg_color(81)
    assert "hsl(120, 100%, 40%)" in reporter._get_smart_score_bg_color(90)
    
    # 0-20: Red (0)
    assert "hsl(0, 100%, 40%)" in reporter._get_smart_score_bg_color(19)
    assert "hsl(0, 100%, 40%)" in reporter._get_smart_score_bg_color(0)
    
    # 50: Midpoint (Hue 60?)
    # Ratio = (50 - 20) / 60 = 0.5
    # Hue = 120 * 0.5 = 60
    assert "hsl(60, 100%, 40%)" in reporter._get_smart_score_bg_color(50)

    assert "#D1D5DB" in reporter._get_smart_score_bg_color(None)

def test_vibe_colors():
    reporter = Reporter()
    # Vibe is 1-10
    # > 8 (Good), >= 5 (Avg), < 5 (Bad)
    
    assert "text-state-good" in reporter._get_vibe_class(8)
    assert "text-state-good" in reporter._get_vibe_class(10)
    
    assert "text-state-avg" in reporter._get_vibe_class(5)
    assert "text-state-avg" in reporter._get_vibe_class(7)
    
    assert "text-state-bad" in reporter._get_vibe_class(4)
    assert "text-state-bad" in reporter._get_vibe_class(1)
    
    assert "text-text-tertiary" in reporter._get_vibe_class(None)
