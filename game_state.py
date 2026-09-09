"""Shared mutable state passed between scenes."""

selected_chapter = None   # set by level_select, read by story_mode
score = {}                # chapter_id -> stars earned
day   = 0                 # current in-game day (0 = story intro)
